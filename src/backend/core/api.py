from fastapi import APIRouter
from pydantic import BaseModel

from ..auth.views import auth_router, user_router
from ..permission.views import permission_router, role_router
from ..application.views import application_router
from ..application_category.views import app_category_router
from ..application_installed.views import installed_app_router
from ..project.views import project_router
from ..task.views import task_router
from ..sys_resource.views import sys_resource_router


class ErrorResponse(BaseModel):
    detail: list[dict[str, str]]


api_router = APIRouter(
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(user_router, prefix="/users", tags=["user"])
api_router.include_router(permission_router, prefix="/permission", tags=["permission"])
api_router.include_router(role_router, prefix="/roles", tags=["role"])
api_router.include_router(application_router, prefix="/apps", tags=["app"])
api_router.include_router(app_category_router, prefix="/app_categories", tags=["app_category"])
api_router.include_router(installed_app_router, prefix="/installed_apps", tags=["my_app"])
api_router.include_router(project_router, prefix="/projects", tags=["project"])
api_router.include_router(task_router, prefix="/tasks", tags=["task"])
api_router.include_router(sys_resource_router, prefix="/sys_resources", tags=["sys_resource"])
