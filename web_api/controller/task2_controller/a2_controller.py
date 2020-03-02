#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : jzy
@Contact :  : 905414225@qq.com
@Software: PyCharm
@File    :
@Time    : 2019/09/27 18:36
@Desc    :
"""
from flask_restful import Resource, request
from flask import current_app
import flask_gevent.utils.response_util as response_util
from flask_gevent.web_api.service.task2_service.a2_service import a2_service


def init(app):
    global service
    service = a2_service()
    #redis = app.redis


class test2(Resource):
    """ 后台登录 """
    @response_util.response_filter_v2
    def post(self):
        text_json = request.get_json()
        username = text_json.get("username","admin")
        password = text_json.get("password","admin")
        return service.test2(username,password)
