from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    is_active: bool = True
    is_admin: bool = False
    is_common: bool = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    value: str


class Tag(TagBase):
    id: int
    author: User
    date: datetime
    may_be_deleted: bool = False

    class Config:
        orm_mode = True


class TagCreate(TagBase):
    pass


class BarsaBase(BaseModel):
    name: str
    lastname: str
    passport: str
    nationality: str
    registration: str


class Barsa(BarsaBase):
    id: int
    image: str | None
    tags: list[Tag]

    class Config:
        orm_mode = True


class BarsaCreate(BarsaBase):
    image: bytes
