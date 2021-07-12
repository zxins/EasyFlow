# -*- coding: utf-8 -*-
from typing import Optional
from fastapi import APIRouter, Depends

from decorators import get_current_superuser, get_current_active_user, check_permission
from services.role.entities import get_group_list_perm, create_group_perm, update_group_perm
from .controllers import GroupCtrl
from .schemas import GroupCreateSchema, GroupUpdateSchema

group_router = APIRouter(prefix='/groups')


@group_router.get('', summary="部门列表")
@check_permission(get_group_list_perm)
async def group_list(
        name: Optional[str] = None,
        user=Depends(get_current_active_user)
):
    groups = GroupCtrl().get_group_sections(name)
    return dict(r={'groups': groups}, msg="", code=0)


@group_router.post('', summary="创建部门",  name="CreateGroup")
@check_permission(create_group_perm)
async def create_group(
        create_schema: GroupCreateSchema,
        user=Depends(get_current_active_user)

):
    GroupCtrl().create_group(create_schema)
    return dict(r={}, msg='创建成功', code=0)


@group_router.put('/{group_id}', summary="更新部门", name="UpdateGroup")
@check_permission(update_group_perm)
async def create_group(
        group_id: int,
        update_schema: GroupUpdateSchema,
        user=Depends(get_current_active_user)
):
    GroupCtrl().update_group(group_id, update_schema)
    return dict(r={}, msg='更新成功', code=0)
