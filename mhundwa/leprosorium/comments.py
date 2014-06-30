# -*- coding: utf-8 -*--

"""Функции, относящиеся к комментариям"""

from mhundwa.helpers import post
from mhundwa.leprosorium import get_csrf_token


def vote(id, value):
    """Ставит плюс/минус комментарию

    Параметры::
        id : идентификатор комментария
        value : добавляемое значение (-1 или +1)
    """

    if value not in (-1, 1):
        raise ValueError()

    # TODO:

    return post('https://leprosorium.ru/ajax/vote/comment/', data={
        'doc': id,
        'vote': value,
        'csrf_token': get_csrf_token(),
    })
