from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..core.database import Base, DateTimeMixin


class ApplicationInstalled(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, index=True, comment="我的应用名称")
    banner = Column(String(256), comment="我的应用logo")
    description = Column(String(512), comment="描述")
    is_online = Column(Boolean, comment="应用是否已经上线")
    version = Column(String(32), comment="当前应用的版本")

    # 原应用
    application_id = Column(Integer, ForeignKey("application.id"))
    application = relationship("Application", backref="installed_applications", uselist=False)

    # 关联的用户
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", backref="installed_applications", uselist=False)
