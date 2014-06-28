# -*- coding: utf-8 -*-

from __future__ import absolute_import

import re
import os
import urlparse
import html5lib
import datetime
import logging
import tempfile

from helpers import get
from models import Video, Post, session


logger = logging.getLogger(__name__)

SECONDS_RE = re.compile(r'(\d+)s')
MINUTES_RE = re.compile(r'(\d+)m(\d+)s')


def parse(post_id=None):
    """Парсинг отдельного поста

    Если `post_id` не указан, для проверки выбирается из базы пост за последний месяц с наименьшей датой обновления
    """

    if post_id:
        post = session.query(Post).filter_by(id=post_id).first()
        if post is None:
            post = Post(id=post_id, last_checked=datetime.datetime.now())
            session.add(post)
            session.commit()
    else:
        post = session.query(Post).order_by(Post.last_checked.asc()).first()
        if post is None:
            return  # TODO: warning message

    post.last_checked = datetime.datetime.now()
    session.add(post)
    session.commit()

    logger.debug('Parsing post #{}'.format(post.id))

    content = get('https://auto.leprosorium.ru/comments/{}/'.format(post.id))

    # Сохраняем копию страницы на всякий случай
    with open(os.path.join(tempfile.gettempdir(), '{}.html'.format(post.id)), 'w') as storage:
        storage.write(content)

    doc = html5lib.parse(content, treebuilder='lxml', namespaceHTMLElements=False)

    comments = doc.xpath('//div[@class="b-post_comments"]/div[contains(@class, "comment")]')
    for comment in comments:
        comment_id = int(comment.attrib['id'])
        author_id = int(comment.attrib['data-user_id'])
        comment_date = int(comment.xpath('.//span[contains(@class, "js-date")]')[0].attrib['data-epoch_date'])
        comment_date = datetime.datetime.fromtimestamp(comment_date)

        logger.debug('Processing comment #{}'.format(comment_id))

        links = comment.xpath('.//div[@class="c_body"]/a/@href')
        for link in links:
            if not 'youtu' in link:
                # TODO: проверять наличие ссылок на следующие автопосты
                logger.debug('Skipping link `{}`'.format(link))
                continue

            url = urlparse.urlparse(link)
            location = url.netloc
            params = urlparse.parse_qs(url.query)

            video_id, timestamp = None, 0
            if 'youtube.com' in location:
                video_id = params['v'][0]
            elif 'youtu.be' in location:
                video_id = url.path.lstrip('/')

            # Варианты написания timestamp в ссылке: 120, 16s, 2m32s
            try:
                timestamp = int(params['t'][0])
            except (KeyError, IndexError):
                pass
            except ValueError:
                match = SECONDS_RE.match(params['t'][0])
                if match:
                    timestamp = int(match.group(1))
                else:
                    match = MINUTES_RE.match(params['v'][0])
                    if match:
                        timestamp = (int(match.group(1)) * 60) + int(match.group(2))

            logger.debug('Saving information about YouTube video {}'.format(video_id))

            video = session.query(Video).filter_by(id=video_id).first()
            if video is None:
                video = Video(id=video_id, timestamp=timestamp, author_id=author_id, post_id=post.id,
                    comment_id=comment_id, posted=comment_date)
                session.add(video)
                session.commit()


if __name__ == '__main__':
    parse(1)
