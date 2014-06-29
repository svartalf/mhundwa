# -*- coding: utf-8 -*-

"""Загрузка резервных копий видео из последних постов"""

import os
import logging

import youtube_dl
from youtube_dl.utils import DownloadError

from mhundwa.models import Video, Post, session
import settings


logger = logging.getLogger(__name__)


def download():
    """Резервное копирование видео файлов"""

    if not os.path.isdir(settings.VIDEOS_FOLDER):
        os.makedirs(settings.VIDEOS_FOLDER)

    latest_posts = [x[0] for x in session.query(Post).order_by(Post.id.desc()).limit(2).values(Post.id)]
    videos = session.query(Video).filter(Video.post_id.in_(latest_posts)).filter_by(was_removed=False).order_by(Video.post_id.desc())

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

    for video_id in download_targets:
        try:
            downloader.extract_info('http://www.youtube.com/watch?v={}'.format(video_id))
        except DownloadError as e:
            if 'This video has been removed by the user' in e.message:
                session.query(Video).filter_by(id=video_id).update({'was_removed': True})
                session.commit()
                continue

    logger.info('{} video(s) downloading is done'.format(len(download_targets)))

    logger.debug('Cleaning up videos directory')

    required_videos = [x.id for x in videos]
    for root, _, files in os.walk(settings.VIDEOS_FOLDER):
        for filename in files:
            if filename not in required_videos:
                os.remove(os.path.join(root, filename))
                logger.info('Removing video file {}'.format(filename))

    logger.debug('Videos directory is clean now')
