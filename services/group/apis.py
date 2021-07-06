# -*- coding: utf-8 -*-
from typing import Optional
from fastapi import APIRouter, Depends

from decorators import get_current_superuser, get_current_user, check_permission
from services.role.entities import get_group_list_perm, create_group_perm
from .controllers import GroupCtrl
from .schemas import GroupCreateSchema

group_router = APIRouter(prefix='/groups')


@group_router.get('', summary="部门列表")
@check_permission(get_group_list_perm)
async def group_list(
        per_page: int =10,
        page:int =1,
        name: Optional[str] = None
):
    pass


@group_router.post('', summary="创建部门", dependencies=[Depends(get_current_superuser)], name="CreateGroup")
@check_permission(create_group_perm)
async def create_group(
        create_schema: GroupCreateSchema,
):
    GroupCtrl().create_group(create_schema)
    return dict(r={}, msg='创建成功', code=0)
