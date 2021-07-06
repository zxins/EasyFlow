# -*- coding: utf-8 -*-
import requests
from decorators_demo import md5_secret_with_random
from config import config
from shortuuid import uuid

url = 'http://127.0.0.1:8888/v1/groups'
app_random = uuid()
sign = md5_secret_with_random(config.DEV_KEY, config.SECRET_KEY, app_random)
headers = {
    'app_sign': sign,
    'app_random': app_random,
    'Authorization': 'token NdFkxf48E4wDCjsEYV3z9R'
}


def test_create_group():
    r = requests.post(url, headers=headers)
    print(r.json())


def test_get_group():
    r = requests.get(url, headers=headers)
    print(r.json())


if __name__ == '__main__':
    # test_create_group()
    test_get_group()
