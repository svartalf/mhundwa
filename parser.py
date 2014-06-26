# -*- coding: utf-8 -*-

"""Запускатель парсеров

>>> python2 parser.py post 1736842
где `post` - название файла из модуля `parsers`
"""

import sys
import importlib

name = sys.argv[1]
args = sys.argv[2:]

module = importlib.import_module('parsers.{}'.format(name))
parse = getattr(module, 'parse')

parse(*args)
