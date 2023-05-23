from sqlalchemy import Column, Boolean, String

from app.database import Base


class Barsa(Base):
    name = Column(String)
    lastname = Column(String)
    passport = Column(String, index=True)
    nat = Column(String)
    gunlic = Column(String, default='нет')
    crime = Column(String, default='нет')
    image = Column(String, nullable=True, default=None)


class User(Base):
    username = Column(String)
    password_hash = Column(String)
    is_active = Column(Boolean)
    is_admin = Column(Boolean)
    is_common = Column(Boolean)
