import sys
import json
import base64
import binascii
from http import HTTPStatus

import cherrypy.lib
from cherrypy._cptools import Toolbox, Tool

from .auth import User
from ..model import ModelError
from ..storage import StorageQueryError, StorageSizeLimitError


chronotools = Toolbox('chronotools')


def json_encode(value):
  for chunk in json.JSONEncoder(default = str).iterencode(value):
    yield chunk.encode()

def json_handler(*args, **kwargs):
  value = cherrypy.serving.request._json_inner_handler(*args, **kwargs)
  return json_encode(value)

def jsonout(content_type = 'application/json'):
  '''Wrapper around built-in tool to pass ``default = str`` to encoder.'''

  cherrypy.lib.jsontools.json_out(content_type, False, json_handler)

chronotools.jsonout = Tool('before_handler', jsonout, priority = 30)
chronotools.jsonin  = Tool('before_request_body', cherrypy.lib.jsontools.json_in, priority = 30)


def ndjsonGenerator(fp):
  lineno = 0
  try:
    while True:
      line = fp.readline().decode()
      if not line:
        break
      lineno += 1
      yield json.loads(line)
  except (json.JSONDecodeError, UnicodeDecodeError):
    raise ValueError('Invalid JSON document on line {}'.format(lineno))

def ndjsonProcessor(entity):
  ''''Read application/x-ndjson data into generator request.ndjson.'''

  if not entity.headers.get('Content-Length'):
    raise cherrypy.HTTPError(HTTPStatus.LENGTH_REQUIRED.value)

  cherrypy.serving.request.ndjson = ndjsonGenerator(entity.fp)

@chronotools.register('before_request_body', priority = 30)
def ndjsonin(content_type):
  request = cherrypy.serving.request
  if isinstance(content_type, str):
    content_type = [content_type]

  for ct in content_type:
    request.body.processors[ct] = ndjsonProcessor


class JsonErrorTool(Tool):

  def __init__(self):
    super().__init__(self, None, None)

  @staticmethod
  def getErrorBody(type, message):
    return {'error': {'type': type, 'message': message}}

  def _handleUnexpectedError(self):
    extype, exobj, _ = sys.exc_info()

    status = HTTPStatus.INTERNAL_SERVER_ERROR.value
    if isinstance(exobj, (StorageQueryError, ModelError, ValueError)):
      status = HTTPStatus.BAD_REQUEST.value
    elif isinstance(exobj, StorageSizeLimitError):
      status = HTTPStatus.REQUEST_ENTITY_TOO_LARGE.value

    if cherrypy.serving.request.method == 'HEAD':
      cherrypy.serving.response.headers['X-Error-Type']    = extype.__name__
      cherrypy.serving.response.headers['X-Error-Message'] = str(exobj)
    else:
      cherrypy.serving.response.headers['Content-Type'] = 'application/json'
      cherrypy.serving.response.body = json.dumps(
        self.getErrorBody(extype.__name__, str(exobj))).encode()

    cherrypy.serving.response.status = status

  def _handleExpectedError(self, status, message, traceback, version):
    extype, _, _ = sys.exc_info()
    cherrypy.serving.response.headers['Content-Type'] = 'application/json'
    return json.dumps(
      self.getErrorBody(getattr(extype, '__name__', 'unknown'), message)).encode()

  def _setup(self):
    cherrypy.serving.request.error_response = self._handleUnexpectedError
    cherrypy.serving.request.error_page = {'default': self._handleExpectedError}

chronotools.jsonerror = JsonErrorTool()


def brotliCompress(body, level):
  import brotli
  compressor = brotli.Compressor(mode = brotli.MODE_TEXT, quality = level)
  for line in body:
    yield compressor.process(line)
  yield compressor.finish()

@chronotools.register('before_finalize', name = 'brotli', priority = 79)
def brotliTool(compress_level = 4, mime_types = ['text/html', 'text/plain'], debug = False):
  '''Adaptation of ``cherrypy.lib.encoding.gzip`` for Brotli.'''

  request = cherrypy.serving.request
  response = cherrypy.serving.response

  cherrypy.lib.set_vary_header(response, 'Accept-Encoding')

  # Response body is empty (might be a 304 for instance)
  if not response.body:
    return

  # If returning cached content, which should already have been compressed, don't re-compress
  if getattr(request, 'cached', False):
    return

  # If no Accept-Encoding field is present in a request,
  # the server MAY assume that the client will accept any
  # content coding. In this case, if "identity" is one of
  # the available content-codings, then the server SHOULD use
  # the "identity" content-coding, unless it has additional
  # information that a different content-coding is meaningful
  # to the client.
  acceptable = request.headers.elements('Accept-Encoding')
  if not acceptable:
    return

  for coding in acceptable:
    if coding.value == 'identity' and coding.qvalue != 0:
      return

    if coding.value == 'br':
      # brotliApply(coding, response, mime_types, compress_level, debug)
      if coding.qvalue == 0:
        return

      ct = response.headers.get('Content-Type', '').split(';')[0]
      if ct not in mime_types:
        return

      # Return a generator that compresses the response body
      response.headers['Content-Encoding'] = 'br'
      # Prevent gzip tool from re-compressing the body
      del request.headers['Accept-Encoding']

      response.body = brotliCompress(response.body, compress_level)
      if 'Content-Length' in response.headers:
        # Delete Content-Length header so finalize() recalcs it
        del response.headers['Content-Length']

      return


