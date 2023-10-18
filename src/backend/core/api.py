from fastapi import APIRouter
from pydantic import BaseModel

from ..auth.views import auth_router
from ..permission.views import permission_router
from ..application.views import application_router


class ErrorResponse(BaseModel):
    detail: str


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
api_router.include_router(permission_router, prefix="/permission", tags=["permission"])
api_router.include_router(application_router, prefix="/apps", tags=["app"])
