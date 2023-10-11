from typing import Annotated, Union

from fastapi import Depends, Query

from .database import DbSession

from ..auth.service import CurrentUser, CurrentRoles


# 通用查询参数
def common_parameters(
    current_user: CurrentUser,
    db_session: DbSession,
    roles: CurrentRoles,
    page: int = Query(1, gt=0, lt=2147483647),
    items_per_page: int = Query(20, alias="itemsPerPage", gt=-2, lt=2147483647),
    query_str: str = Query(None, alias="q"),
    sort_by: list[str] = Query([], alias="sortBy[]"),
    descending: list[bool] = Query([], alias="descending[]"),
):
    return {
        "db_session": db_session,
        "page": page,
        "items_per_page": items_per_page,
        "query_str": query_str,
        "sort_by": sort_by,
        "descending": descending,
        "current_user": current_user,
        "roles": roles,
    }


CommonParameters = Annotated[
    dict[str, Union[int, str, list[str], list[bool], CurrentUser, DbSession, CurrentRoles]],
    Depends(common_parameters),
]
