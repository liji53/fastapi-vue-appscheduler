from datetime import datetime, timedelta

import bcrypt
from jose import jwt
from sqlalchemy import DateTime, Column, String, Integer, LargeBinary
from sqlalchemy.orm import relationship

from ..core.config import JWT_EXP, JWT_SECRET, JWT_ALG
from ..core.database import Base
from ..core.models import DateTimeMixin


class User(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(LargeBinary, nullable=False)

    # 当前用户所有已安装的应用
    # applications = relationship("application", backref="user")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    @property
    def token(self):
        now = datetime.utcnow()
        exp = (now + timedelta(seconds=JWT_EXP)).timestamp()
        data = {
            "exp": exp,
            "username": self.username,
        }
        return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALG)

    # def get_organization_role(self, organization_slug: OrganizationSlug):
    #     """Gets the user's role for a given organization slug."""
    #     for o in self.organizations:
    #         if o.organization.slug == organization_slug:
    #             return o.role
