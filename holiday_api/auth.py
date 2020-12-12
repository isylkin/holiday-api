import secrets
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from holiday_api import models
from holiday_api.database import get_session

security = HTTPBasic()


def get_user(db: Session, username: str) -> Optional[models.User]:
    user = db.query(  # type: ignore
        models.User).filter_by(username=username).first()
    return user  # type: ignore


def authenticate(
        credentials: HTTPBasicCredentials = Depends(security),
        db: Session = Depends(get_session),
) -> None:
    if user := get_user(db, credentials.username):
        is_username_correct = secrets.compare_digest(
            credentials.username, user.username)
        is_password_correct = user.check_password(credentials.password)
        if is_username_correct and is_password_correct:
            return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect email or password',
        headers={'WWW-Authenticate': 'Basic'},
    )
