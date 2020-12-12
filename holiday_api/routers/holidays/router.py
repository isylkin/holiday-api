from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from holiday_api import models
from holiday_api.auth import authenticate
from holiday_api.routers.holidays import schemas
from holiday_api.routers.holidays.repository import (
    HolidayRepository, SQLAlchemyHolidayRepository)

ROUTER = APIRouter(
    redirect_slashes=False,
)


@ROUTER.post(
    '',
    response_model=schemas.HolidayOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_holiday(
    holiday: schemas.HolidayInPOST,
    _auth: Any = Depends(authenticate),
    repo: HolidayRepository = Depends(SQLAlchemyHolidayRepository),
) -> models.Holiday:
    created_holiday: models.Holiday = repo.create(holiday)
    return created_holiday


@ROUTER.get(
    '/{id}',
    response_model=schemas.HolidayOut,
    responses={
        404: {'description': 'Item not found'},
    },
)
async def read_holiday(
    id_: int = Query(..., alias='id'),
    _auth: Any = Depends(authenticate),
    repo: HolidayRepository = Depends(SQLAlchemyHolidayRepository),
) -> models.Holiday:
    if holiday := repo.get_holiday(id_):
        return holiday
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Item not found'
    )


@ROUTER.get(
    '',
    response_model=List[schemas.HolidayOut],
)
async def read_holidays(
    filters: schemas.HolidayFilters = Depends(),
    repo: HolidayRepository = Depends(SQLAlchemyHolidayRepository),
) -> List[models.Holiday]:
    holidays = repo.get_holidays(filters)  # type: ignore
    return holidays


@ROUTER.put(
    '/{id}',
    response_model=schemas.HolidayOut,
    responses={
        404: {'description': 'Item not found'},
    },
)
async def replace_holiday(
    holiday: schemas.HolidayInPUT,
    id_: int = Query(..., alias='id'),
    _auth: Any = Depends(authenticate),
    repo: HolidayRepository = Depends(SQLAlchemyHolidayRepository),
) -> models.Holiday:
    if updated_holiday := repo.update(id_, holiday):
        return updated_holiday
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found",
    )


@ROUTER.patch(
    '/{id}',
    response_model=schemas.HolidayOut,
    responses={
        404: {'description': 'Item not found'},
    },
)
async def update_holiday(
    holiday: schemas.HolidayInPATCH,
    id_: int = Query(..., alias='id'),
    _auth: Any = Depends(authenticate),
    repo: HolidayRepository = Depends(SQLAlchemyHolidayRepository),
) -> models.Holiday:
    if updated_holiday := repo.update(id_, holiday):
        return updated_holiday
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found",
    )


@ROUTER.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {'description': 'Item not found'},
    },
)
async def delete_holiday(
    id_: int = Query(..., alias='id'),
    _auth: Any = Depends(authenticate),
    repo: HolidayRepository = Depends(SQLAlchemyHolidayRepository),
) -> Response:
    is_deleted = repo.delete(id_)
    if is_deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Item not found'
    )
