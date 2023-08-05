import logging.config

import cherrypy

try:
  import chronologerui
except ImportError:
  chronologerui = None

from . import storage, controller


__all__ = 'bootstrap',


def prepareControllers(config):
  yield '/api/v1/record', controller.RecordApi(), config['app']['api']
  yield '/health', controller.Health(), None
  if chronologerui:
    if not config['auth']['secret']:
      raise ValueError('UI authentication requires CHRONOLOGER_SECRET to be defined')

    ui = chronologerui.Ui()
    ui.authn = controller.UiAuthn()
    yield '/ui', ui, config['app']['ui']
    yield '/', controller.Redirector(), {'/': {'url': '/ui/authn'}}


def bootstrap(config):
  '''Bootstrap application server'''

  logging.config.dictConfig(config['logging'])

  # Make cherrypy.process.wspbus.Bus.block interval shorter to reduce idle CPU usage
  cherrypy.engine.block.__func__.__defaults__ = 1,

  # If "global" is present it'll be used alone
  cherrypy.config.update(config.pop('global'))
  cherrypy.config.update(config)

  storageObj = storage.createStorage(config['storage']['dsn'])

  apps = [
    cherrypy.tree.mount(app, url, appcfg or {'/': {}})
    for url, app, appcfg in prepareControllers(config)]
  for app in apps:
    app.storage = storageObj
    app.toolboxes[controller.chronotools.namespace] = controller.chronotools

  purgePlugin = controller.RecordPurgePlugin(cherrypy.engine, storageObj)
  purgePlugin.subscribe()
  cherrypy.engine.subscribe('exit', purgePlugin.unsubscribe)

