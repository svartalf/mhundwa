# -*- coding: utf-8 -*-

from __future__ import absolute_import

import re
import urlparse
import html5lib
import datetime

import requests

from models import Video, session


SECONDS_RE = re.compile(r'(\d+)s')
MINUTES_RE = re.compile(r'(\d+)m(\d+)s')


def parse(post_id):
    """Парсинг отдельного поста"""

    content = open('/tmp/post.html')
    # content = requests.get('https://auto.leprosorium.ru/comments/{}/'.format(post_id))
    doc = html5lib.parse(content, treebuilder='lxml', namespaceHTMLElements=False)

    comments = doc.xpath('//div[@class="b-post_comments"]/div[contains(@class, "comment")]')
    for comment in comments:
        comment_id = int(comment.attrib['id'])
        post_id = int(comment.attrib['data-post_id'])
        author_id = int(comment.attrib['data-user_id'])
        comment_date = int(comment.xpath('.//span[contains(@class, "js-date")]')[0].attrib['data-epoch_date'])
        comment_date = datetime.datetime.fromtimestamp(comment_date)

        links = comment.xpath('.//div[@class="c_body"]/a/@href')
        for link in links:
            if not 'youtu' in link:
                continue

            url = urlparse.urlparse(link)
            location = url.netloc
            params = urlparse.parse_qs(url.query)

            video_id, timestamp = None, 0
            if 'youtube.com' in location:
                video_id = params['v'][0]
            elif 'youtu.be' in location:
                video_id = url.path.lstrip('/')

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

            video = session.query(Video).filter_by(id=video_id).first()
            if video is None:
                video = Video(id=video_id, timestamp=timestamp, author_id=author_id, post_id=post_id,
                    comment_id=comment_id, posted=comment_date)
                session.add(video)
                session.commit()


if __name__ == '__main__':
    parse(1)
