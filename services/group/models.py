# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, BigInteger, String, DateTime, Integer

from database import Base


class GroupModel(Base):
    """ 分组性质的, 如：部门 """
    __tablename__ = 'group'

    group_id = Column(BigInteger, primary_key=True, autoincrement=True, comment="组id")
    superior_id = Column(BigInteger, nullable=False, default=0, comment="上级分组,0表示无分组")
    name = Column(String(55), nullable=False, comment="名称")
    description = Column(String(255), nullable=False, default="", comment="描述")
    manager_name = Column(String(25), nullable=False, default="", comment="负责人")
    manager_phone = Column(String(25), nullable=False, default="", comment="负责人手机号")
    level = Column(Integer, nullable=False, default=1, comment="层级")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted_at = Column(DateTime, nullable=True, comment="删除时间")
