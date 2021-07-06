# -*- coding: utf-8 -*-
from services.account.controllers import AccountCtrl
from services.account.schemas import AccountCreateSchema


def test_create_account():
    schema = AccountCreateSchema(
        username="admin",
        password="123456",
        name="张三",
        phone="18888888888",
        title="开发工程师",
        gender="male"
    )

    ctrl = AccountCtrl()
    uid = ctrl.create_account(schema)
    print(uid)


def test_login():
    ctrl = AccountCtrl()
    account = ctrl.login_by_password('admin', '123456')

    print(account)



if __name__ == '__main__':
    # test_create_account()
    test_login()
    # schema = AccountCreateSchema(
    #     username="admin",
    #     password="123456",
    #     name="张三",
    #     phone="18888888888",
    #     title="开发工程师",
    #     gender="male"
    # )
    # s2 = schema.copy(exclude={'gender'})
    # print(schema)
    # print(s2)
