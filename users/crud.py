import random, string

from sqlalchemy.orm import Session

from . import schemas, utils, models


def get_user(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


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
