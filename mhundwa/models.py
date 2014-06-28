# -*- coding: utf-8 -*-

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref

import settings


engine = create_engine(settings.DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Post(Base):
    __tablename__ = 'posts'

    id = sa.Column(sa.Integer, primary_key=True)
    last_checked = sa.Column(sa.DateTime, nullable=True)


class Video(Base):
    __tablename__ = 'videos'
    __tableargs__ = (
        sa.UniqueConstraint('post_id', 'comment_id'),
    )

    id = sa.Column(sa.String(12), primary_key=True)
    post_id = sa.Column(sa.Integer, sa.ForeignKey('posts.id'))
    comment_id = sa.Column(sa.Integer, index=True)
    author_id = sa.Column(sa.Integer, index=True)
    was_removed = sa.Column(sa.Boolean, default=False)
    was_reposted = sa.Column(sa.Boolean, default=False)
    posted = sa.Column(sa.DateTime)
    timestamp = sa.Column(sa.Integer, default=0)

    post = relationship(Post, backref=backref('videos'))

    def __repr__(self):
        return '<Video:{}>'.format(self.id)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
