#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : jzy
@Contact :  : 905414225@qq.com
@Software: PyCharm
@File    : db_service.py
@Time    : 2018/12/10 16:51
@Desc    : 数据库连接配置文件
"""
import configparser,os
import pymysql
import redis

cf = configparser.ConfigParser()
root_path = os.path.abspath(__file__).split("flask_gevent")[0]
# 绝对路径,此种方法的前提,所有内容都在get_ai下面，调用文件的文件夹深度可以不限
cf.read(root_path + "/flask_gevent/conf/db.ini")

def get_mysql_db():
    """mysql数据库连接"""
    connect = pymysql.Connect(
        host=cf.get('db', 'host'),
        port=cf.getint('db', 'port'),
        user=cf.get('db', 'user'),
        passwd=cf.get('db', 'passwd'),
        db=cf.get('db', 'db'),
        charset='utf8'
    )
    connect.ping(reconnect=True)
    cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)
    return connect,cursor

def get_db_mysql_ds_get():
    """mysql数据库连接"""
    connect = pymysql.Connect(
        host=cf.get('db_mysql_ds_get', 'host'),
        port=cf.getint('db_mysql_ds_get', 'port'),
        user=cf.get('db_mysql_ds_get', 'user'),
        passwd=cf.get('db_mysql_ds_get', 'passwd'),
        db=cf.get('db_mysql_ds_get', 'db'),
        charset='utf8mb4'
    )
    connect.ping(reconnect=True)
    cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)
    return connect,cursor



def get_local_mysql_db():
    connect = pymysql.Connect(
        host=cf.get('db_local_python', 'host'),
        port=cf.getint('db_local_python', 'port'),
        user=cf.get('db_local_python', 'user'),
        passwd=cf.get('db_local_python', 'passwd'),
        db=cf.get('db_local_python', 'db'),
        charset='utf8mb4'
    )
    connect.ping(reconnect=True)
    cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)
    return connect, cursor

def get_redis(redis_pool=None):
    """获取一个redis连接实例"""
    pool = redis_pool if redis_pool else redis.ConnectionPool(host=cf.get("redis", "host"), port=cf.get("redis", "port"), decode_responses=True, password=cf.get("redis", "password"))
    # pool = redis_pool if redis_pool else redis.ConnectionPool(host='localhost', port=6379, decode_responses=True, password=None)
    return redis.Redis(connection_pool=pool)

def get_local_redis(redis_pool=None):
    """获取一个redis连接实例"""
    # pool = redis_pool if redis_pool else redis.ConnectionPool(host=cf.get("redis", "host"), port=cf.get("redis", "port"), decode_responses=True, password=cf.get("redis", "password"))
    pool = redis_pool if redis_pool else redis.ConnectionPool(host='localhost', port=6379, decode_responses=True, password=None)
    return redis.Redis(connection_pool=pool)

def get_redis_pool():
    """获取一个redis连接池"""
    return redis.ConnectionPool(host=cf.get("redis", "host"), port=cf.get("redis", "port"), decode_responses=True, password=cf.get("redis", "password"))

# def get_neo4j_db():
#     # from py2neo import Graph
#     return Graph(cf.get("neo4j_db","address"), username=cf.get("neo4j_db","username"), password=cf.get("neo4j_db","password"))

def get_mysql_get_ai_connect():
    """ 获取mysql数据库 get_ai库的连接"""
    connect = pymysql.Connect(
        host=cf.get('db', 'host'),
        port=cf.getint('db', 'port'),
        user=cf.get('db', 'user'),
        passwd=cf.get('db', 'passwd'),
        db=cf.get('db', 'db'),
        charset='utf8'
    )
    connect.ping(reconnect=True)
    cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)
    return connect,cursor


def get_db_from_pool(pool):
    conn = pool.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return conn,cursor



if __name__ == '__main__':
    pass
    redis = get_redis()
    res = redis.rpush("test2","123")
    print()