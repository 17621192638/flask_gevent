from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
import sys
sys.path.append('../../')
from get_ai_djk.utils.common_util import common_util
from flask import Flask, jsonify,g
from flask_cors import CORS
from flask_restful import Api, Resource, request
import  flask_gevent.web_api.service.db_conf_service as db_service

app = Flask(__name__)
CORS(app)  # 跨域处理
api = Api(app)
app.config['JSON_AS_ASCII'] = False  # 设置后返回成中文
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))



# 初始化redis连接对象
# app.redis = db_service.get_redis()
# 初始化mysql,连接池对象
# app.ds_get_pool = db_service.get_mysql_ds_get_pool()


# 业务1
import flask_gevent.web_api.controller.task1_controller.a1_controller as a1_controller
a1_controller.init(app)
api.add_resource(a1_controller.test1, '/a1/test1',endpoint="a1_controller.test1")  # 添加路由


# 业务2
import flask_gevent.web_api.controller.task2_controller.a2_controller as a2_controller
a2_controller.init(app)
api.add_resource(a2_controller.test2, '/a2/test2',endpoint="a2_controller.test2")  # 添加路由
if __name__ == '__main__':
    print("start")
    utils = common_util()  # 静态工具类
    # ----------------------------        flask系统启动配置         ---------------------------------
    WSGIServer(('0.0.0.0', 7790),app).serve_forever()  #　配置gevent后的启动方式
    # app.run(host='0.0.0.0',port=7790)  # 不加gevent的方式

