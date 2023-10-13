from typing import Annotated, Optional
import re

from fastapi import Depends
from fastapi.requests import Request
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from loguru import logger

from .config import DATABASE_URI, DATABASE_ENGINE_POOL_SIZE, DATABASE_ENGINE_MAX_OVERFLOW

engine = create_engine(
    DATABASE_URI,
    pool_size=DATABASE_ENGINE_POOL_SIZE,
    max_overflow=DATABASE_ENGINE_MAX_OVERFLOW,
)
SessionLocal = sessionmaker(bind=engine)


class CustomBase:
    __repr_attrs__ = []
    __repr_max_length__ = 15

    @declared_attr
    def __tablename__(self):
        names = re.split("(?=[A-Z])", self.__name__)
        return "_".join([x.lower() for x in names if x])

    def dict(self, exclude: Optional[list[str]] = None):
        """model 转 dic"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if not exclude or c.name not in exclude}

    @property
    def _id_str(self):
        ids = inspect(self).identity
        if ids:
            return "-".join([str(x) for x in ids]) if len(ids) > 1 else str(ids[0])
        else:
            return "None"

    @property
    def _repr_attrs_str(self):
        max_length = self.__repr_max_length__

        values = []
        single = len(self.__repr_attrs__) == 1
        for key in self.__repr_attrs__:
            if not hasattr(self, key):
                raise KeyError(
                    "{} has incorrect attribute '{}' in "
                    "__repr__attrs__".format(self.__class__, key)
                )
            value = getattr(self, key)
            wrap_in_quote = isinstance(value, str)

            value = str(value)
            if len(value) > max_length:
                value = value[:max_length] + "..."

            if wrap_in_quote:
                value = "'{}'".format(value)
            values.append(value if single else "{}:{}".format(key, value))

        return " ".join(values)

    def __repr__(self):
        # 拼接 id like '#123'
        id_str = ("#" + self._id_str) if self._id_str else ""
        # 拼接 model名, id, repr_attrs
        return "<{} {}{}>".format(
            self.__class__.__name__,
            id_str,
            " " + self._repr_attrs_str if self._repr_attrs_str else "",
        )


Base = declarative_base(cls=CustomBase)


def get_db(request: Request):
    # 在middleware中创建
    return request.state.db


DbSession = Annotated[Session, Depends(get_db)]
