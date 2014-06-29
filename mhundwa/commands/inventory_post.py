# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import settings


log = logging.getLogger(__name__)


def inventory_post():
    """Инвентаризация поста
       Проверка наличия всех заплюсованных видео,
       перезалив, если видео не найдено на ютубе и добавление коммента
       с новым видео."""

    log.debug('inventory started')
