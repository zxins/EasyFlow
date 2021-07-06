# -*- coding: utf-8 -*-
from fastapi import APIRouter
from services.account.apis import account_router, login_router
from services.group.apis import group_router
from services.role.apis import role_router

service_router = APIRouter()
service_router.include_router(login_router, tags=['登录'])
service_router.include_router(account_router, tags=['账户'])
service_router.include_router(group_router, tags=['分组'])
service_router.include_router(role_router, tags=['角色'])
