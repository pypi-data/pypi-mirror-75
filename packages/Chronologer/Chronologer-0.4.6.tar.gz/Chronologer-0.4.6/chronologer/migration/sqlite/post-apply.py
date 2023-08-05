import os
import shutil
import logging
from urllib.parse import urlparse

import cherrypy


user = cherrypy.config.get('server.user')
group = cherrypy.config.get('server.group')
if user or group:
  path = urlparse(cherrypy.config['storage']['dsn']).path.split('/', 1)[1]
  if os.path.exists(path):
    logging.getLogger('yoyo.migrations').info(
      ' - chowning database file and its dir to {}:{}'.format(user, group))
    shutil.chown(path, user, group)
    shutil.chown(os.path.dirname(path), user, group)

