# -*- coding: utf-8 -*-

"""https://developers.google.com/youtube/v3/code_samples/python#upload_a_video"""

import os
import sys
import time
import random
import httplib
import httplib2
import logging

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow, argparser

from mhundwa.models import session
import settings


logger = logging.getLogger(__name__)


RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected, httplib.IncompleteRead,
                        httplib.ImproperConnectionState, httplib.CannotSendRequest, httplib.CannotSendHeader,
                        httplib.ResponseNotReady, httplib.BadStatusLine)

RETRIABLE_STATUS_CODES = (500, 502, 503, 504)


def _get_youtube_service():
    flow = flow_from_clientsecrets(settings.GOOGLE_API_CREDENTIALS, scope='https://www.googleapis.com/auth/youtube')

    storage = Storage(os.path.join(settings.DATA_ROOT, 'google-credentials-oauth.json'))
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        args = sys.argv[2:]
        args.append('--noauth_local_webserver')
        credentials = run_flow(flow, storage, argparser.parse_args(args))

    return build('youtube', 'v3', http=credentials.authorize(httplib2.Http()))


def _upload(request, video):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            status, response = request.next_chunk()
            if 'id' in response:
                video.repost_id = response['id']
                session.add(video)
                session.commit()

                logger.info('Reposted video {} with new ID {}'.format(video.id, video.repost_id))

                return video

            raise ValueError('Upload failed with an unexpected response: {}'.format(response))

        except HttpError as e:
            error = True
            if e.resp.status not in RETRIABLE_STATUS_CODES:
                raise

        except RETRIABLE_EXCEPTIONS:
            error = True

    if error is not None:
        error = None
        retry += 1
        if retry > 10:
            raise RuntimeError('No longer attempting to retry.')

        max_sleep = 2 ** retry
        sleep_seconds = random.random() * max_sleep
        logger.debug('Sleeping {f} seconds and then retrying'.format(sleep_seconds))
        time.sleep(sleep_seconds)


def upload_video(video):
    """Загрузка видео на YouTube

    Параметры::
        video : объект модели `mhundwa.models.Video`
    """

    filename = os.path.join(settings.DATA_VIDEOS, video.id)
    if not os.path.exists(filename):
        raise RuntimeError('Video file {} is not exists'.format(video.id))

    youtube = _get_youtube_service()

    body = {
        'snippet': {
            'title': video.id,
        },
        'status': {
            'privacyStatus': 'unlisted',
        }
    }

    request = youtube.videos().insert(part=','.join(body.keys()), body=body,
                                      media_body=MediaFileUpload(filename, mimetype='video/mp4', chunksize=-1, resumable=True))

    return _upload(request, video)
