# -*- coding: utf-8 -*-
import requests

root_url = 'http://127.0.0.1:8888/v1/roles'


def test_role_list():
    r = requests.get(root_url)
    print(r.json())


if __name__ == '__main__':
    test_role_list()
