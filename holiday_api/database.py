from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import holiday_api.config as config

engine = create_engine(config.DATABASE_URL, connect_args={
                       'check_same_thread': False}, echo=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session() -> None:  # type: ignore
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()  # pylint: disable=no-member
