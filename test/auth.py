# -*- coding: utf-8 -*-
import requests
from decorators_demo import md5_secret_with_random
from config import config
from shortuuid import uuid

url = 'http://127.0.0.1:8888/v1/accounts'

app_random = uuid()
sign = md5_secret_with_random(config.DEV_KEY, config.SECRET_KEY, app_random)

headers = {
    'app_sign': sign,
    'app_random': app_random,
    'Authorization': 'token h8JKEoG8S6JcWFV5TLESg9'
}
r = requests.get(url, headers=headers)
print(r.text)
