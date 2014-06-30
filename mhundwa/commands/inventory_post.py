# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import logging

import youtube_dl
from youtube_dl.utils import DownloadError


from mhundwa.models import Video, Post, session
import settings


log = logging.getLogger(__name__)


def inventory_post():
    """Инвентаризация поста
       Проверка наличия всех заплюсованных видео,
       перезалив, если видео не найдено на ютубе и добавление коммента
       с новым видео."""

    latest_posts = [x[0] for x in session.query(Post).order_by(Post.id.desc()).limit(2).values(Post.id)]
    videos = session.query(Video).filter(Video.post_id.in_(latest_posts)).filter_by(was_removed=False).order_by(Video.post_id.desc())

    downloader = youtube_dl.YoutubeDL({
        'outtmpl': os.path.join(settings.DATA_VIDEOS, '%(id)s'),
    })
    downloader.add_default_info_extractors()

    for video in videos:
        try:
            downloader.extract_info('http://www.youtube.com/watch?v={}'.format(video.id), download=False)
        except DownloadError:
            # Видео было удалено, закачиваем резервную копию, оставляем комментарий
            pass