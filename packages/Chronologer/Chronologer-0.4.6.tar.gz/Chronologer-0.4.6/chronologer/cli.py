import os
from urllib.parse import urlparse
from argparse import ArgumentParser
from importlib.machinery import SourceFileLoader

import cherrypy
import yoyo.connections
from clor import configure
from cherrypy import daemon

from .server import bootstrap
from .storage.mysql import YoyoMysqlBackend


def serve(config, user = None, group = None, premigrate = False, **kwargs):
  if user or group:
    # set for SQLite migration post-apply
    cherrypy.config['server.user'] = user
    cherrypy.config['server.group'] = group

    cherrypy.process.plugins.DropPrivileges(
      cherrypy.engine, uid = user, gid = group, umask = 0o022).subscribe()

  if premigrate:
    migrate(config)

  daemon.start(**kwargs)


def migrate(config, **kwargs):
  yoyo.connections.BACKENDS['mysql'] = YoyoMysqlBackend

  dir = urlparse(config['storage']['dsn']).scheme.split('+', 1)[0]
  migrations = yoyo.read_migrations(os.path.join(os.path.dirname(__file__), 'migration', dir))

  backend = yoyo.get_backend(config['storage']['dsn'], migration_table = 'schema_version')
  backend.apply_migrations(backend.to_apply(migrations))


def createArgParser():
  p = ArgumentParser()
  sp = p.add_subparsers(dest = 'subparser')

  p.add_argument(
    '-c', dest = 'envconf',
    default = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'envconf.py'),
    help = 'Override default envconf.py')
  p.add_argument(
    '-e', dest = 'environment', default = 'development',
    help = 'Apply the given config environment')

  srv = sp.add_parser('serve')
  srv.add_argument(
    '-d', action = 'store_true', dest = 'daemonize', help = 'Run the server as a daemon')
  srv.add_argument(
    '-p', dest = 'pidfile', default = None, help = 'Store the process id in the given file')
  srv.add_argument(
    '-u', dest = 'user', default = None, help = 'Run application as specified user')
  srv.add_argument(
    '-g', dest = 'group', default = None, help = 'Run application as specified group')
  srv.add_argument(
    '-m', dest = 'premigrate', action = 'store_true', help = 'Run migrations before serving')

  sp.add_parser('migrate')

  return p


def main():
  parser = createArgParser()
  kwargs = vars(parser.parse_args())

  cherrypy.config.environments.setdefault('development', {})
  cherrypy.config['environment'] = kwargs['environment']

  envconfs = SourceFileLoader('envconf', kwargs.pop('envconf')).load_module()
  config = configure(*getattr(envconfs, kwargs['environment']))

  cmd = kwargs.pop('subparser')
  if not cmd:
    parser.print_help()
  else:
    bootstrap(config)
    globals()[cmd](config, **kwargs)
