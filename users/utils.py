from datetime import timedelta, datetime

from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBasic
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.dependency import get_db
from . import schemas, crud, enums, models
from app import schemas as app_schemas
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/token")
security = HTTPBasic()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str) -> models.User | bool:
    user = crud.get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = app_schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = crud.get_user(db, username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


async def get_current_admin_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_admin or not current_user.is_active:
        raise HTTPException(status_code=403, detail=enums.ResponseDetail.FORBIDDEN.value)
    return current_user


async def get_current_common_user(
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> schemas.User:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=enums.ResponseDetail.UNAUTHORIZED.value,
        headers={"WWW-Authenticate": "Basic"},
    )

    user = crud.get_user(db, current_user.username)

    if user is None:
        raise exception

    if not current_user.password_hash == user.password_hash:
        raise exception

    return schemas.User(**jsonable_encoder(user))
