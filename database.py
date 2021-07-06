# -*- coding: utf-8 -*-
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import object_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import config

engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()


class MySQLSession(object):
    """ session的上下文管理器 """

    def __enter__(self):
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_value, exc_trace):
        self.session.close()
        if exc_type is not None:
            return False
        return True

