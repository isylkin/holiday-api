# pylint: disable=too-few-public-methods

import datetime
from typing import Any, Dict, Optional

import pydantic
from fastapi import HTTPException, Query, status


class HolidayFilters(pydantic.BaseModel):
    country: str = Query(..., max_length=2)
    year: int = Query(..., ge=2010, le=2200)
    month: Optional[int] = Query(None, ge=1, le=12)
    day: Optional[int] = Query(None, ge=1, le=31)
    public: Optional[bool] = Query(None)

    @pydantic.validator('day')
    def day_must_be_used_with_month(  # pylint: disable=no-self-argument,no-self-use
            cls,  # pylint: disable=unused-argument
            v: Optional[int],
            values: Dict[str, Any],
            **kwargs: Dict[str, Any],
    ) -> Optional[int]:
        if values.get('month') or v is None:
            return v
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='day must be used with month',
        )


class HolidayBase(pydantic.BaseModel):
    name: str = pydantic.Field(..., max_length=100)
    date: datetime.date
    public: bool
    country: str = pydantic.Field(..., max_length=2)

    class Config:
        schema_extra = {
            'example': {
                'name': 'Christmas Day',
                'date': '2020-12-25',
                'public': True,
                'country': 'PL',
            }
        }


class HolidayInPOST(HolidayBase):
    pass


class HolidayInPUT(HolidayBase):
    pass


class HolidayInPATCH(pydantic.BaseModel):
    name: Optional[str] = pydantic.Field(None, max_length=100)
    date: Optional[datetime.date] = None
    public: Optional[bool] = None
    country: Optional[str] = pydantic.Field(None, max_length=2)

    class Config:
        schema_extra = {
            'example': {
                'name': 'Christmas Day',
                'date': '2020-12-25',
                'public': True,
                'country': 'PL',
            }
        }


class HolidayOut(HolidayBase):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'name': 'Christmas Day',
                'date': '2020-12-25',
                'public': True,
                'country': 'PL',
                'id': 1,
            }
        }
