# -*- coding: utf-8 -*-

import os
import sys
import errno
import inspect

from mhundwa.models import Base, engine
from mhundwa.commands.index import parse as parse_index
from mhundwa.commands.post import parse as parse_post
from mhundwa.commands.download import download
from mhundwa.commands.inventory_post import inventory_post

import settings

sys.path.insert(0, os.path.abspath('.'))


def database_create(*args):
    """Создание базы данных и всех таблиц"""

    try:
        os.makedirs(settings.DATA_ROOT)
    except OSError as err:
        if err.errno == errno.EEXIST and os.path.isdir(settings.DATA_ROOT):
            pass
        else:
            raise

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


commands = {
    'parse_index': parse_index,
    'parse_post': parse_post,
    'database_create': database_create,
    'download': download,
    'inventory_post': inventory_post
}


if __name__ == '__main__':
    try:
        command = commands[sys.argv[1]]
    except (KeyError, IndexError) as e:
        if isinstance(e, KeyError):
            sys.stdout.write('Unknown command!\n\n')
        commands_list = u'\n'.join([
            u'{}: {}'.format(key, inspect.getdoc(value).decode('utf-8').split('\n')[0]) for key, value in commands.items()
        ])
        sys.stdout.write(u'Run one of those commands:\n\n{}\n'.format(commands_list))
        sys.exit(errno.EINVAL)

    command(*sys.argv[2:])