def authenticateBasic(handler, realm, negotiate):
  if not realm:
    raise ValueError('Realm is required for basic authentication')
  elif '"' in realm:
    raise ValueError('Realm cannot contain quotes')

  username = password = None

  header = cherrypy.serving.request.headers.get('Authorization')
  if header is not None:
    with cherrypy.HTTPError.handle(
        (ValueError, AssertionError, binascii.Error), HTTPStatus.BAD_REQUEST.value):
      scheme, creds = header.split(' ', 1)
      assert scheme.lower() == 'basic'
      username, password = base64.b64decode(creds, validate = True).decode().split(':', 1)

  username, roles = handler.verify(username, password)
  if username:
    authenticateSetRequestUser(username, roles)
  elif negotiate:
    cherrypy.serving.response.headers['Www-Authenticate'] = 'Basic realm="{}"'.format(realm)
    raise cherrypy.HTTPError(
      HTTPStatus.UNAUTHORIZED.value, 'You are not authorised to access that resource')
  else:
    raise cherrypy.HTTPError(HTTPStatus.FORBIDDEN.value)

def authenticateJwt(handler):
  username, roles = handler.verify(cherrypy.serving.request.cookie)
  if username:
    authenticateSetRequestUser(username, roles)
  else:
    raise cherrypy.HTTPError(HTTPStatus.FORBIDDEN.value)

def authenticateSetRequestUser(username, roles):
  cherrypy.serving.request.user = User(username, set(roles))

@chronotools.register('before_handler', name = 'authenticate', priority = 1)
def authenticateTool(
  jwt_handler = None,
  basic_handler = None,
  basic_realm = None,
  basic_negotiate = False,
):
  '''
  Combined Basic Auth and JWT authentication tool.

  The tool can work with either or both methods. A method is enabled
  by providing correspondent handler. If the JWT cookie is present
  JWT handler takes precedence over Basic Auth handler.

  :param jwt_handler:     Instance of ``JwtCookieAuthenticator``.
  :param basic_handler:   Instance of ``PasswordAuthenticator``.
  :param basic_realm:     When ``basic_handler`` is provided ``realm``
                          is required.
  :param basic_negotiate: Then ``True`` the tool replies with 401 on
                          missing authentication header, 403 otherwise.
  '''

  if jwt_handler and jwt_handler.hasCookie(cherrypy.serving.request.cookie):
    authenticateJwt(jwt_handler)
  elif basic_handler:
    authenticateBasic(basic_handler, basic_realm, basic_negotiate)
  else:
    raise cherrypy.HTTPError(HTTPStatus.FORBIDDEN.value)


@chronotools.register('before_handler')
def authorise(rulsetfactory):
  if not hasattr(authorise, '_ruleset'):
    authorise._ruleset = rulsetfactory()

  ruleName = '{app}.{method}'.format(
    app = cherrypy.serving.request.app.root.__class__.__name__,
    method = cherrypy.serving.request.method)

  if not authorise._ruleset.test_rule(ruleName, cherrypy.serving.request):
    raise cherrypy.HTTPError(HTTPStatus.FORBIDDEN.value)


@chronotools.register('before_finalize')
def forbiddenredirector(paths, url):
  request = cherrypy.serving.request
  if request.path_info in paths:
    _, exobj, _ = sys.exc_info()
    if isinstance(exobj, cherrypy.HTTPError) and exobj.code == HTTPStatus.FORBIDDEN.value:
      cherrypy.serving.response.status = HTTPStatus.SEE_OTHER.value
      cherrypy.serving.response.headers['Location'] = cherrypy.url(url)


@chronotools.register('before_handler', priority = 60)
def rootslash():
  if cherrypy.serving.request.path_info == '':
    raise cherrypy.HTTPRedirect(cherrypy.url('/'), status = HTTPStatus.MOVED_PERMANENTLY.value)

