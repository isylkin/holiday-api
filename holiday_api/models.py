# pylint: disable=too-few-public-methods

from sqlalchemy import Boolean, Column, Date, Integer, String, Text
from werkzeug.security import check_password_hash, generate_password_hash

from holiday_api.database import Base


class UniqueUser(Base):
    __tablename__ = 'unique_users'

    ip_address = Column(Text, primary_key=True)
    count = Column(Integer, default=1, nullable=False)


class TotalUniqueUsers(Base):
    __tablename__ = 'total_unique_users'

    count = Column(Integer, default=0, nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password, salt_length=16)

    def check_password(self, password: str) -> bool:
        return check_password_hash(  # type: ignore
            self.password_hash, password)


class Holiday(Base):
    __tablename__ = 'holidays'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    public = Column(Boolean, nullable=False)
    country = Column(String, nullable=False)
