from typing import Union, Optional

from fastapi import APIRouter, Query, HTTPException
from loguru import logger

from .schemas import RouteResponse, RolePagination, RoleRead, RoleCreate, RoleUpdate, RoleStatusUpdate, \
    RoleMenuUpdate, RoleMenuRead
from .service import get_by_code, get_by_id, create, update, delete

from ..core.database import DbSession
from ..core.service import CommonParameters, sort_paginate, CurrentRoles
from ..core.schemas import PrimaryKey

permission_router = APIRouter()
role_router = APIRouter()


def recursion_role_menu(menu, result: list) -> dict:
    tmp_menu = {
        "id": menu.id,
        "title": menu.meta.title
    }
    if menu.parent:
        parent_menu = recursion_role_menu(menu.parent, result)
        if parent_menu.__contains__("children"):
            if parent_menu.__contains__("children"):
                for child in parent_menu['children']:  # 已经添加过该节点了
                    if child['id'] == menu.id:
                        return tmp_menu
            parent_menu["children"].append(tmp_menu)
        else:
            parent_menu["children"] = [tmp_menu]
    else:
        for menu_item in result:
            if menu_item["id"] == menu.id:   # 之前已经添加过该节点了
                return menu_item
        result.append(tmp_menu)
        return tmp_menu


def recursion_menu(menu, result: list) -> Optional[dict]:
    """基于子节点，递归查找父节点，并生成路由树"""
    tmp_menu = {
        "path": menu.path,
        "name": menu.name,
        "meta": menu.meta.dict()
        # "meta": menu.meta.dict(exclude=["id", "menu_id", "created_at", "updated_at"])
    }
    if menu.parent:
        parent_menu = recursion_menu(menu.parent, result)
        if parent_menu.__contains__("children"):
            for child in parent_menu['children']:  # 已经添加过该节点了
                if child['path'] == menu.path:
                    return tmp_menu

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
def routes(current_roles: CurrentRoles):
    """前端动态路由"""
    logger.debug(f"获取web路由, 当前角色为: {current_roles}")
    menus = []
    for role in current_roles:
        sorted_menus = sorted(role.menus, key=lambda x: x.meta.rank)
        for menu in sorted_menus:
            recursion_menu(menu, menus)
    # 写死，后续优化
    if list(filter(lambda x: x.code == "admin", current_roles)):
        for menu in menus:
            if menu["path"] != "/app":
                continue
            for child in menu["children"]:
                if child["name"] == "Store":
                    child["meta"]["auths"] = ["btn_add", "btn_update", "btn_delete"]
    return {"data": menus}


@role_router.get("", response_model=RolePagination, summary="获取角色列表")
def get_roles(common:  CommonParameters,
              code: str = None,
              active: Optional[bool] = Query(default=None, alias="status")):
    """获取角色列表"""
    filter_spec = []
    if code:
        filter_spec.append({"field": "code", 'op': '==', 'value': code})
    if active is not None:
        filter_spec.append({"field": "status", 'op': '==', 'value': active})

    return sort_paginate("Role", filter_spec=filter_spec, **common)


@role_router.post("", response_model=RoleRead, summary="创建角色")
def create_role(role_in: RoleCreate, db_session: DbSession):
    """创建角色"""
    # todo: 权限控制
    role = get_by_code(db_session=db_session, code=role_in.code)
    if role:
        raise HTTPException(422, detail=[{"msg": "创建角色失败，该角色已经存在!"}])
    try:
        role = create(db_session=db_session, role_in=role_in)
    except Exception as e:
        logger.warning(f"创建角色失败，原因：{e}")
        raise HTTPException(500, detail=[{"msg": "创建角色失败！"}])
    return role


@role_router.put("/{role_id}", response_model=RoleRead, summary="更新角色信息, 更新角色状态, 更新角色的菜单权限")
def update_role(role_id: PrimaryKey,
                role_in: Union[RoleUpdate, RoleStatusUpdate, RoleMenuUpdate],
                db_session: DbSession):
    """更新角色"""
    # todo: 权限控制
    role = get_by_id(db_session=db_session, role_id=role_id)
    if not role:
        raise HTTPException(404, detail=[{"msg": "更新角色失败，该角色不存在！"}])
    try:
        role = update(db_session=db_session, role=role, role_in=role_in)
    except Exception as e:
        logger.warning(f"更新角色失败，原因：{e}")
        raise HTTPException(500, detail=[{"msg": "更新角色失败！"}])
    return role


@role_router.delete("/{role_id}", response_model=None, summary="删除角色")
def delete_role(role_id: PrimaryKey, db_session: DbSession):
    """删除角色"""
    # todo: 权限控制
    try:
        delete(db_session=db_session, role_id=role_id)
    except Exception as e:
        logger.warning(f"删除角色失败，原因: {e}")
        raise HTTPException(500, detail=[{"msg": f"角色删除失败！"}])


@role_router.get("/{role_id}/menus", response_model=RoleMenuRead, summary="获取指定角色的菜单")
def get_role_menus(role_id: int, db_session: DbSession, current_roles: CurrentRoles):
    """获取指定角色的菜单"""
    role = get_by_id(db_session=db_session, role_id=role_id)
    if not role:
        raise HTTPException(404, detail=[{"msg": "该角色不存在！"}])

    # 当前用户所有角色的菜单
    menus = []
    for current_role in current_roles:
        for menu in current_role.menus:
            recursion_role_menu(menu, menus)

    return {
        "menus": menus,
        "activedMenus": [menu.id for menu in role.menus]  # 只需叶子节点的id
    }


