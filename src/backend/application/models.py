from enum import Enum

from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

from ..core.database import Base, DateTimeMixin


UserApplication = Table(
    'users_applications',
    Base.metadata,
    Column('user_id', Integer, ForeignKey("user.id")),
    Column('application_id', Integer, ForeignKey("application.id"))
)


# 已安装、已上线 状态 通过业务判断
class StatusEnum(Enum):
    deprecated = '废弃'
    published = '已发布'


class Application(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, comment="应用名称")
    banner = Column(String(128), comment="应用图标")
    description = Column(String(512), comment="备注")
    status = Column(String(16), default=StatusEnum.published)

    # 应用分类
    category_id = Column(Integer, ForeignKey("application_category.id"))
    category = relationship("ApplicationCategory", backref="applications", uselist=False)

    # 该应用被哪些用户安装了
    users = relationship("User", secondary=UserApplication, back_populates="installed_applications")

