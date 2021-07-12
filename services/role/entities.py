# -*- coding: utf-8 -*-
from collections import namedtuple
from typing import Union

Module = namedtuple('Module', ['code', 'name', 'permissions'])
Permission = namedtuple('Permission', ['module', 'code', 'name'])

MODULES = {}
PERMISSIONS = {}
MODULE_PERMISSIONS = {}


def add_module(code: Union[str, int], name: str) -> Module:
    global MODULES
    MODULES[code] = Module(code, name, [])
    return MODULES[code]


def add_permission(module: Module, sub_code: Union[str, int], name: str) -> Permission:
    global PERMISSIONS

    # 权限code = module.code + 子code
    sub_code = str(sub_code).zfill(3)  # sub_code定义为三位数, 不足3位则补0
    module_code = str(module.code)
    code = module_code + sub_code
    # 权限实例
    permission = Permission(module, code, name)
    # 放入权限字典
    PERMISSIONS[code] = permission
    # 更新module的权限列表
    module.permissions.append(permission)
    # 维护模块-权限关系字典
    MODULE_PERMISSIONS.setdefault(module_code, [])
    MODULE_PERMISSIONS[module_code].append(permission)

    return PERMISSIONS[code]


def get_permission(code: str) -> Permission:
    return PERMISSIONS[code]


# modules
account_module = add_module(100, '用户')
group_module = add_module(101, '部门')
role_module = add_module(102, '角色')

# permissions
# account

# group
get_group_list_perm = add_permission(group_module, 1, '查看部门列表')
create_group_perm = add_permission(group_module, 2, '创建部门')
update_group_perm = add_permission(group_module, 3, '更新部门')

# role
get_role_list_perm = add_permission(role_module, 1, '查看角色列表')
create_role_perm = add_permission(role_module, 2, '添加角色')
set_role_permissions_perm = add_permission(role_module, 3, '设置角色权限')
