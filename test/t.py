# -*- coding: utf-8 -*-
from services.role.entities import get_role_list_perm
from services.role.schemas import RolePermissionOutSchema

print(get_role_list_perm)
print(RolePermissionOutSchema.from_orm(get_role_list_perm))