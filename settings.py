# -*- coding: utf-8 -*-

# http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html
DATABASE_URI = 'sqlite:////tmp/lepra.db'

try:
    from settings_local import *
except ImportError:
    pass
