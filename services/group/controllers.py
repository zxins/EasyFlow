# -*- coding: utf-8 -*-
from sqlalchemy import insert, text, select, update

from library.controller import BaseCtrl
from library.exception import ApiException
from services.group.models import GroupModel
from services.group.schemas import GroupCreateSchema, GroupOutSchema, GroupUpdateSchema


class GroupCtrl(BaseCtrl):

    def _filter_sections_tree(self, groups):
        min_level = 1000
        for group in groups:
            if group.level <= min_level:
                min_level = group.level
            childs_filter = filter(lambda x: x.superior_id == group.group_id, groups)
            group.childs = list(childs_filter)
        return list(filter(lambda x: x.level == min_level, groups))

    def get_group_sections(self, name: str = None):
        """ 树状结构的组织列表

        结构示例如下:
            A组一级:
              A组二级:
               A组三级:
                ...

            B组一级:
              B组二级:
                ...
        """

        # 这个模块的数据不会很多，不必担心性能问题

        # 查询字段
        columns = GroupModel.__table__.columns.keys()
        fields = [text(f'`{GroupModel.__tablename__}`.`{col}`') for col in columns]

        filters = [GroupModel.deleted_at.is_(None), ]
        if name:
            filters.append(GroupModel.name.like(f'%{name}%'))
        q = select(fields).where(*filters).order_by(GroupModel.created_at.asc())
        items = self.db.execute(q).all()
        all_groups = [GroupOutSchema.from_orm(item) for item in items]

        groups = self._filter_sections_tree(all_groups)
        return groups

    def retrieve_group(self, group_id: int, allow_raise: bool = True):
        q = select(GroupModel).filter(GroupModel.group_id == group_id)
        result = self.db.execute(q).scalar()
        if allow_raise and result is None:
            raise ApiException(111111, '该分组不存在')
        if result is None:
            return None
        return GroupOutSchema.from_orm(result)

    def exits_group_name(self, name: str, allow_group_id: int = None) -> bool:
        filters = [
            GroupModel.deleted_at.is_(None),
            GroupModel.name == name
        ]
        if allow_group_id:
            filters.append(GroupModel.group_id != allow_group_id)
        return super()._exists(GroupModel, filters)

    def create_group(self, create_schema: GroupCreateSchema):
        if self.exits_group_name(create_schema.name):
            raise ApiException(111111, '该名称已存在')

        create_info = create_schema.dict(exclude_none=True)
        create_info['level'] = 1
        if create_schema.superior_id:
            superior_group = self.retrieve_group(create_schema.superior_id)
            create_info['level'] = superior_group.level + 1

        q = insert(GroupModel).values(create_info)
        result = self.db.execute(q)
        self.__commit__()
        return result.inserted_primary_key[0]  # group id

    def update_group(self, group_id: int, update_schema: GroupUpdateSchema):
        if self.exits_group_name(update_schema.name, group_id):
            raise ApiException(111111, '该名称已存在')

        update_info = update_schema.dict(exclude_none=True)
        if update_schema.superior_id:
            superior_group = self.retrieve_group(update_schema.superior_id)
            update_info['level'] = superior_group.level + 1
        elif update_schema.superior_id == 0:
            update_info['level'] = 1

        q = update(GroupModel).where(GroupModel.group_id == group_id).values(update_info)
        self.db.execute(q)
        self.__commit__()
