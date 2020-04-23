#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth
import time
import json


class IndexHandler(BaseHandler):

    @Auth
    def get(self):
        user = self.redis.hget(self.application.settings['users_key'],self.session.data['username'])
        self.render('setting/index.html',user=json.loads(user))


# 系统初始化
class InstallHandler(BaseHandler):

    def get(self):
        if self.session.isGuest: # 未登录
            users = self.redis.hlen(self.application.settings['users_key'])
            if users == 0: # 用户列表无用户
                self.render('setting/install.html')
            else:
                return self.redirect('/user/login?_from=installed')  # 已登录则跳转到首页
        else: # 已登录
            return self.redirect('/?_from=installed') # 已登录则跳转到首页


    def post(self):
        if self.session.isGuest: # 未登录
            users = self.redis.hlen(self.application.settings['users_key'])
            if users == 0: # 用户列表无用户
                nickname = self.get_argument('nickname')
                username = self.get_argument('username')
                password = self.get_argument('password')
                if not nickname or not username or not password:
                    return self.returnJson({'code': -1, 'msg': u'用户信息不能为空！'})
                result = self.create_user(nickname,username,password)
                if result:
                    return self.returnJson({'code': 0, 'msg': u'保存成功，点击[确定]去登录吧！'})
                else:
                    return self.returnJson({'code': -1, 'msg': u'保存失败，请检查您的部署环境！'})
            else:
                return self.returnJson({'code': -1, 'msg': u'非法请求(-1)！'})
        else: # 已登录
            return self.returnJson({'code': -2, 'msg': u'非法请求(-2)！'})


    # 创建新用户
    def create_user(self,nickname,username,password):
        data = {
            'uid': 1000,
            'nickname': nickname,
            'username': username,
            'password': password,
            'email': '',
            'role': 1,  # Administrator
            'status': 10,  # Active status
            'reg_time': int(time.time())
        }
        return self.redis.hset(self.settings['users_key'], data['username'], json.dumps(data))
