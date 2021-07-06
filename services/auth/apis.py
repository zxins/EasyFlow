# -*- coding: utf-8 -*-
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from library.exception import ApiException
from services.account.controllers import AccountCtrl, AccountTokenCtrl

auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/simple")


class SimpleForm(OAuth2PasswordRequestForm):
    def __init__(self, username: str = Form(...), password: str = Form(...), ):
        super(SimpleForm, self).__init__(username=username, password=password, scope="")


async def verify_token(token: str = Depends(oauth2_scheme)):
    """ 校验token """
    ctrl = AccountTokenCtrl()
    token = ctrl.retrieve_token(token=token)
    if not token:
        raise ApiException(111111, "未登录")
    if datetime.now() >= token.expired_at:
        raise ApiException(200001, "登录状态失效")
    return token


async def get_current_user(token=Depends(verify_token)):
    ctrl = AccountCtrl()
    account = ctrl.retrieve_account(token.uid)
    if not account.is_active:
        raise ApiException(111111, '该用户已禁止登录')
    return account


@auth_router.post('/simple', summary="simple oauth2 login")
async def simple_oauth2_login(form_data: SimpleForm = Depends()):
    username = form_data.username
    password = form_data.password
    login_info = AccountCtrl().login_by_password(username, password)
    token = login_info.token
    return {"access_token": token.access_token, "token_type": "bearer"}


@auth_router.get('/test/simple', summary="test simple")
async def test_simple(user=Depends(get_current_user)):
    return user
