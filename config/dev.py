# -*- coding: utf-8 -*-
import os
from typing import Union

from pydantic import BaseSettings, AnyHttpUrl, IPvAnyAddress


class Config(BaseSettings):
    # 项目目录 - 当前文件所在上级目录
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # 文档
    # DOCS_URL: str = "/docs"
    # OPENAPI_URL: str = "/openapi.json"
    # REDOC_URL: Optional[str] = "/redoc"

    # Debug
    DEBUG_APP_KEYS: list = ["abcdefghijklmnopqrstuvwxyz"]

    # token
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    DEV_KEY: str = "3gZ5bdpyAE6Z"
    SECRET_KEY: str = 'c9a6861e1b164a70be0d398442f0bc98'

    # MySQL
    MYSQL_USER: str = "root"
    MYSQL_PASS: str = os.environ.get('MYSQL_PASS')
    MYSQL_HOST: Union[AnyHttpUrl, IPvAnyAddress] = "127.0.0.1"
    MYSQL_DATABASE: str = "easy_flow"

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}/{MYSQL_DATABASE}?charset=utf8mb4"

    # Redis
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_PASS: str = ""

    # cache
    REDIS_CACHE_DB: int = 0
    CACHE_PREFIX: str = "ef"

    CACHE_EXPIRED: dict = {}


config = Config()
