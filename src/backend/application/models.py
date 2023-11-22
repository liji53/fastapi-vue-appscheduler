from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

from ..core.database import Base, DateTimeMixin


class Application(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True, index=True, comment="应用名称")
    url = Column(String(1024), nullable=False, comment="应用的地址，暂时只支持svn地址")
    banner = Column(String(256), comment="应用logo")
    description = Column(String(512), comment="描述")
    status = Column(Boolean, comment="该应用是否已经上架")

    # 应用分类
    category_id = Column(Integer, ForeignKey("application_category.id"))
    category = relationship("ApplicationCategory", backref="applications", uselist=False)


