#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : jzy
@Contact :  : 905414225@qq.com
@Software: PyCharm
@File    : file_util.py
@Time    : 2018/10/15 15:12
@Desc    : http响应工具类
"""
import traceback,json,time
from flask import jsonify
from flask_gevent.utils.common_util import common_util

utils = common_util()

def response_filter(fn):
    """
    响应修饰器
    :param fn:被修饰的方法体
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            time1 = time.time()
            res = fn(*args, **kwargs)
            time2 = time.time()
            timeout = '%.3f' % (time2 - time1)
            return jsonify(response_ok(res=res,timeout=timeout))
        except Exception as e:
            traceback.print_exc()
            error_msg = "{0} - response_util - {1} - {2}".format(utils.get_current_time(),str(e),str(traceback.format_exc()))
            return jsonify(response_fail(res = error_msg))
    return wrapper

def response_ok(res=None,timeout=None):
    code = 200
    message=None
    if res:
        if type(res)==dict:
            code =res["code"] if res.__contains__("code") else 200
            message =res["message"] if res.__contains__("message") else None
        return {"code":code,"status": "success", "res": res,"timeout":timeout,"message":message}
    else:
        return {"code":code,"status":"success","timeout":timeout}

def response_fail(res=None):
    return {"code":400,"status":"fail","res":res}


def parse_response(fn):
    """
    响应修饰器
    :param fn:被修饰的方法体
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            res = fn(*args, **kwargs)
            data = json.loads(res.content)
            return data["res"] if data["status"] == "success" and data.__contains__("res") else None
        except Exception as e:
            traceback.print_exc()
            return None
    return wrapper

# -------------------------------
#  2019-09-24 修改后的规范接口
# -------------------------------

def response_filter_v2(fn):
    """
    响应修饰器
    :param fn:被修饰的方法体
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            time1 = time.time()
            res = fn(*args, **kwargs)
            time2 = time.time()
            timeout = '%.3f' % (time2 - time1)
            return jsonify(response_ok_v2(res=res,timeout=timeout))
        except Exception as e:
            traceback.print_exc()
            error_msg = "{0} - response_util - {1} - {2}".format(utils.get_current_time(),str(e),str(traceback.format_exc()))
            return jsonify(response_fail_v2(res = error_msg))
    return wrapper

def response_ok_v2(res=None,timeout=None):
    code = 200
    message=None
    if res:
        if type(res)==dict:
            code =res["code"] if res.__contains__("code") else 200
            message =res["message"] if res.__contains__("message") else None
        return {"code":code,"data": res,"timeout":timeout,"message":message}
    else:
        return {"code":code,"timeout":timeout}

def response_fail_v2(res=None):
    return {"code":400,"data":res}


def parse_response_v2(fn):
    """
    响应修饰器
    :param fn:被修饰的方法体
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            res = fn(*args, **kwargs)
            data = json.loads(res.content)
            if data["code"]==200:
                if data.__contains__("data"):
                    return data["data"]
                elif data.__contains__("res"):
                    return data["res"]
            else:
                return None
        except Exception as e:
            traceback.print_exc()
            return None
    return wrapper


if __name__ == '__main__':
    pass