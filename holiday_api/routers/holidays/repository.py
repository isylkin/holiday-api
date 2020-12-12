from dataclasses import dataclass
from typing import List, Optional, Protocol, TypeVar, Union

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import extract

from holiday_api import models
from holiday_api.database import get_session
from holiday_api.routers.holidays import schemas

Holiday = TypeVar('Holiday')


class HolidayRepository(Protocol):
    def create(
        self,
        holiday: schemas.HolidayInPOST,
    ) -> Holiday:
        raise NotImplementedError

    def get_holiday(self, id_: int) -> Optional[Holiday]:
        raise NotImplementedError

    def get_holidays(
        self,
        filters: schemas.HolidayFilters,
    ) -> List[Holiday]:
        raise NotImplementedError

    def update(
        self,
        id_: int,
        holiday: Union[schemas.HolidayInPUT,
                       schemas.HolidayInPATCH],
    ) -> Optional[Holiday]:
        raise NotImplementedError

    def delete(self, id_: int) -> bool:
        raise NotImplementedError


@dataclass
class SQLAlchemyHolidayRepository:
    session: Session = Depends(get_session)

    def create(
        self,
        holiday: schemas.HolidayInPOST,
    ) -> models.Holiday:
        holiday_db = models.Holiday(**holiday.dict())
        self.session.add(holiday_db)
        self.session.commit()  # type: ignore
        return holiday_db

    def get_holiday(self, id_: int) -> Optional[models.Holiday]:
        holiday = self.session.query(models.Holiday).get(id_)  # type: ignore
        return holiday  # type: ignore

    def get_holidays(
        self,
        filters: schemas.HolidayFilters,
    ) -> List[models.Holiday]:
        query = self.session.query(models.Holiday)  # type: ignore
        filters = filters.dict(exclude_none=True)  # type: ignore
        for name, value in filters.items():  # type: ignore
            if name in ('year', 'month', 'day'):
                query = query.filter(
                    extract(name, models.Holiday.date) == value)
            else:
                filter_dict = {name: value}
                query = query.filter_by(**filter_dict)
        holidays = query.all()
        return holidays  # type: ignore

    def update(
        self,
        id_: int,
        holiday: Union[schemas.HolidayInPUT,
                       schemas.HolidayInPATCH],
    ) -> Optional[models.Holiday]:
        if holiday_db := self.get_holiday(id_):
            self.session.query(  # type: ignore
                models.Holiday).filter_by(id=id_)\
                .update(holiday.dict(exclude_unset=True))
            self.session.commit()  # type: ignore
        return holiday_db

    def delete(self, id_: int,) -> Optional[models.Holiday]:
        if holiday_db := self.get_holiday(id_):
            self.session.delete(holiday_db)  # type: ignore
            self.session.commit()  # type: ignore
        return holiday_db
