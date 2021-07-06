# -*- coding: utf-8 -*-
from typing import Optional

from fastapi import APIRouter, Depends

from decorators import check_permission, get_current_active_user
from .controllers import RoleCtrl
from .entities import (
    get_role_list_perm,
    create_role_perm,
)
from .schemas import (
    RolePaginateSchema,
    RoleCreateSchema,
)

role_router = APIRouter(prefix='/roles')


@role_router.get('', summary="角色列表")
@check_permission(get_role_list_perm)
async def role_list(
        name: Optional[str] = None,
        per_page: int = 10,
        page: int = 1,
        user=Depends(get_current_active_user)
):
    schema = RolePaginateSchema(name=name, per_page=per_page, page=page)
    pagination = RoleCtrl().paginate_roles(schema)
    result = {
        "roles": pagination.items,
        "per_page": pagination.per_page,
        "page": pagination.page,
        "total_rows": pagination.total,
        "total_pages": pagination.pages
    }
    return dict(r=result, msg="", code=0)


@role_router.get('/permissions', summary="所有权限列表")
@check_permission(get_role_list_perm)  # 能查看角色就能查看权限
async def permissions_list(user=Depends(get_current_active_user)):
    permissions = RoleCtrl().retrieve_modules_with_permissions()
    return dict(r={'modules': permissions}, msg="", code=0)


@role_router.post('', summary="添加角色")
@check_permission(create_role_perm)
async def create_role(
        create_schema: RoleCreateSchema,
        user=Depends(get_current_active_user)
):
    RoleCtrl().create_role(create_schema)
    return dict(r={}, msg="添加成功", code=0)
