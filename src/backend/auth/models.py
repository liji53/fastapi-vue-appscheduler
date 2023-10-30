from datetime import datetime, timedelta

import bcrypt
from jose import jwt
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table, LargeBinary
from sqlalchemy.orm import relationship

from ..core.config import JWT_EXP, JWT_SECRET, JWT_ALG
from ..core.database import Base, DateTimeMixin
from ..application.models import UserApplication


# 中间表
UserRole = Table(
    "users_roles",
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('role_id', Integer, ForeignKey('role.id'))
)


class User(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True, comment="用户名")
    password = Column(String(128), nullable=False, comment="密码")
    avatar = Column(String(256), comment="用户头像")
    email = Column(String(128), unique=True, comment="邮箱")
    phone = Column(String(32), unique=True, comment="手机号")
    status = Column(Boolean, default=True, comment="是否启用")
    remark = Column(String(512), comment="备注")

    # 当前用户的角色
    roles = relationship("Role", secondary=UserRole, back_populates="users")
    # 当前用户所有已安装的应用
    installed_applications = relationship("Application", secondary=UserApplication, back_populates="users")

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
