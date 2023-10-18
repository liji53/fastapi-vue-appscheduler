import json

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from loguru import logger

from .schemas import ApplicationPagination

from ..core.database import DbSession
from ..core.service import CommonParameters, sort_paginate

application_router = APIRouter()


@application_router.get("", response_model=ApplicationPagination, summary="获取所有的应用")
def get_applications(common: CommonParameters):
    pagination = sort_paginate(model="application", **common)
    logger.debug(pagination)
    return json.loads(ApplicationPagination(**pagination).model_dump_json())
