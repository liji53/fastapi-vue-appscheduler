from typing import Optional, List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ..auth.views import auth_router


# 定义错误的model
class ErrorMsg(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMsg]]


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
