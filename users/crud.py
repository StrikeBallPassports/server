import datetime
import random, string

import pytz

from sqlalchemy.orm import Session

from app.core.config import settings
from . import schemas, utils, models


def get_user(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def remove_tag_from_user(db: Session, user_id: int, tag_id: int) -> models.Barsa:
    user = db.query(models.Barsa).filter(models.Barsa.id == user_id).first()

    if user is not None:
        db_tag = db.query(models.BarsaTag).filter(models.BarsaTag.id == tag_id).first()
        if db_tag is not None:
            db.delete(db_tag)
            db.commit()

    return user

def add_tag_to_user(db: Session, user_id: int, author: models.User, tag: schemas.TagCreate) -> models.Barsa:
    user = db.query(models.Barsa).filter(models.Barsa.id == user_id).first()

    if user is not None:
        db_tag = models.BarsaTag(
            value=tag.value,
            date=datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)),
            author_id=author.id,
            user_id=user_id
        )

        db.add(db_tag)
        db.commit()

    return user


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = utils.get_password_hash(user.password)

    db_user = models.User(
        username=user.username,
        is_active=user.is_active,
        password_hash=hashed_password,
        is_admin=user.is_admin,
        is_common=user.is_common
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_barsa(db: Session, user_id: int) -> models.Barsa:
    return db.query(models.Barsa).filter(models.Barsa.id == user_id).first()


def get_all_users(db: Session) -> list[models.Barsa]:
    return db.query(models.Barsa).all()


def create_barsa_user(db: Session, user: schemas.BarsaCreate) -> models.Barsa:
    image_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    file_name = f'media/user_{user.name}/{image_name}'

    with open(file_name, 'wb') as image:
        image.write(user.image)

    db_user = models.Barsa(
        name=user.name,
        lastname=user.lastname,
        passport=user.passport,
        nat=user.nat,
        gunlic=user.gunlic,
        crime=user.crime,
        image=file_name
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
