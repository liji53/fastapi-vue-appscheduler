from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from ..core.database import Base, DateTimeMixin


class Task(Base, DateTimeMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, comment="任务名称")
    remark = Column(String(512), comment="任务备注")
    status = Column(Boolean, comment="任务是否使能")
    cron = Column(String(16), comment="定时cron表达式")

    # 所属项目
    project_id = Column(Integer, ForeignKey("project.id"))
    project = relationship("Project", backref="tasks", uselist=False)

    # 安装的应用
    app_id = Column(Integer, ForeignKey("application_installed.id"))
    application = relationship("ApplicationInstalled", backref="tasks", uselist=False)

    def __repr__(self) -> str:
        return f"<{self.name} - {self.cron}>"
