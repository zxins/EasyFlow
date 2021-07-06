# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, BigInteger, String, DateTime, Text, PickleType, JSON


from database import Base


class RoleModel(Base):
    """ 角色 """
    __tablename__ = 'role'

    role_id = Column(BigInteger, primary_key=True, autoincrement=True, comment="角色id")
    group_id = Column(BigInteger, nullable=False, comment="组id")
    name = Column(String(55), nullable=False, comment="角色名称")
    permissions = Column(JSON, nullable=False, default=[], comment="权限列表")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted_at = Column(DateTime, nullable=True, comment="删除时间")