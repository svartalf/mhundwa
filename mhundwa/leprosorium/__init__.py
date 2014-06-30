# -*- coding: utf-8 -*-

"""Библиотека для запросов к лепре"""

import re

from mhundwa.helpers import get


CSRF_TOKEN_RE = re.compile(r'csrf_token\s*:\s*\'(.*)\'')


def get_csrf_token():
    """Для POST запросов нам нужен CSRF токен.

    Выдергиваем из любой страницы, которая открывается не так медленно, чтобы не мешать серверу"""

    # TODO: кэшировать CSRF токен в data/credentials.json

    response = get('https://leprosorium.ru/asylum')

    try:
        return CSRF_TOKEN_RE.findall(response)[0]
    except IndexError:
        raise RuntimeError('Cant get CSRF token from page')
