# -*- coding: utf-8 -*-

"""Загрузка резервных копий видео из последних постов"""

import os
import logging

import youtube_dl

from mhundwa.models import Video, Post, session
import settings


logger = logging.getLogger(__name__)


def download():
    if not os.path.isdir(settings.VIDEOS_FOLDER):
        os.makedirs(settings.VIDEOS_FOLDER)

    latest_posts = [x[0] for x in session.query(Post).order_by(Post.id.desc()).limit(2).values(Post.id)]
    videos = session.query(Video).filter(Video.post_id.in_(latest_posts)).order_by(Video.post_id.desc())

    download_targets = []
    for video in videos:
        if not os.path.exists(os.path.join(settings.VIDEOS_FOLDER, video.id)):
            download_targets.append(video.id)

    if not download_targets:
        logger.debug('All videos are already downloaded')
        return

    downloader = youtube_dl.YoutubeDL({
        'outtmpl': os.path.join(settings.VIDEOS_FOLDER, '%(id)s'),
    })
    downloader.add_default_info_extractors()

    downloader.download(['http://www.youtube.com/watch?v={}'.format(id_) for id_ in download_targets])

    logger.info('Videos downloading is done')
