from datetime import datetime, timedelta

import bcrypt
from jose import jwt
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from ..core.config import JWT_EXP, JWT_SECRET, JWT_ALG
from ..core.database import Base
from ..core.models import DateTimeMixin


class User(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True)
    email = Column(String(128), unique=True)
    password = Column(String(128), nullable=False)

    # 当前用户所有已安装的应用
    # applications = relationship("application", backref="user")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), bytes(self.password))

    @property
    def token(self):
        now = datetime.utcnow()
        exp = (now + timedelta(seconds=JWT_EXP)).timestamp()
        data = {
            "exp": exp,
            "username": self.username,
        }
        return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALG)

