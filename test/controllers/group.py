# -*- coding: utf-8 -*-
from services.group.controllers import GroupCtrl
from services.group.schemas import GroupCreateSchema, GroupUpdateSchema


def print_sections(sections):
    for row in sections:
        tab_num = row.level - 1
        print(tab_num * ' ' + row.name)
        if row.childs:
            print_sections(row.childs)


def test_get_group_section():
    ctrl = GroupCtrl()
    tops = ctrl.get_group_sections()
    print_sections(tops)


def test_create_group():
    schema = GroupCreateSchema(
        name="测试部门一组",
        superior_id=6
    )
    ctrl = GroupCtrl()
    group_id = ctrl.create_group(schema)
    print(group_id)


def test_update_group():
    schema = GroupUpdateSchema(
        superior_id=6
    )
    ctrl = GroupCtrl()
    ctrl.update_group(7, schema)


if __name__ == '__main__':
    test_get_group_section()
    # test_create_group()
    # test_update_group()
