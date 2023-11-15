from typing import Annotated, Union

from fastapi import Depends, Query, HTTPException
from loguru import logger
from sqlalchemy_filters import apply_pagination, apply_sort, apply_filters

from .database import DbSession, get_model_by_table_name

from ..auth.service import CurrentUser, CurrentRoles, User, Role


# 通用查询参数
def common_parameters(
    current_user: CurrentUser,
    db_session: DbSession,
    roles: CurrentRoles,
    page: int = Query(1, gt=0, lt=2147483647),
    items_per_page: int = Query(None, alias="itemsPerPage", gt=-2, lt=2147483647),
    query_name: str = Query(None, alias="name"),
    sort_by: list[str] = Query([], alias="sortBy[]"),
    descending: list[bool] = Query([], alias="descending[]"),
):
    return {
        "db_session": db_session,
        "page": page,
        "items_per_page": items_per_page,
        "query_name": query_name,
        "sort_by": sort_by,
        "descending": descending,
        "current_user": current_user,
        "roles": roles,
    }


CommonParameters = Annotated[
    dict[str, Union[str, int, list[str], list[bool], CurrentUser, DbSession, CurrentRoles]],
    Depends(common_parameters),
]


def sort_paginate(
    model,
    db_session,
    filter_spec: list[dict] = None,
    page: int = 1,
    items_per_page: int = None,
    query_name: str = None,
    sort_by: list[str] = None,
    descending: list[bool] = None,
    current_user: User = None,
    roles: list[Role] = None,
):
    """用于分页、排序 的通用函数"""
    model_cls = get_model_by_table_name(model)
    try:
        query = db_session.query(model_cls)
        if query_name:
            # query = search(query_str=query_str, query=query, model=model, sort=sort)
            name_filter = [{"field": "name", 'op': 'like', 'value': f"%{query_name}%"}]
            query = apply_filters(query, filter_spec=name_filter)

        if model in ["Project", "ApplicationInstalled"]:
            # user外键
            user_filter = [{"field": "user_id", 'op': '==', 'value': f"{current_user.id}"}]
            query = apply_filters(query, filter_spec=user_filter)

        if filter_spec:
            query = apply_filters(query, filter_spec=filter_spec)

        if sort_by:
            sort_spec = _create_sort_spec(model, sort_by, descending)
            logger.debug(f"排序内容: {sort_spec}")
            query = apply_sort(query, sort_spec)

    except Exception as e:
        logger.debug(e)
        raise HTTPException(status_code=500, detail=[{"msg": "排序功能错误!"}])

    if items_per_page == -1:
        items_per_page = None

    try:
        query, pagination = apply_pagination(query, page_number=page, page_size=items_per_page)
    except Exception as e:
        logger.debug(e)
        raise HTTPException(status_code=500, detail=[{"msg": "分页功能错误!"}])

    return {
        "data": query.all(),
        "total": pagination.total_results,
    }


def _create_sort_spec(model, sort_by: list[str], descending: list[bool]):
    sort_spec = []
    if sort_by and descending:
        for field, direction in zip(sort_by, descending):
            direction = "desc" if direction else "asc"

            sort_spec.append({"model": model, "field": field, "direction": direction})

    return sort_spec
