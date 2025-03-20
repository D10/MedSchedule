import datetime as dt

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):  # type:ignore
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=dt.datetime.now)

    def as_dict(self):
        return self.__dict__
