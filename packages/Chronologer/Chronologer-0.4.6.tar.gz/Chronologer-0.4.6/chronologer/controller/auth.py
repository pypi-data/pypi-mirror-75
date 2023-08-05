import sys
import json
import hashlib
from hmac import compare_digest
from collections import namedtuple
from http.cookies import SimpleCookie
from datetime import datetime, timezone

import jwt
import rules


User = namedtuple('User', ['username', 'roles'])


class PasswordAuthenticator:
  '''
  Password authenticator that verifies credentials.

  It either verifies credentials against single username-password pair
  or against a user list with hashed passwords.

  This class is thread-safe.
  '''

  _userdict = None
  _authfile = None


  def __init__(self, userdict = None, authfile = None):
    '''
    Initialise instance with either user data dictionary or a file-like object.

    The file-like object, if provided, must contain JSON of the following
    structure::

      [
        {
          "username": "bob",
          "pbkdf2": "f57ef1e3e8f90cb367dedd44091f251b5b15c9c36ddd7923731fa7ee41cbaa82",
          "hashname": "sha256",
          "salt": "c0139cff",
          "iterations": 32,
          "roles": ["writer"]
        }, {
          "username": "obo",
          "pbkdf2": "ff680a9237549f698da5345119dec1ed314eb4fdefe59837d0724d747c3169089ae45...",
          "hashname": "sha384",
          "salt": "9230dbdd5a13f009",
          "iterations": 4096,
          "roles": ["basic-reader", "query-reader"]
        }
      ]

    '''

    if authfile:
      if isinstance(authfile, str):
        with open(authfile) as fp:
          self._authfile = {r['username']: r for r in json.load(fp)}
      elif isinstance(authfile, list):
        self._authfile = {r['username']: r for r in authfile}
      else:
        raise ValueError('authfile has to be either filename or list of dictionaries')
    elif userdict:
      self._userdict = userdict
    else:
      raise ValueError('No authentication source provided')

  def _handleAuthfile(self, username, password):
    success = False
    roles = None
    if username in self._authfile:
      entry = self._authfile[username]
      roles = entry['roles']
      hash = hashlib.pbkdf2_hmac(
        entry['hashname'], password.encode(), entry['salt'].encode(), entry['iterations'])
      success = compare_digest(entry['pbkdf2'], hash.hex())

    return success, roles

  def _handleFixedCredentials(self, username, password):
    roles = self._userdict['roles']
    success = username == self._userdict['username'] and password == self._userdict['password']
    return success, roles

  def verify(self, username, password):
    if self._authfile:
      success, roles = self._handleAuthfile(username, password)
    else:
      success, roles = self._handleFixedCredentials(username, password)

    return (
      username if success else None,
      roles if success else None
    )


if sys.version_info < (3, 8):  # nocov
  # "backport" bpo-29613 for "samesite" cookie keyword
  import http.cookies
  http.cookies.Morsel._reserved.setdefault('samesite', 'SameSite')

class JwtCookieAuthenticator:
  '''
  JSON Web Token cookie authenticator.

  The cookie morsel this class generates to store the authentication
  JWT has ``httponly`` and ``samesite=strict`` attributes. The former
  helps to prevent XSS and the latter CSRF attacks.
  '''

  cookieName = 'Jwt'

  _secret = None


  def __init__(self, secret):
    self._secret = secret

  def verify(self, cookies):
    try:
      payload = jwt.decode(
        cookies[self.cookieName].value, self._secret, algorithms = ['HS256'], verify = True)
    except (jwt.InvalidTokenError, KeyError):
      return None, None
    else:
      return payload['username'], payload['roles']

  @classmethod
  def hasCookie(cls, cookies):
    return cls.cookieName in cookies

  @classmethod
  def createJwtMorsel(cls, user, secret):
    payload = user._asdict()
    payload['roles'] = list(payload['roles'])
    payload['iat'] = datetime.now(timezone.utc)
    jwtBytes = jwt.encode(payload, secret, algorithm = 'HS256')

    cookie = SimpleCookie()
    cookie[cls.cookieName] = jwtBytes.decode()
    cookie[cls.cookieName]['path'] = '/'
    cookie[cls.cookieName]['httponly'] = True
    cookie[cls.cookieName]['samesite'] = 'strict'
    return cookie[cls.cookieName]


def isA(role):
  @rules.predicate
  def predicate(request):
    return role in request.user.roles
  return predicate

@rules.predicate
def isQueryRequest(request):
  return bool(request.params.get('query'))

canReadRecord = isA('basic-reader') & (~isQueryRequest | isA('query-reader'))


def createRuleset():
  # Note that RuleSet can't be used in config directly because it's a dict.
  ruleset = rules.RuleSet()
  ruleset['RecordApi.HEAD'] = canReadRecord
  ruleset['RecordApi.GET']  = canReadRecord
  ruleset['RecordApi.POST'] = isA('writer')
  return ruleset

