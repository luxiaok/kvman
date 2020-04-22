#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# 2020-03-12

import tornado
import time
import json
from app.Session import Session


class BaseHandler(tornado.web.RequestHandler):

    # 初始化函数
    def initialize(self):
        # 当前请求时间
        self.time = int(time.time())
        # Session
        self._init_session()
        # Version
        self.app_version = self.application.__version__
        # Current Route
        self.url = self.get_current_route()

    # 后面的方法如果重写on_finish方法，需要调用_on_finish
    def _on_finish(self):
        # 更新Session
        self.session.save()
        # 请求逻辑处理结束时关闭数据库连接，如果不关闭可能会造成MySQL Server has gone away 2006错误
        #self.db.close()

    # 重载on_finish
    def on_finish(self):
        self._on_finish()

    # 重载write_error方法
    def write_error(self, status_code, **kwargs):
        title = "%s - %s" % (status_code, self._reason)
        if status_code == 404: # 捕获404
            self.render('page/error.html',title=title)
        elif status_code == 500: # 500可以正常捕获，404好像不行
            #print self.settings.get("serve_traceback")
            msg = ''
            if 'exc_info' in kwargs:
                for i in kwargs['exc_info']:
                    #print type(i)
                    msg += "<p>%s</p>" % str(i)
            self.render('page/error.html', title=title, code=status_code, msg=msg)
        else:
            self.render('page/error.html', title=title, code=status_code, msg=status_code)

    # Log Instance
    @property
    def log(self):
        return self.application.log

    # 获取当前路由
    def get_current_route(self):
        uri = self.request.uri.split('?')
        return uri[0]

    # 数据库
    @property
    def db(self):
        return self.application.db

    # Redis
    @property
    def redis(self):
        return self.application.redis

    # 返回Json
    def returnJson(self,data):
        self.set_header('Content-Type', 'application/json')
        self.write(data)

    # 格式化时间戳
    def format_time(self,timstamp=None,format='%Y-%m-%d %H:%M:%S'):
        return time.strftime(format, time.localtime(timstamp))


    # 获取当前登录用户信息，该方法为重写方法
    def get_current_user(self):
        if not self.session.isGuest and self.session.data:
            return self.session.data
        else:
            return None


    # Session初始化
    def _init_session(self):
        prefix = self.settings.get('session_prefix')
        expires = self.settings.get('session_expires')
        self.cookie_name = self.settings.get('cookie_name')
        self.sid = self.get_secure_cookie(self.cookie_name)
        self.session = Session(prefix, self.sid, expires, self.redis)


    # 获取 Kvm Server 配置
    def get_kvm_server(self,hostname=None):
        key = self.application.settings['kvm_servers_key']
        if hostname:
            stuff = self.redis.hget(key,hostname)
            if stuff:
                servers = json.loads(stuff)
            else:
                servers = None
        else:
            stuff = self.redis.hgetall(key)
            if stuff:
                servers = [json.loads(stuff[i]) for i in stuff]
            else:
                servers = []
        return servers
