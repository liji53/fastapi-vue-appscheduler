from sqlalchemy import Column, String, Integer
from ..core.database import Base, DateTimeMixin


class ApplicationCategory(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, index=True, comment="应用分类的名称")
    description = Column(String(512), comment="描述")
