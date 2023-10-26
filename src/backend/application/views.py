from fastapi import APIRouter, Query
from loguru import logger

from .models import StatusEnum
from .schemas import ApplicationPagination

from ..core.service import CommonParameters, sort_paginate

application_router = APIRouter()


@application_router.get("", response_model=ApplicationPagination, summary="获取应用列表")
def get_applications(
        common: CommonParameters,
        category_id: int = Query(default=-1, alias="categoryId"),
        statuses: list = Query(default=[])
):
    filter_spec = []
    if category_id > 0:
        filter_spec.append({"field": "category_id", 'op': '==', 'value': category_id})
    if statuses:
        filter_spec.append({"field": "status", 'op': 'in', 'value': statuses})

    pagination = sort_paginate(model="Application", filter_spec=filter_spec, **common)
    # 修改该用户的app状态
    for app in pagination["data"]:
        if app.status == StatusEnum.published.value:
            if common["current_user"] in app.users:
                app.status = "已安装"
            else:
                app.status = "未安装"

    return pagination
