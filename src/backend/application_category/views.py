
from fastapi import APIRouter

from .schemas import ApplicationCategoryPagination

from ..core.service import CommonParameters, sort_paginate


app_category_router = APIRouter()


@app_category_router.get("", response_model=ApplicationCategoryPagination, summary="获取应用类别列表")
def get_app_categories(common: CommonParameters):
    return sort_paginate(model="ApplicationCategory", **common)
