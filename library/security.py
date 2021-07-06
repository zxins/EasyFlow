# -*- coding: utf-8 -*-
import hashlib
from string import digits
from uuid import uuid4 as uuid_uuid4

from shortuuid import uuid
from werkzeug.security import generate_password_hash, check_password_hash


# hash password
def pbkdf2_password_hash(passwd: str):
    return generate_password_hash(passwd)


# check password
def verify_pbkdf2_password(passwd_hash, passwd):
    return check_password_hash(passwd_hash, passwd)


# uuid
def short_uuid():
    return uuid()


# uuid4
def uuid4():
    return uuid_uuid4()


# 签名算法
def md5_secret_with_random(dev_key: str, secret_key: str, random_key: str) -> str:
    # 去掉字符串中的数字
    app_random = random_key.translate(str.maketrans('', '', digits))
    m = hashlib.md5()
    m.update('.'.join([dev_key, secret_key, app_random]).encode('utf-8'))
    sign = m.hexdigest()
    return sign
