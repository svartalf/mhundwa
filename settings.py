# -*- coding: utf-8 -*-

# http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html
DATABASE_URI = 'sqlite:////tmp/lepra.db'

AUTH_USERNAME = ''
AUTH_PASSWORD = ''

# Настройки логирования. По умолчанию пишем все в консоль
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout',
            },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'filename': '/tmp/mhundwa.log',
            'when': 'midnight',
            'backupCount': 7,
        },
    },
    'formatters': {
        'detailed': {
            'format': '%(levelname)s %(asctime)s %(name)s %(message)s',
        },
    },
    'loggers': {
        'mhundwa': {
            'level':'DEBUG',
            'handlers': ['console',]
        },
    }
}

try:
    from settings_local import *
except ImportError:
    pass
