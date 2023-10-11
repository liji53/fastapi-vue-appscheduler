from fastapi import APIRouter
from loguru import logger

from .schemas import RouteResponse
from .service import get_menus_by_roles

from ..core.database import DbSession
from ..core.service import CommonParameters

permission_router = APIRouter()


@permission_router.get("/routes", response_model=RouteResponse, response_model_exclude_none=True, summary="获取动态路由")
def routes(common: CommonParameters, db_session: DbSession):
    """前端动态路由"""
    logger.debug(f"获取web路由: {common['roles']}")
    return {"data": get_menus_by_roles(db_session=db_session, roles=common["roles"])}
