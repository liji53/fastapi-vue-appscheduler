from fastapi import APIRouter
from pydantic import BaseModel

from ..auth.views import auth_router
from ..route.views import route_router


class ErrorResponse(BaseModel):
    detail: str


api_router = APIRouter(
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(route_router, prefix="/routes", tags=["route"])
