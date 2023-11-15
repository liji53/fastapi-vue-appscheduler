from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base, DateTimeMixin


class Project(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, comment="项目名称")
    remark = Column(String(512), comment="备注")

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", backref="projects", uselist=False)
