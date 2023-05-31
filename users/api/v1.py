from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Body
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas as app_schemas, dependency as global_dependency
from app.core.config import settings
from .. import utils, schemas, crud, enums, responses

router = APIRouter(prefix='/api/v1/users', tags=['users'])


@router.post(
    '/token',
    response_model=app_schemas.Token,
    description='Login for access token',
    responses={
        401: responses.error_responses.get(401, {}),
    }
)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(global_dependency.get_db)
):
    user = utils.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=enums.ResponseDetail.UNAUTHORIZED.value,
            headers={'WWW-Authenticate': 'Bearer'}
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    '/',
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    description='Create new user',
    responses={
        400: responses.error_responses.get(400, {}),
        403: responses.error_responses.get(403, {}),
        409: responses.error_responses.get(409, {})
    }
)
async def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(global_dependency.get_db),
        _=Depends(utils.get_current_admin_user),
):
    db_user = crud.get_user(db, user.username)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=enums.ResponseDetail.ALREADY_EXISTS.value
        )

    return crud.create_user(db, user)


@router.get(
    '/',
    response_model=list[schemas.Barsa],
    status_code=status.HTTP_200_OK,
    description='Get all users',
    responses={}
)
async def get_barsa_users(
        db: Session = Depends(global_dependency.get_db),
        _=Depends(utils.get_current_common_user)
):
    return crud.get_all_users(db)

@router.post(
    '/{barsa_id}/mark',
    response_model=schemas.Barsa,
    status_code=status.HTTP_200_OK,
    description='Add mark to user',
    responses={}
)
async def add_mark_to_user(
        barsa_id: int,
        tag: schemas.TagCreate,
        db: Session = Depends(global_dependency.get_db),
        author=Depends(utils.get_current_common_user)
):
    return crud.add_tag_to_user(db, barsa_id, author, tag)


@router.delete(
    '/{barsa_id}/mark',
    response_model=schemas.Barsa,
    status_code=status.HTTP_200_OK,
    description='Remove mark from user',
    responses={}
)
async def add_mark_to_user(
        barsa_id: int,
        tag_id: int = Body(embed=True),
        db: Session = Depends(global_dependency.get_db),
        _=Depends(utils.get_current_common_user)
):
    return crud.remove_tag_from_user(db, barsa_id, tag_id)

@router.get(
    '/user/',
    response_model=schemas.Barsa,
    status_code=status.HTTP_200_OK,
    description='Get user info',
    responses={
        404: responses.error_responses.get(404, {})
    }
)
async def get_barsa_user(
        user_id: int,
        db: Session = Depends(global_dependency.get_db),
        current_user=Depends(utils.get_current_common_user)
):
    user = crud.get_barsa(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=enums.ResponseDetail.ALREADY_EXISTS.value
        )

    # update tags
    for tag in user.tags:
        if tag.author.id == current_user.id:
            tag.may_be_deleted = True

    return user


@router.post(
    '/user/',
    response_model=schemas.Barsa,
    status_code=status.HTTP_200_OK,
    description='Create Barsa user',
    responses={
        409: responses.error_responses.get(409, {})
    }
)
async def create_barsa_user(
        user: schemas.BarsaCreate,
        db: Session = Depends(global_dependency.get_db),
        _=Depends(utils.get_current_admin_user)
):
    db_user = crud.get_user(db, user.passport)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=enums.ResponseDetail.ALREADY_EXISTS.value
        )

    return crud.create_barsa_user(db, user)


@router.get(
    '/media/{image_path}',
    response_class=FileResponse,
    description='Get user image',
    responses={
        404: responses.error_responses.get(404, {})
    }
)
async def get_user_image(
        image_path: str,
        _: Session = Depends(global_dependency.get_db)
):
    return FileResponse(f'media/{image_path}')
