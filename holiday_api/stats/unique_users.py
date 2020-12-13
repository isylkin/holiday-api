from ipaddress import IPv4Address, IPv6Address
from typing import Optional, Union

from sqlalchemy.orm import Session
from prometheus_client import Counter

from holiday_api import models


UNIQUE_USERS = Counter(
    'unique_users', 'Total count of all unique users using api.'
)


class UniqueUsers:
    def __init__(self, session: Session):
        self.session = session
        self._set_initial_counter_value()

    def _set_initial_counter_value(self) -> None:
        if UNIQUE_USERS._value.get() == 0:  # pylint: disable=W0212
            total_users = self._get_total_unique_users()
            UNIQUE_USERS.inc(total_users.count)
            self.session.commit()  # type: ignore

    def _get_total_unique_users(self) -> models.TotalUniqueUsers:
        total_users = self.session.query(  # type: ignore
            models.TotalUniqueUsers).get(id=1)
        return total_users  # type: ignore

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
            total_unique_users = self._get_total_unique_users()
            total_unique_users.count = total_unique_users.count + 1
            UNIQUE_USERS.inc()
            self.session.commit()  # type: ignore
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
