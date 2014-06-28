# -*- coding: utf-8 -*-

from __future__ import absolute_import

import html5lib

from helpers import get
from models import Post, session


def parse():
    """Парсинг индексной страницы и поиск новых постов"""

    content = get('https://auto.leprosorium.ru/')
    doc = html5lib.parse(content, treebuilder='lxml', namespaceHTMLElements=False)

    posts = doc.xpath('//div[@class="b-posts_holder"]/div[contains(@class, "post")]')
    for post in posts:
        if not post.xpath(u'.//div[@class="dti"]/*[text()[contains(.,"Странного хобби пост №")]]'):
            continue

        post_id = int(post.attrib['id'].replace('p', ''))
        instance = session.query(Post).filter_by(id=post_id).first()
        if instance is None:
            instance = Post(id=post_id)
            session.add(instance)
            session.commit()
