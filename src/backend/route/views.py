from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from loguru import logger

from .schemas import RouteResponse

from ..core.database import DbSession

route_router = APIRouter()


@route_router.get("", response_model=RouteResponse, response_model_exclude_none=True)
def routes(db_session: DbSession):
    """前端动态路由"""
    return {"data": [
        {
            "path": "/permission",
            "name": None,
            "meta": {
                "title": "权限管理",
                "icon": "lollipop",
                "rank": 10,
                "roles": None,
                "auths": None,
            },
            "children": [
                {
                    "path": "/permission/page/index",
                    "name": "PermissionPage",
                    "meta": {
                        "title": "页面权限",
                        "icon": None,
                        "rank": None,
                        "roles": ["admin", "common"],
                        "auths": None,
                    },
                    "children": None
                },
                {
                  "path": "/permission/button/index",
                  "name": "PermissionButton",
                  "meta": {
                    "title": "按钮权限",
                    "icon": None,
                    "rank": None,
                    "roles": ["admin", "common"],
                    "auths": ["btn_add", "btn_edit", "btn_delete"]
                  },
                  "children": None
                }
            ]
        }
    ]}
