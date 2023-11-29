import uuid

from database import Base

from .base_entity import BaseEntity
from sqlalchemy import Column, String, Uuid, ForeignKey, Boolean, SmallInteger
from sqlalchemy.orm import relationship

from .user import User


class Book(Base, BaseEntity):
    __tablename__ = 'books'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    is_published = Column(Boolean, default=False)
    rating = Column(SmallInteger, default=0)
    author_id = Column(Uuid, ForeignKey("authors.id"), nullable=False,)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=False,)
    author = relationship("Author")
    owner = relationship(User)
