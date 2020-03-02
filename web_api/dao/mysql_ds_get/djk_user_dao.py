#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : jzy
@Contact :  : 905414225@qq.com
@Software: PyCharm
@File    :
@Time    : 2019/9/29 11:32
@Desc    :
@Scene   :
"""
import flask_gevent.web_api.service.db_conf_service as db_service
import pymysql, traceback


class djk_user_dao(object):
    """用户表"""

    def __init__(self, db=None, pool=None):
        if pool:
            self.conn, self.cursor = db_service.get_db_from_pool(pool)
        else:
            self.conn, self.cursor = db_service.get_db_mysql_ds_get() if not db else db

    # ----------------------    查询操作    ----------------------------
    def search_user(self,username,password):
        """查询当前用户是否存在"""
        sql = "select id,username,nick_name,similarity from djk_user where username='%s' and password='%s' "
        sql = sql % (username,password)
        try:
            self.cursor.execute(sql.replace("'None'", "Null"))
            self.conn.commit()
            return self.cursor.fetchone()
        except:
            # traceback.print_exc()
            pass


    def close(self):
        self.cursor.close()
        self.conn.close()

    def run_sql(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.fetchall()


if __name__ == '__main__':
    pass
    # dao = originality_testing_result_dao()
    # res= dao.is_vip(uid="62053b05b06d4a16b85bfd805e9ba4db")
    # print(res)
