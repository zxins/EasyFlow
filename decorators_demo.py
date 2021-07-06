# -*- coding: utf-8 -*-
from datetime import datetime
from functools import wraps

from fastapi import Request, Depends

from config import config
from library.security import md5_secret_with_random
from library.exception import ApiException
from services.account.controllers import AccountTokenCtrl, AccountCtrl
from services.account.schemas import AccountTokenSchema, AccountOutSchema
from services.role.entities import get_permission

async def verify_sign(app_sign: str, app_random: str) -> bool:
    """ 校验签名 """
    sign = md5_secret_with_random(config.DEV_KEY, config.SECRET_KEY, app_random)
    # 校验两个签名
    if sign != app_sign:
        return False
    return True


async def verify_token(request: Request) -> AccountTokenSchema:
    """ 校验token """
    authorization: str = request.headers.get("Authorization", "")
    scheme, _, param = authorization.partition(" ")

    ctrl = AccountTokenCtrl()
    token = ctrl.retrieve_token(token=param)
    if not token or datetime.now() >= token.expired_at:
        raise ApiException(200001, "登录状态失效")
    return token


async def get_current_user(token: AccountTokenSchema = Depends(verify_token)) -> AccountOutSchema:
    """ 通过token获取登录用户信息 """
    ctrl = AccountCtrl()
    account = ctrl.retrieve_account(token.uid)
    if not account.is_active:
        raise ApiException(111111, '该用户已禁止登录')
    return account


async def get_current_superuser(user: AccountOutSchema = Depends(get_current_user)):
    """ 管理员 """
    if not user.is_superuser:
        raise ApiException(111111, "该用户没有足够的权限")
    return user


def check_permission(code):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(kwargs.get('user'))
            perm = get_permission(code)
            print(perm)
            return func(*args, **kwargs)

        return wrapper

    return decorate