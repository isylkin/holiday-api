from dataclasses import dataclass
from typing import List, Optional, Protocol, TypeVar, Union

from fastapi import Depends
from sqlalchemy.orm import Session

from holiday_api import models
from holiday_api.database import get_session
from holiday_api.routers.users import schemas

User = TypeVar('User')


class UserRepository(Protocol):
    def create(self, user: schemas.UserInPOST) -> User:
        raise NotImplementedError

    def get(self, id_: int) -> Optional[User]:
        raise NotImplementedError

    def get_all(self) -> List[User]:
        raise NotImplementedError

    def update(
        self,
        id_: int,
        user: Union[schemas.UserInPUT,
                    schemas.UserInPATCH],
    ) -> Optional[User]:
        raise NotImplementedError

    def change_password(
        self,
        id_: int,
        password_change: schemas.UserPassword,
    ) -> bool:
        raise NotImplementedError

    def delete(self, id_: int) -> bool:
        raise NotImplementedError


@dataclass
class SQLAlchemyUserRepository:
    session: Session = Depends(get_session)

    def create(
        self,
        user: schemas.UserInPOST
    ) -> models.User:
        user_db = models.User(**user.dict(exclude={'password'}))
        user_db.set_password(user.password.get_secret_value())
        self.session.add(user_db)
        self.session.commit()  # type: ignore
        return user_db

    def get(self, id_: int) -> Optional[models.User]:
        user = self.session.query(models.User).get(id_)  # type: ignore
        return user  # type: ignore

    def get_all(self) -> List[models.User]:
        users = self.session.query(models.User).all()  # type: ignore
        return users  # type: ignore

    def update(
        self,
        id_: int,
        user: Union[schemas.UserInPUT,
                    schemas.UserInPATCH],
    ) -> Optional[models.User]:
        if user_db := self.get(id_):
            user_dict = user.dict(exclude_unset=True, exclude={'password'})
            self.session.query(  # type: ignore
                models.User).filter(models.User.id == id_).\
                update(user_dict)
            if user.password:
                user_db.set_password(user.password.get_secret_value())
            self.session.commit()  # type: ignore
        return user_db

    def change_password(
        self,
        id_: int,
        password_change: schemas.UserPassword,
    ) -> bool:
        if user := self.get(id_):
            if user.check_password(password_change.current_password.get_secret_value()):
                user.set_password(
                    password_change.new_password.get_secret_value())
                self.session.commit()  # type: ignore
                return True
        return False

    def delete(self, id_: int,) -> Optional[models.User]:
        if user_db := self.get(id_):
            self.session.delete(user_db)  # type: ignore
            self.session.commit()  # type: ignore
        return user_db
