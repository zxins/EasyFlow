# -*- coding: utf-8 -*-
import when
from sqlalchemy import insert, select, delete

from config import config
from library.controller import BaseCtrl
from library.exception import ApiException
from library.security import pbkdf2_password_hash, verify_pbkdf2_password, short_uuid
from services.account.models import AccountModel, AccountTokenModel
from services.account.schemas import (
    AccountCreateSchema,
    AccountLoginOutSchema,
    AccountOutSchema,
    AccountTokenSchema
)


class AccountCtrl(BaseCtrl):

    def exits_username(self, username: str):
        filters = [
            AccountModel.username == username,
        ]
        return super()._exists(AccountModel, filters)

    def create_account(self, create_schema: AccountCreateSchema):
        if self.exits_username(username=create_schema.username):
            raise ApiException(201001, '该账号已存在')

        create_schema.password = pbkdf2_password_hash(create_schema.password)
        q = insert(AccountModel).values(create_schema.dict(exclude_none=True))
        result = self.db.execute(q)
        self.__commit__()
        return result.inserted_primary_key[0]  # uid

    def retrieve_by_username(self, username, allow_raise: bool = True):
        filters = [
            AccountModel.deleted_at.is_(None),
            AccountModel.username == username
        ]
        q = select(AccountModel).where(*filters)
        result = self.db.execute(q).scalar()
        if allow_raise and result is None:
            raise ApiException(201002, '该用户不存在')
        return AccountOutSchema.from_orm(result) if result else None

    def retrieve_account(self, uid: int, allow_raise: bool = True):
        filters = [
            AccountModel.deleted_at.is_(None),
            AccountModel.uid == uid
        ]
        q = select(AccountModel).where(*filters)
        result = self.db.execute(q).scalar()
        if allow_raise and result is None:
            raise ApiException(201002, '该用户不存在')
        return AccountOutSchema.from_orm(result) if result else None

    def login_by_password(self, username: str, password: str):
        account = self.retrieve_by_username(username, False)
        if not account.is_active:
            raise ApiException(111111, '该用户已禁止登录')
        if not account or not verify_pbkdf2_password(account.password, password):
            raise ApiException(201003, '用户名或密码错误')
        token_ctrl = AccountTokenCtrl()
        token = token_ctrl.create_token(account.uid)
        return AccountLoginOutSchema(user=account.copy(exclude={'password'}), token=token)


class AccountTokenCtrl(BaseCtrl):

    def _clear_old_token(self, uid: int, inner_commit: bool = False):
        q = delete(AccountTokenModel).where(AccountTokenModel.uid == uid)
        self.db.execute(q)
        if inner_commit:
            self.__commit__()

    def create_token(self, uid: int):
        self._clear_old_token(uid)

        token = AccountTokenSchema(
            uid=uid,
            access_token=short_uuid(),
            refresh_token=short_uuid(),
            expired_at=when.future(days=config.ACCESS_TOKEN_EXPIRE_DAYS)
        )
        q = insert(AccountTokenModel).values(token.dict(exclude_none=True))
        self.db.execute(q)
        self.__commit__()
        return token

    def retrieve_token_by_uid(self, uid: int):
        q = select(AccountTokenModel).where(
            AccountTokenModel.uid == uid,
        )
        result = self.db.execute(q).scalar()
        return AccountTokenSchema.from_orm(result) if result else None

    def retrieve_token(self, token: str):
        q = select(AccountTokenModel).where(
            AccountTokenModel.access_token == token,
        )
        result = self.db.execute(q).scalar()
        return AccountTokenSchema.from_orm(result) if result else None
