from fastapi import APIRouter
from loguru import logger

from .schemas import RouteResponse, MenuItem

from ..core.database import DbSession
from ..core.service import CommonParameters

permission_router = APIRouter()


def recursion_menu(menu, result: list) -> dict:
    tmp_menu = {
        "path": menu.path,
        "name": menu.name,
        "meta": menu.meta.dict()
        # "meta": menu.meta.dict(exclude=["id", "menu_id", "created_at", "updated_at"])
    }
    if menu.parent:
        parent_menu = recursion_menu(menu.parent, result)
        if parent_menu.__contains__("children"):
            parent_menu["children"].append(tmp_menu)
        else:
            parent_menu["children"] = [tmp_menu]
        return tmp_menu
    else:
        for menu_item in result:
            if menu_item["path"] == menu.path:   # 之前已经添加过该节点了
                return menu_item
        result.append(tmp_menu)
        return tmp_menu


@permission_router.get("/routes", response_model=RouteResponse, response_model_exclude_none=True, summary="获取动态路由")
def routes(common: CommonParameters, db_session: DbSession):
    """前端动态路由"""
    logger.debug(f"获取web路由, 当前角色为: {common['roles']}")
    menus = []
    for role in common['roles']:
        for menu in role.menus:
            recursion_menu(menu, menus)

    return {"data": menus}
