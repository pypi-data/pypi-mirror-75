import warnings

import cherrypy
from clor import configure

from .. import server, envconf


def bootstrap(*, extraConfig = None):
  cherrypy.config.update({'environment': 'test_suite'})
  extraConfig = (extraConfig,) if extraConfig else ()
  config = configure(*(getattr(envconf, 'test_suite') + extraConfig))
  server.bootstrap(config)


def warntoexc():
  warnings.simplefilter('error')

