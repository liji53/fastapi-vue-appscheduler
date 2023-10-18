from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

from ..core.database import Base, DateTimeMixin


UserApplication = Table(
    'users_applications',
    Base.metadata,
    Column('user_id', Integer, ForeignKey("user.id")),
    Column('application_id', Integer, ForeignKey("application.id"))
)


class Application(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, comment="应用名称")
    banner = Column(String(128), comment="应用图标")
    description = Column(String(512), comment="备注")

    # 应用类型
    # application_type = relationship("ApplicationType", backref="applications")
    # application_type_id = Column(Integer, ForeignKey("application_type.id"))

    # 该应用被哪些用户安装了
    users = relationship("User", secondary=UserApplication, back_populates="installed_applications")

