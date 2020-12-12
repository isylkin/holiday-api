# pylint: disable=too-few-public-methods

from typing import Optional

import pydantic
import pydantic.types


class UserBase(pydantic.BaseModel):
    first_name: str
    last_name: str
    username: str
    password: pydantic.types.SecretStr


class UserInPOST(UserBase):
    pass


class UserInPUT(UserBase):
    pass


class UserInPATCH(pydantic.BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[pydantic.types.SecretStr] = None


class UserOut(pydantic.BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str

    class Config:
        orm_mode = True


class UserPassword(pydantic.BaseModel):
    current_password: pydantic.types.SecretStr
    new_password: pydantic.types.SecretStr
