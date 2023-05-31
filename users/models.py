from sqlalchemy import Column, Boolean, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class Barsa(Base):
    name = Column(String)
    lastname = Column(String)
    passport = Column(String, index=True)
    nat = Column(String)
    image = Column(String, nullable=True, default=None)


class User(Base):
    username = Column(String)
    password_hash = Column(String)
    is_active = Column(Boolean)
    is_admin = Column(Boolean)
    is_common = Column(Boolean)


class BarsaTag(Base):
    value = Column(String)
    date = Column(DateTime)

    user_id = Column(Integer, ForeignKey(Barsa.id))
    author_id = Column(Integer, ForeignKey(User.id))

    author = relationship(Barsa)
    user = relationship(User, cascade='all, delete', back_populates='tags')
