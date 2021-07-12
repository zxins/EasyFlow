# -*- coding: utf-8 -*-
from typing import Optional, List, Union
from pydantic import BaseModel, Field, Json
from library.pagination import PaginateSchema


# --- 分页 ---
class RolePaginateSchema(PaginateSchema):
    """ 分页查询角色入参 """
    name: Optional[str] = None


# --- 输出 ---
class RoleOutSchema(BaseModel):
    """ 输出角色 """
    role_id: int = Field(..., title="角色id")
    name: str = Field(..., title="角色名称")
    permissions: Json

    class Config:
        orm_mode = True


class RoleModuleOutShortSchema(BaseModel):
    """ 输出模块, 不带permissions """
    code: str = Field(..., title="模块代码")
    name: str = Field(..., title="模块名称")

    class Config:
        orm_mode = True


class RolePermissionOutShortSchema(BaseModel):
    """ 输出权限, 不带module """
    code: str = Field(..., title="权限代码")
    name: str = Field(..., title="权限名称")

    class Config:
        orm_mode = True


class RoleModuleOutSchema(RoleModuleOutShortSchema):
    """ 输出模块，含permissions """
    permissions: List[RolePermissionOutShortSchema]

    class Config:
        orm_mode = True


class RolePermissionOutSchema(RolePermissionOutShortSchema):
    """ 输出权限，含module """
    module: RoleModuleOutShortSchema = Field(..., title="所属模块")

    class Config:
        orm_mode = True


# --- 创建 ---
class RoleCreateSchema(BaseModel):
    """ 创建角色入参 """
    name: str = Field(..., title="角色名称")
    permissions: Optional[List[Union[str, int]]] = Field([], title="权限列表")
