from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker, declared_attr

from app.core.config import settings

engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
