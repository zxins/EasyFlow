# -*- coding: utf-8 -*-
from datetime import datetime
from functools import wraps
from typing import Optional

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param

from library.exception import ApiException
from services.account.controllers import AccountCtrl, AccountTokenCtrl
from services.account.schemas import AccountOutSchema
from services.role.entities import Permission


class Oauth2PasswordBearerOpen(OAuth2PasswordBearer):

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise ApiException(200002, "未授权，无法访问")
            else:
                return None
        return param


oauth2_scheme = Oauth2PasswordBearerOpen(tokenUrl="v1/login")


async def verify_token(token: str = Depends(oauth2_scheme)):
    """ 校验token """
    ctrl = AccountTokenCtrl()
    token = ctrl.retrieve_token(token=token)
    if not token:
        raise ApiException(200000, "未登录，无法访问")
    if datetime.now() >= token.expired_at:
        raise ApiException(200001, "登录状态失效")
    return token


async def get_current_user(token=Depends(verify_token)):
    ctrl = AccountCtrl()
    user = ctrl.retrieve_account(token.uid)
    return user


async def get_current_active_user(user: AccountOutSchema = Depends(get_current_user)):
    if not user.is_active:
        raise ApiException(201002, '该用户已被禁止登录')
    return user


async def get_current_superuser(user: AccountOutSchema = Depends(get_current_user)):
    """ 管理员 """
    if not user.is_superuser:
        raise ApiException(201001, '非超级管理员无法操作')
    return user


def check_permission(permisssion: Permission):
    def decorate(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get('user')
            if not user:
                raise Exception("缺少User信息")  # 通常是未在接口参数中声明user
            if user.is_superuser:
                return await func(*args, **kwargs)

            print(permisssion)
            return await func(*args, **kwargs)

        return wrapper

    return decorate
