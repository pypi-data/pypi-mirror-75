import logging
from http import HTTPStatus
from datetime import timezone, timedelta

import schedule
import cherrypy
from cherrypy.process.plugins import Monitor

from .auth import JwtCookieAuthenticator
from .toolbox import chronotools
from .. import __version__
from ..storage import StorageError
from ..model import createRecord, groupTimeseries, ModelError
from ..utility import chunk, parse8601


__all__ = 'RecordApi', 'RecordPurgePlugin', 'UiAuthn', 'UiInfo', 'Redirector', 'chronotools'

logger = logging.getLogger(__name__)


class RecordApi:

  exposed = True


  def HEAD(self, **kwargs):
    filters = self._getFilters(**kwargs)
    group   = kwargs.get('group')
    tz      = kwargs.get('timezone')
    if group and timezone:
      m15Grp = cherrypy.request.app.storage.count(filters, group = True)
      grps, cnts = list(zip(*groupTimeseries(m15Grp, group, tz))) or ['', '']
      cherrypy.response.headers['X-Record-Group'] = ','.join(str(int(v.timestamp())) for v in grps)
      cherrypy.response.headers['X-Record-Count'] = ','.join(map(str, cnts))
    else:
      cherrypy.response.headers['X-Record-Count'] = cherrypy.request.app.storage.count(filters)

    cherrypy.response.headers['Cache-Control'] = 'no-cache'

  @chronotools.jsonout(content_type = 'application/json')
  def GET(self, _id = None, **kwargs):
    storage = cherrypy.request.app.storage
    if _id:
      record = storage.get(_id)
      if not record:
        raise cherrypy.HTTPError(HTTPStatus.NOT_FOUND.value)

      cherrypy.response.headers['Cache-Control'] = 'max-age=2600000'  # let cache for ~1 month
      return record.asdict()
    else:
      filters = self._getFilters(**kwargs)
      range = storage.range(int(kwargs['left']), int(kwargs['right']), filters)
      cherrypy.response.headers['Cache-Control'] = 'no-cache'
      return [r.asdict() for r in range]

  @chronotools.jsonout(content_type = 'application/json')
  @chronotools.jsonin(content_type = 'application/json', force = False)
  @chronotools.ndjsonin(content_type = 'application/x-ndjson')
  def POST(self, **kwargs):
    raw = int(kwargs.get('raw', 0))
    if cherrypy.request.body.type.value == 'application/x-www-form-urlencoded':
      record = createRecord(cherrypy.request.body.params, raw = raw, parse = True)
    elif cherrypy.request.body.type.value == 'application/json':
      record = createRecord(cherrypy.request.json, raw = raw)
    elif cherrypy.request.body.type.value == 'application/x-ndjson':
      return self._createMultiple(cherrypy.request.ndjson, raw)
    else:
      supported = 'application/x-www-form-urlencoded', 'application/json', 'application/x-ndjson'
      raise cherrypy.HTTPError(
        HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value,
        'Supported content types: {}'.format(', '.join(supported))
      )

    record = cherrypy.request.app.storage.record([record])[0]
    cherrypy.response.status = HTTPStatus.CREATED.value
    return record.asdict()

  def _createMultiple(self, ndjson, raw):
    ids = []
    try:
      for logdicts in chunk(cherrypy.request.ndjson, cherrypy.config['ingestion']['chunk_size']):
        records = cherrypy.request.app.storage.record(
          [createRecord(d, raw = raw) for d in logdicts]
        )
        ids.extend(r.id for r in records)
    except (ValueError, ModelError, StorageError) as ex:
      logger.exception('Multiline request error')
      if not ids:
        raise cherrypy.HTTPError(HTTPStatus.BAD_REQUEST.value, str(ex))
      else:
        cherrypy.response.status = HTTPStatus.MULTI_STATUS.value
        errorBody = chronotools.jsonerror.getErrorBody(type(ex).__name__, str(ex))
        return {
          'multistatus' : [
            {'status': HTTPStatus.CREATED,     'body': ids},
            {'status': HTTPStatus.BAD_REQUEST, 'body': errorBody},
          ]
        }
    else:
      cherrypy.response.status = HTTPStatus.CREATED.value
      return ids

  def _getFilters(self, **kwargs):
    return {
      'date'  : (parse8601(kwargs.get('after')), parse8601(kwargs.get('before'))),
      'level' : kwargs.get('level'),
      'name'  : kwargs.get('name'),
      'query' : kwargs.get('query')
    }


class RecordPurgePlugin(Monitor):

  _storage = None
  _schedule = None
  _older = None


  def __init__(self, bus, storage):
    self._storage = storage
    self._schedule = schedule.Scheduler()
    self._schedule.every().day.at('00:00').do(self._purge)

    # Zero frequency means no timing thread will be created
    frequency = 0
    retainDays = cherrypy.config['retention']['days']
    if retainDays:
      frequency = 300
      self._older = timedelta(days = float(retainDays))

    super().__init__(bus, self._schedule.run_pending, frequency = frequency)

  def _purge(self):
    count = self._storage.purge(self._older)
    logger.info('Purged records: %s', count)


class Redirector:

  @cherrypy.expose
  def index(self):
    raise cherrypy.HTTPRedirect(cherrypy.request.config['url'])


class Health:

  @cherrypy.expose
  def index(self):
    return 'OK'


class UiAuthn:
  '''
  UI authentication resource.

  It's not a part of the Chronologer HTTP API and is only mounted when
  UI package is present. Available methods are as follows:

    - ``HEAD`` returns current user set by the authentication tool,
    - ``GET`` sets JWT token, assuming Basic Auth, and redirects to
      the mount-point,
    - ``DELETE`` resets JWT cookie and facilitates rest of Basic Auth.

  The controller must be mounted on a prefix that authenticates with
  both Basic Auth and JWT cookie because on ``DELETE`` UI resets Basic
  Auth and the request can only be authenticated with JWT.
  '''

  exposed = True


  def HEAD(self):
    cherrypy.response.headers['X-Username'] = (
      cherrypy.request.user.username if hasattr(cherrypy.request, 'user') else '')
    cherrypy.response.headers['X-Version'] = __version__

  def GET(self):
    morsel = JwtCookieAuthenticator.createJwtMorsel(
      cherrypy.request.user, cherrypy.config['auth']['secret'])
    cherrypy.response.cookie[morsel.key] = morsel
    raise cherrypy.HTTPRedirect(cherrypy.url('/'))

  def DELETE(self):
    morsel = JwtCookieAuthenticator.createJwtMorsel(cherrypy.request.user, secret = '')
    morsel.set(morsel.key, '', '')
    morsel['max-age'] = 0
    cherrypy.response.cookie[morsel.key] = morsel
    # Chromium doesn't reset basic auth with 200 OK
    cherrypy.response.status = HTTPStatus.UNAUTHORIZED.value

