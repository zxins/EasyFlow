# -*- coding: utf-8 -*-
from typing import Optional, List

from pydantic import BaseModel

from library.pagination import PaginateSchema


class GroupBaseOutSchema(BaseModel):
    childs: Optional[List] = []  # 下级分组
    group_id: int
    superior_id: int
    name: str
    description: str
    manager_name: str
    manager_phone: str
    level: int


class GroupOutSchema(GroupBaseOutSchema):
    childs: Optional[List[GroupBaseOutSchema]] = []

    class Config:
        orm_mode = True


class GroupCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    superior_id: Optional[int] = None
    manager_name: Optional[str] = None
    manager_phone: Optional[str] = None


class GroupUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    superior_id: Optional[int] = None
    manager_name: Optional[str] = None
    manager_phone: Optional[str] = None
