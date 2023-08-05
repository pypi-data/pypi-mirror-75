'''Application environment configuration.

Configuration keys that can be overridden through environment variables:

  * CHRONOLOGER_USERNAME
  * CHRONOLOGER_PASSWORD
  * CHRONOLOGER_ROLES
  * CHRONOLOGER_AUTHFILE
  * CHRONOLOGER_SECRET
  * CHRONOLOGER_STORAGE_DSN
  * CHRONOLOGER_HOST
  * CHRONOLOGER_PORT
  * CHRONOLOGER_THREAD_POOL_SIZE
  * CHRONOLOGER_RETENTION_DAYS
  * CHRONOLOGER_HTTP_COMPRESS_LEVEL

'''


import os


__all__ = 'production', 'development', 'test_suite'


base = {
  'global' : {
    # HTTP server
    'server.socket_host' : os.environ.get('CHRONOLOGER_HOST', '127.0.0.1'),
    'server.socket_port' : int(os.environ.get('CHRONOLOGER_PORT', 8080)),
    'server.thread_pool' : int(os.environ.get('CHRONOLOGER_THREAD_POOL_SIZE', 8)),
    # file change reload
    'engine.autoreload.on' : False,
    # URL trailing slash
    'tools.trailing_slash.on' : False,
    # logging
    'log.screen'      : False,
    'log.access_file' : None,
    'log.error_file'  : None,
    # JSON error page
    'chronotools.jsonerror.on' : True
  },
  'logging' : {
    'disable_existing_loggers' : False,
    'version'                  : 1,
    'formatters'               : {
      'print' : {
        'format' : '%(levelname)-8s %(name)-15s %(message)s'
      },
    },
    'handlers' : {
      'console' : {
        'class'     : 'logging.StreamHandler',
        'formatter' : 'print'
      },
    },
    'root' : {
      'handlers' : ['console'],
    }
  },
  'storage' : {
    'dsn' : os.environ.get('CHRONOLOGER_STORAGE_DSN'),
  },
  'retention' : {
    # Days to retain log records, forever if ``None``
    'days': os.environ.get('CHRONOLOGER_RETENTION_DAYS')
  },
  'auth' : {
    'username' : os.environ.get('CHRONOLOGER_USERNAME', 'logger'),
    'password' : os.environ.get('CHRONOLOGER_PASSWORD', ''),
    'roles'    : os.environ.get('CHRONOLOGER_ROLES', 'basic-reader writer').split(),
    'authfile' : os.environ.get('CHRONOLOGER_AUTHFILE'),
    'secret'   : os.environ.get('CHRONOLOGER_SECRET'),
  },
  'ingestion' : {
    'chunk_size' : 1024
  },
  'app' : {
    'api' : {
      '/' : {
        'request.dispatch' : {
          '()' : 'cherrypy._cpdispatch.MethodDispatcher'
        }
      }
    },
    'ui' : {
      '/authn' : {
        'request.dispatch' : {
          '()' : 'cherrypy._cpdispatch.MethodDispatcher'
        }
      },
    },
  },
}

production = (base, {
  'global' : {
    'server.socket_host' : os.environ.get('CHRONOLOGER_HOST', '0.0.0.0'),
    # compression: gzip unless brotli is accepted
    'tools.gzip.on'                    : True,
    'tools.gzip.mime_types'            : ['application/json', 'application/javascript'],
    'tools.gzip.compress_level'        : int(os.environ.get('CHRONOLOGER_HTTP_COMPRESS_LEVEL', 6)),
    'chronotools.brotli.on'            : True,
    'chronotools.brotli.mime_types'    : ['application/json', 'application/javascript'],
    'chronotools.brotli.compress_level': int(os.environ.get('CHRONOLOGER_HTTP_COMPRESS_LEVEL', 4)),
  },
  'logging' : {
    'handlers' : {
      'console' : {
        'level' : 'INFO',
      },
    },
    'root' : {
      'level' : 'INFO',
    },
  },
  'authenticator' : {
    'password' : {
      '()'       : 'chronologer.controller.auth.PasswordAuthenticator',
      'userdict' : {
        'username' : 'cfg://auth.username',
        'password' : 'cfg://auth.password',
        'roles'    : 'cfg://auth.roles',
      }
    },
    'jwt' : {
      '()'     : 'chronologer.controller.auth.JwtCookieAuthenticator',
      'secret' : 'cfg://auth.secret',
    },
  },
  'app' : {
    'api' : {
      '/' : {
        # authentication
        'chronotools.authenticate.on'              : True,
        'chronotools.authenticate.basic_realm'     : 'Chronologer API',
        'chronotools.authenticate.basic_handler'   : 'cfg://authenticator.password',
        'chronotools.authenticate.basic_negotiate' : False,
        'chronotools.authenticate.jwt_handler'     : 'cfg://authenticator.jwt',
        # authorisation
        'chronotools.authorise.on'            : True,
        'chronotools.authorise.rulsetfactory' : 'ext://chronologer.controller.auth.createRuleset',
      }
    },
    'ui' : {
      '/' : {
        # relative paths of UI need trailing slash
        'chronotools.rootslash.on' : True,
        # only allow JWT authentication
        'chronotools.authenticate.on'          : True,
        'chronotools.authenticate.jwt_handler' : 'cfg://authenticator.jwt',
        # in case of lost JWT cookie
        'chronotools.forbiddenredirector.on'    : True,
        'chronotools.forbiddenredirector.paths' : ['/'],
        'chronotools.forbiddenredirector.url'   : '/authn',
      },
      '/authn' : {
        'chronotools.authenticate.on'              : True,
        'chronotools.authenticate.basic_realm'     : 'Chronologer UI',
        'chronotools.authenticate.basic_handler'   : 'cfg://authenticator.password',
        'chronotools.authenticate.basic_negotiate' : True,
        'chronotools.authenticate.jwt_handler'     : 'cfg://authenticator.jwt',
      },
    },
  }
})

development = (base, {
  'storage' : {
    'dsn' : os.environ.get('CHRONOLOGER_STORAGE_DSN', 'mysql://guest@localhost/chronologer'),
  },
  'logging' : {
    'handlers' : {
      'console' : {
        'level' : 'DEBUG',
      },
    },
    'root' : {
      'level' : 'DEBUG',
    },
  },
  'app' : {
    'api' : {
      '/' : {
        'tools.response_headers.on'      : True,
        'tools.response_headers.headers' : [
          ('Access-Control-Allow-Origin', '*'),
          ('Access-Control-Expose-Headers', 'X-Record-Count, X-Record-Group')
        ]
      }
    },
    'ui' : {
      '/authn' : {
        'tools.response_headers.on'      : True,
        'tools.response_headers.headers' : [
          ('Access-Control-Allow-Origin', '*'),
          ('Access-Control-Expose-Headers', 'X-Version, X-Username')
        ]
      }
    },
  }
})

test_suite = (base, {
  'global' : {
    # Remove these, as they prevent CherryPy simulator from working
    'server.socket_host' : None,
    'server.socket_port' : None,
  },
  'storage' : {
    'dsn' : os.environ.get(
      'CHRONOLOGER_STORAGE_DSN', 'mysql://root:pass@127.0.0.1/chronologer_test'
    ),
  },
  'auth' : {
    'secret'   : os.environ.get('CHRONOLOGER_SECRET', '...to nail the next fool martyr'),
  },
  'logging' : {
    'handlers' : {
      'console' : {
        'level' : 'WARNING',
      },
    },
    'root' : {
      'level' : 'WARNING',
    },
  }
})

