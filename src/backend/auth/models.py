from datetime import datetime, timedelta

import bcrypt
from jose import jwt
from loguru import logger
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from ..core.config import JWT_EXP, JWT_SECRET, JWT_ALG
from ..core.database import Base
from ..core.models import DateTimeMixin
from ..permission.models import users_roles


class User(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True)
    email = Column(String(128), unique=True)
    password = Column(String(128), nullable=False)

    roles = relationship("Role", secondary=users_roles, back_populates="users")
    # 当前用户所有已安装的应用
    # applications = relationship("application", backref="user")

    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    @property
    def token(self):
        now = datetime.utcnow()
        exp = (now + timedelta(seconds=JWT_EXP)).timestamp()
        data = {
            "exp": exp,
            "username": self.username,
        }
        return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALG)

    @property
    def expired(self):
        now = datetime.utcnow()
        exp = (now + timedelta(seconds=JWT_EXP)).strftime("%Y/%m/%d %H:%M:%S")
        return exp
