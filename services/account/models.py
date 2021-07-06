# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, BigInteger, String, DateTime, Boolean

from database import Base


class AccountModel(Base):
    __tablename__ = 'account'

    uid = Column(BigInteger, primary_key=True, autoincrement=True, comment="账户id")
    role_id = Column(BigInteger, nullable=False, default=0, comment="角色id")
    username = Column(String(35), nullable=False, comment="登录账号")
    password = Column(String(255), nullable=False, comment="密码(加密后)")
    name = Column(String(55), nullable=False, comment="姓名")
    gender = Column(String(10), nullable=False, default="", comment="性别")
    phone = Column(String(15), nullable=False, default="", comment="联系电话")
    logined_at = Column(DateTime, nullable=False, default=datetime.now, comment="最后登录时间")
    is_superuser = Column(Boolean, nullable=False, default=False, comment="是否是超级管理员")
    is_active = Column(Boolean, nullable=False, default=True, comment="是否活跃(可登录)")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted_at = Column(DateTime, nullable=True, comment="删除时间")


class AccountTokenModel(Base):
    __tablename__ = 'account_token'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="id")
    uid = Column(BigInteger, nullable=False, index=True, comment="用户id")
    access_token = Column(String(32), nullable=False, index=True, comment="token")
    refresh_token = Column(String(32), nullable=False, comment="刷新token")
    expired_at = Column(DateTime, nullable=False, default=datetime.now, comment="过期时间")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")
