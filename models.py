# -*- coding: utf-8 -*-

import urlparse

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:////tmp/lepra.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Video(Base):
    __tablename__ = 'videos'

    id = sa.Column(sa.String(12), primary_key=True)
    post_id = sa.Column(sa.Integer, index=True)
    comment_id = sa.Column(sa.Integer, index=True)
    author_id = sa.Column(sa.Integer, index=True)
    was_removed = sa.Column(sa.Boolean, default=False)
    posted = sa.Column(sa.DateTime)
    timestamp = sa.Column(sa.Integer, default=0)

    def __repr__(self):
        return '<Video:{}>'.format(self.id)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
