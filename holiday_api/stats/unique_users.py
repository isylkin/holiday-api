from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address
from typing import Optional, Union

from sqlalchemy.orm import Session
from prometheus_client import Counter

from holiday_api import models


UNIQUE_USERS = Counter(
    'unique_users', 'Total count of all unique users using api.'
)


@dataclass
class UniqueUsers:
    session: Session

    def update(
        self,
        ip_address: Union[IPv4Address, IPv6Address],
    ) -> Optional[models.UniqueUser]:
        if ip_address.is_loopback:
            return None
        if unique_user := self.get(ip_address):
            unique_user.count = unique_user.count + 1
            self.session.commit()  # type: ignore
        else:
            unique_user = self.create(ip_address)
            UNIQUE_USERS.inc()
        return unique_user

    def create(
        self,
        ip_address: Union[IPv4Address, IPv6Address],
    ) -> models.UniqueUser:
        unique_user = models.UniqueUser(ip_address=ip_address.exploded)
        self.session.add(unique_user)
        self.session.commit()  # type: ignore
        return unique_user

    def get(
        self,
        ip_address: Union[IPv4Address, IPv6Address],
    ) -> Optional[models.UniqueUser]:
        unique_user = self.session.query(  # type: ignore
            models.UniqueUser).filter_by(ip_address=ip_address.exploded).first()
        return unique_user  # type: ignore

    def delete(
        self,
        ip_address: Union[IPv4Address, IPv6Address],
    ) -> Optional[models.UniqueUser]:
        if unique_user := self.get(ip_address):
            self.session.delete(unique_user)  # type: ignore
            self.session.commit()  # type: ignore
        return unique_user
