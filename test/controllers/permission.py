# -*- coding: utf-8 -*-

from services.role.controllers import RoleCtrl
from services.role.schemas import *


def test_paginate_roles():
    ctrl = RoleCtrl()

    pagination = ctrl.paginate_roles(RolePaginateSchema())
    for item in pagination.items:
        print(item)


def test_create_role():
    ctrl = RoleCtrl()

    schema = RoleCreateSchema(
        name="文员",
        group_id=1
    )
    role_id = ctrl.create_role(schema)
    print(role_id)


def test_retrieve_modules_with_permissions():
    ctrl = RoleCtrl()
    permissions = ctrl.retrieve_modules_with_permissions()
    for permission in permissions:
        print(permission)


def test_retrieve_permissions_by_codes():
    ctrl = RoleCtrl()
    codes = [101001, 102001, '102002', '102003']
    permissions = ctrl.retrieve_permissions_by_codes(codes)
    print(permissions)


def test_set_permission():
    ctrl = RoleCtrl()
    ctrl.set_permissions(1, [101001, 102001])

def test_get_permission_codes():
    ctrl = RoleCtrl()
    codes = ctrl.get_permission_codes(1)
    print(codes)

if __name__ == '__main__':
    # test_create_role()
    # test_retrieve_modules_with_permissions()
    test_retrieve_permissions_by_codes()
    # test_set_permission()
    # test_get_permission_codes()
