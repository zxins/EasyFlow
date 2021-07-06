# -*- coding: utf-8 -*-
from sqlalchemy import insert, text, select

from library.controller import BaseCtrl
from library.exception import ApiException
from services.group.models import GroupModel
from services.group.schemas import GroupCreateSchema, GroupPaginateSchema, GroupOutSchema


class GroupCtrl(BaseCtrl):

    def paginate_groups(self, paginate_schema: GroupPaginateSchema):
        # 查询字段
        columns = GroupModel.__table__.columns.keys()
        fields = [text(f'{GroupModel.__tablename__}.{col}') for col in columns]

        # 关联组
        fields.append(GroupModel.name.label('group_name'))

        # 条件
        filters = [GroupModel.deleted_at.is_(None), ]
        if paginate_schema.name:
            fields.append(GroupModel.name.like(f'%{paginate_schema.name}%'))

        q = select(GroupModel).where(*filters).order_by(GroupModel.created_at.desc())
        per_page = paginate_schema.per_page
        page = paginate_schema.page
        return super()._get_pagination_by_query(q, GroupOutSchema, per_page, page)

    def get_group_sections(self):
        pass

    def exits_group_name(self, name: str):
        filters = [
            GroupModel.deleted_at.is_(None),
            GroupModel.name == name
        ]
        return super()._exists(GroupModel, filters)

    def create_group(self, create_schema: GroupCreateSchema):
        if self.exits_group_name(create_schema.name):
            raise ApiException(111111, '该名称已存在')
        q = insert(GroupModel).values(create_schema.dict(exclude_none=True))
        result = self.db.execute(q)
        self.__commit__()
        return result.inserted_primary_key[0]  # group id
