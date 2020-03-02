# flask_gevent
基于flask+gevent搭建改造的一个高可用的后端服务框架
* 适用python新手学习
* 适用转到python的其它语言开发者

框架思路沿用java经典的分层架构,controller层、service层、dao层
utils/* 工具类下面封装了常用的通用方法和接口返回的代码修饰类
conf/*  配置文件，用于记录一些关键性配置
flask_gevent_api.py flask启动类，只用来处理路由和加载DB

![后端通过框架](https://github.com/17621192638/flask_gevent/blob/master/a.png)
