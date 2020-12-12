from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from holiday_api import models
from holiday_api.routers.users import schemas
from holiday_api.routers.users.repository import (SQLAlchemyUserRepository,
                                                  UserRepository)

ROUTER = APIRouter(
    redirect_slashes=False,
    include_in_schema=False,
)


@ROUTER.post(
    '',
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user: schemas.UserInPOST,
    repo: UserRepository = Depends(SQLAlchemyUserRepository),
) -> models.User:
    registered_user: models.User = repo.create(user)
    return registered_user


@ROUTER.get(
    '/{id}',
    response_model=schemas.UserOut,
)
async def read_user(
    id_: int = Query(..., alias='id'),
    repo: UserRepository = Depends(SQLAlchemyUserRepository),
) -> models.User:
    if user := repo.get(id_):
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Item not found'
    )


@ROUTER.get(
    '',
    response_model=List[schemas.UserOut],
)
async def read_all_users(
    repo: UserRepository = Depends(SQLAlchemyUserRepository),
) -> List[models.User]:
    users: List[models.User] = repo.get_all()
    return users


@ROUTER.put(
    '/{id}',
    response_model=schemas.UserOut,
)
async def replace_user(
    user: schemas.UserInPUT,
    id_: int = Query(..., alias='id'),
    repo: UserRepository = Depends(SQLAlchemyUserRepository),
) -> models.User:
    if updated_user := repo.update(id_, user):
        return updated_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Item not found',
    )


@ROUTER.patch(
    '/{id}',
    response_model=schemas.UserOut,
)
async def update_user(
    user: schemas.UserInPATCH,
    id_: int = Query(..., alias='id'),
    repo: UserRepository = Depends(SQLAlchemyUserRepository),
) -> models.User:
    if updated_user := repo.update(id_, user):
        return updated_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Item not found',
    )


@ROUTER.patch(
    '/{id}/password',
)
async def change_user_password(
    password_change: schemas.UserPassword,
    id_: int = Query(..., alias='id'),
    repo: UserRepository = Depends(SQLAlchemyUserRepository),
) -> Response:
    is_password_changed = repo.change_password(id_, password_change)
    if is_password_changed:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Failed to change user password',
    )


@ROUTER.delete(
    '/{id}',
)
async def delete_user(
    id_: int = Query(..., alias='id'),
    repo: UserRepository = Depends(SQLAlchemyUserRepository),
) -> Response:
    is_deleted = repo.delete(id_)
    if is_deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Item not found'
    )
