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


class BarsaBase(BaseModel):
    name: str
    lastname: str
    passport: str
    nat: str
    gunlic: str
    crime: str


class Barsa(BarsaBase):
    id: int
    image: str | None

    class Config:
        orm_mode = True


class BarsaCreate(BarsaBase):
    image: bytes
