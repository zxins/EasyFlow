# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel

from library.pagination import PaginateSchema


class GroupPaginateSchema(PaginateSchema):
    name: Optional[str] = None


class GroupOutSchema(BaseModel):
    group_id: int
    name: str


class GroupCreateSchema(BaseModel):
    name: str
