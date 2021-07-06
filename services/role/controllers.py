# -*- coding: utf-8 -*-
from typing import List, Union

from sqlalchemy import text, outerjoin, select, insert, update

from library.controller import BaseCtrl
from services.group.models import GroupModel
from services.role.entities import MODULE_PERMISSIONS, MODULES, PERMISSIONS
from services.role.models import RoleModel
from services.role.schemas import (
    RolePaginateSchema,
    RoleOutSchema,
    RoleCreateSchema,
    RolePermissionOutSchema,
    RoleModuleOutSchema,
)


class RoleCtrl(BaseCtrl):

    def paginate_roles(self, paginate_schema: RolePaginateSchema):
        # 查询字段
        columns = RoleModel.__table__.columns.keys()
        fields = [text(f'{RoleModel.__tablename__}.{col}') for col in columns]

        # 关联组
        fields.append(GroupModel.name.label('group_name'))

        # 条件
        filters = [RoleModel.deleted_at.is_(None), ]
        if paginate_schema.name:
            fields.append(RoleModel.name.like(f'%{paginate_schema.name}%'))

        join_tables = outerjoin(
            RoleModel,
            GroupModel,
            GroupModel.group_id == RoleModel.group_id
        )

        q = select(fields).select_from(join_tables).where(*filters).order_by(RoleModel.created_at.desc())
        per_page = paginate_schema.per_page
        page = paginate_schema.page
        return super()._get_pagination_by_query(q, RoleOutSchema, per_page, page)

    def create_role(self, create_schema: RoleCreateSchema):
        q = insert(RoleModel).values(create_schema.dict(exclude_none=True))
        result = self.db.execute(q)
        self.__commit__()
        return result.inserted_primary_key[0]

    def retrieve_modules_with_permissions(self) -> List[RoleModuleOutSchema]:
        """ 查询所有模块(附带模块权限列表) """
        module_permissions = []
        for code, module in MODULES.items():
            schema = RoleModuleOutSchema.from_orm(module)
            module_permissions.append(schema)
        return module_permissions

        # for module_code, permissions in MODULE_PERMISSIONS.items():
        #     module = MODULES[module_code]
        #     schema = ModulePermissionsOutSchema(
        #         code=module.code,
        #         name=module.name,
        #         permissions=[PermissionOutSchema.from_orm(role) for role in permissions]
        #     )
        #     module_permissions.append(schema)
        # return module_permissions

    def retrieve_permissions_by_codes(self, permission_codes: List[Union[str, int]]):
        """ 通过code列表查询permission实例 """
        permissions = []
        for code in permission_codes:
            permission = PERMISSIONS.get(str(code))
            schema = RolePermissionOutSchema.from_orm(permission) if permission else None
            permissions.append(schema)
        return permissions

    def set_permissions(self, role_id: int, permissions: List[Union[str, int]]):
        permissions = [str(row) for row in permissions]
        q = update(RoleModel).where(RoleModel.role_id == role_id).values(dict(permissions=permissions))
        self.db.execute(q)
        self.__commit__()

    def get_permission_codes(self, role_id: int) -> List[Union[str, int]]:
        q = select(RoleModel).where(RoleModel.role_id == role_id)
        result = self.db.execute(q).scalar()
        if not result:
            return []
        return result.permissions
