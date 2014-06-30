# -*- coding: utf-8 -*--

import urllib

from mhundwa.helpers import post
from mhundwa.leprosorium import get_csrf_token


def vote(id, value):
    """Ставит плюс/минус комментарию"""

    if value not in (-1, 1):
        raise ValueError()

    response = post('https://leprosorium.ru/ajax/vote/comment/', data={
        'doc': id,
        'vote': value,
        'csrf_token': get_csrf_token(),
    })

    print response
