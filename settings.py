# -*- coding: utf-8 -*-

from os import path


PWD = path.abspath('.')

# Корневая папка данных
DATA_ROOT = path.join(PWD, 'mhundwa-data')

# Путь до папки с копиями видео
DATA_VIDEOS = path.join(DATA_ROOT, 'videos')

# Путь к файлу с данными авторизации
DATA_CREDENTIALS = path.join(DATA_ROOT, 'credentials.json')

# URI подключения к БД
# http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html
DATABASE_URI = 'sqlite:///{}'.format(path.join(DATA_ROOT, 'mhundwa.sqlite'))

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
