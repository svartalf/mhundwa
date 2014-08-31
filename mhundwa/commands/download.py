# -*- coding: utf-8 -*-

"""Загрузка резервных копий видео из последних постов"""

import os
import logging

import youtube_dl
from youtube_dl.utils import DownloadError

from mhundwa.models import Video, Post, session
from mhundwa.leprosorium.comments import vote
import settings


logger = logging.getLogger(__name__)


def download():
    """Резервное копирование видео файлов"""

    if not os.path.isdir(settings.DATA_VIDEOS):
        os.makedirs(settings.DATA_VIDEOS)

    latest_posts = [x[0] for x in session.query(Post).order_by(Post.id.desc()).limit(1).values(Post.id)]
    videos = session.query(Video).filter(Video.post_id.in_(latest_posts)).filter_by(was_removed=False).order_by(Video.post_id.desc())

    download_targets = []
    for video in videos:
        if not os.path.exists(os.path.join(settings.DATA_VIDEOS, video.id)):
            download_targets.append(video)

    if not download_targets:
        logger.debug('All videos are already downloaded')
        return

    downloader = youtube_dl.YoutubeDL({
        'outtmpl': os.path.join(settings.DATA_VIDEOS, '%(id)s'),
        'cachedir': os.path.join(settings.DATA_VIDEOS, '.cache'),
    })
    downloader.add_default_info_extractors()

    for video in download_targets:
        try:
            downloader.extract_info('http://www.youtube.com/watch?v={}'.format(video.id))
        except DownloadError as e:
            if 'This video has been removed by the user' in e.message:
                session.query(Video).filter_by(id=video.id).update({'was_removed': True})
                session.commit()

                continue

        else:
            # Ставим плюс комментарию, отмечая, что мы сделали копию видео
            vote(video.comment_id, +1)

    logger.info('{} video(s) downloading is done'.format(len(download_targets)))

    logger.debug('Cleaning up videos directory')

    required_videos = [x.id for x in videos]
    for root, _, files in os.walk(settings.DATA_VIDEOS):
        for filename in files:
            if filename not in required_videos:
                os.remove(os.path.join(root, filename))
                logger.info('Removing video file {}'.format(filename))

    logger.debug('Videos directory is clean now')
