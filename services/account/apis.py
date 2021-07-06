# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordRequestForm

from decorators import get_current_superuser
from .schemas import AccountOutSchema, AccountCreateSchema
from .controllers import AccountCtrl

login_router = APIRouter()
account_router = APIRouter(prefix='/accounts')


class SimpleForm(OAuth2PasswordRequestForm):
    def __init__(self, username: str = Form(...), password: str = Form(...), ):
        super(SimpleForm, self).__init__(username=username, password=password, scope="")


# @login_router.post('/login', summary="登录")
# async def login(login_schema: AccountLoginSchema):
#     username = login_schema.username
#     password = login_schema.password
#     account = AccountCtrl().login_by_password(username, password)
#     return dict(r=account.dict(), msg="登录成功", code=0)

@login_router.post('/login', summary="登录")
async def simple_oauth2_login(form_data: SimpleForm = Depends()):
    username = form_data.username
    password = form_data.password
    login_info = AccountCtrl().login_by_password(username, password)
    token = login_info.token
    return {"access_token": token.access_token, "token_type": "bearer"}


@account_router.post('', summary="创建用户", dependencies=[Depends(get_current_superuser)])
async def create_account(create_schema: AccountCreateSchema):
    """ 只有超级管理员可以创建新用户 """
    AccountCtrl().create_account(create_schema)
    return dict(r={}, msg='创建成功', code=0)
