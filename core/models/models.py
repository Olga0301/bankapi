from sqlalchemy import Column, VARCHAR, TEXT, TIMESTAMP, INT, ForeignKey
from sqlalchemy.sql.functions import now
from .base import Base


class User(Base):
    email = Column(VARCHAR(128), nullable=False, unique=True)
    username = Column(VARCHAR(128), nullable=False, unique=True)
    hashed_password = Column(VARCHAR(512), nullable=False)

    def __repr__(self):
        return self.username


class Post(Base):
    title = Column(VARCHAR(128), nullable=False, unique=True)
    body = Column(TEXT, nullable=False)
    date_create = Column(TIMESTAMP, default=now)
    author_id = Column(INT, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return self.title
