# -*- coding: utf-8 -*-

class ApiException(Exception):
    def __init__(self, code: int, errMsg: str = "服务器内部错误，暂无法提供服务。", r: dict = {}):
        self.code = code
        self.errMsg = errMsg
        self.r = r
