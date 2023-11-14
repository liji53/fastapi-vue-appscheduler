from typing import Optional

from .models import Project
from .schemas import ProjectCreate, ProjectUpdate


def get_by_id(*, db_session, pk: int) -> Optional[Project]:
    return db_session.query(Project).filter(Project.id == pk).one_or_none()


def create(*, db_session, project_in: ProjectCreate) -> Project:
    project = Project(**project_in.model_dump())
    db_session.add(project)
    db_session.commit()
    return project


def update(*, db_session, project: Project, project_in: ProjectUpdate) -> Project:
    db_data = project.dict()
    update_data = project_in.model_dump()

    for field in db_data:
        if field in update_data:
            setattr(project, field, update_data[field])

    db_session.commit()
    return project


def delete(*, db_session, pk: int):
    db_session.query(Project).filter(Project.id == pk).delete()
    db_session.commit()
