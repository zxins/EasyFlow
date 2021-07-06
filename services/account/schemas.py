# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional
from typing_extensions import Literal

from pydantic import BaseModel, Field


class AccountOutSchema(BaseModel):
    """ 输出account """
    uid: int = Field(..., title="用户id")
    role_id: int = Field(..., title="角色id")
    role_name: Optional[str] = Field(None, title="角色名称")
    username: str = Field(..., title="登录用户名")
    password: str = Field(..., title="登录密码")  # 暴露给外部时要清除
    name: str = Field(..., title="用户名称")
    gender: str = Field(..., title="性别")
    phone: str = Field(..., title="联系电话")
    is_active: bool = Field(..., title="是否可登录")
    is_superuser: bool = Field(..., title="是否是超管")

    class Config:
        orm_mode = True


class AccountCreateSchema(BaseModel):
    """ 创建account """
    username: str = Field(..., title="登录用户名")
    password: str = Field(..., title="登录密码")
    name: str = Field(..., title="用户名称")
    phone: str = Field(..., title="联系电话")
    role_id: Optional[int] = Field(None, title="角色id")
    gender: Literal['male', 'female'] = Field(..., title="性别")


class AccountTokenSchema(BaseModel):
    """ token创建&输出 """
    uid: int = Field(..., title="用户id")
    access_token: str = Field(..., title="访问令牌")
    refresh_token: str = Field(..., title="刷新access_token的令牌")
    expired_at: datetime = Field(..., title="过期时间")

    class Config:
        orm_mode = True


# class AccountLoginSchema(BaseModel):
#     """ 登录请求 """
#     username: str = Field(..., title="登录用户名", ge=5, le=30)
#     password: str = Field(..., title="登录密码", ge=1, gt=35)


class AccountLoginOutSchema(BaseModel):
    """ 登录返回值 """
    user: AccountOutSchema
    token: AccountTokenSchema
