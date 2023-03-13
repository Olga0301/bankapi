from sqlalchemy import Column, VARCHAR

from .base import Base


class User(Base):
    email = Column(VARCHAR(128), nullable=False, unique=True)
    username = Column(VARCHAR(128), nullable=False, unique=True)
    hashed_password = Column(VARCHAR(512), nullable=False)

    def __repr__(self):
        return self.username
