# -*- coding: utf-8 -*-

import os
import json
import logging
import tempfile

import requests

import settings


logger = logging.getLogger(__name__)


def get(url, max_retries=3):
    """Обертка над `requests.get`, делающая авторизацию, если сессионная кука протухла

    Сессионые куки лежат в файле `settings.DATA_CREDENTIALS`
    """

    cookie_file = os.path.join(tempfile.gettempdir(), settings.DATA_CREDENTIALS)
    try:
        with open(cookie_file, 'r') as storage:
            cookies = json.load(storage)
    except IOError:
        cookies = {}

    logger.debug('Making request with those auth cookies: {}'.format(cookies))

    session = requests.Session()
    session.cookies.update(cookies)

    while max_retries:
        response = session.get(url, allow_redirects=False)
        max_retries -= 1

        if response.status_code == 302:

            logger.debug('Making an authentication request')

            auth_response = session.post('https://leprosorium.ru/ajax/auth/login/', data={
                'username': settings.AUTH_USERNAME,
                'password': settings.AUTH_PASSWORD,
            })
            if auth_response.status_code == 200:
                logger.debug('Authentication completed')
                cookies = {
                    'uid': auth_response.cookies['uid'],
                    'sid': auth_response.cookies['sid'],
                }
                with open(cookie_file, 'w') as storage:
                    logger.debug('Saving auth cookies: {}'.format(cookies))
                    json.dump(cookies, storage)
                session.cookies.update(cookies)

                # Делаем заново запрос `url`
                continue

            else:
                logger.error('Cannot authenticate. Got response: {}'.format(auth_response.content))
                raise RuntimeError('Authentication failed')

        logger.debug('Got content from URL {}'.format(url))
        return response.content

    raise RuntimeError('Cant fetch page {}'.format(url))

if __name__ == '__main__':
    print get('https://auto.leprosorium.ru/comments/1736842/')
