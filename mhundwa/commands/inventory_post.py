# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import random
import logging

import youtube_dl
from youtube_dl.utils import DownloadError

from mhundwa.models import Video, Post, session
from mhundwa.youtube import upload_video
from mhundwa.leprosorium.comments import create
import settings


logger = logging.getLogger(__name__)

COMMENT_TEMPLATE = u'''<a href="http://www.youtube.com/watch?v={video.repost_id}&t={video.timestamp}">
<img src="http://img.youtube.com/vi/{video.repost_id}/{randint}.jpg" width="120" height="90">
</a>'''


def inventory_post():
    """Инвентаризация поста
       Проверка наличия всех заплюсованных видео,
       перезалив, если видео не найдено на ютубе и добавление коммента
       с новым видео."""

    latest_posts = [x[0] for x in session.query(Post).order_by(Post.id.desc()).limit(2).values(Post.id)]
    videos = session.query(Video).filter(Video.post_id.in_(latest_posts)).filter_by(was_removed=False, repost_id=None).order_by(Video.post_id.desc())

    downloader = youtube_dl.YoutubeDL({
        'outtmpl': os.path.join(settings.DATA_VIDEOS, '%(id)s'),
    })
    downloader.add_default_info_extractors()

    for video in videos:
        if not os.path.exists(os.path.join(settings.DATA_VIDEOS, video.id)):
            logger.warning('Skipping video {} check, because video file doesn\'t exists'.format(video.id))
            continue

        try:
            downloader.extract_info('http://www.youtube.com/watch?v={}'.format(video.id), download=False)
        except DownloadError:
            # Видео было удалено, закачиваем резервную копию, оставляем комментарий

            try:
                video = upload_video(video)
            except RuntimeError:
                logger.exception('Got unexpected error')
                continue

            comment = COMMENT_TEMPLATE.format(video=video, randint=random.randint(1, 3))
            create(video.post_id, video.comment_id, comment)
