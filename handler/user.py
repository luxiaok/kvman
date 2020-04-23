#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth
#import pam
import json


class LoginHandler(BaseHandler):

    def get(self):
        if not self.session.isGuest:
            return self.redirect('/') # 已登录则跳转到首页
        next = self.get_argument("next", "/")
        self.render('user/login.html', next=next)

    # For PAM Authentication
    '''
    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        remember = self.get_argument("remember", "no")
        if not username or not password:
            return self.returnJson({'code':-1,'msg':u'用户名或密码错误(-1)！'})
        if pam.authenticate(username,password):
            return self.returnJson({'code': 0, 'msg': u'验证成功！'})
        else:
            if username == 'root':
                return self.returnJson({'code': 0, 'msg': u'用户名或密码错误(您的系统可能禁止root登录)！'})
            else:
                return self.returnJson({'code':-1,'msg':u'用户名或密码错误(-2)！'})
        #self.create_session(self,data,remember)
    '''

    def post(self):
        if not self.session.isGuest: # 已登录
            return self.returnJson({'code': -1, 'msg': u'重复登录！'})
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        remember = self.get_argument("remember", "no")
        if not username or not password: # 参数为空
            return self.returnJson({'code': -1, 'msg': u'用户名或密码错误(-1)！'})
        user_data = self.redis.hget(self.application.settings['users_key'],username)
        if not user_data: # 用户不存在
            return self.returnJson({'code': -2, 'msg': u'用户名或密码错误(-2)！'})
        user = json.loads(user_data)
        if user['password'] == password:
            self.create_session(user,remember) # 创建会话
            return self.returnJson({'code': 0, 'msg': u'Successful'})
        else: # 密码错误
            return self.returnJson({'code': -3, 'msg': u'用户名或密码错误(-3)！'})


    def create_session(self,data,remember):
        sid = self.session.gen_session_id()
        self.session.data = data
        self.session.isGuest = False
        #self.session.save() # Why don't save? See self._on_finish !!
        if remember == "yes":
            expires_days = 15  # Remember Session 15 days
        else:
            expires_days = None
        self.set_secure_cookie(self.cookie_name, sid, expires_days)


# Sign Out
class LogoutHandler(BaseHandler):
    def get(self):
        self.session.remove()
        self.clear_cookie(self.cookie_name)
        self.redirect(self.get_login_url())


class RegisterHandler(BaseHandler):

    def get(self):
        self.render('user/register.html')


# 修改个人资料
class ProfileHandler(BaseHandler):

    @Auth
    def post(self):
        username = self.get_argument('username')
        nickname = self.get_argument('nickname')
        email = self.get_argument('email')
        if not username or not nickname:
            return self.returnJson({'code': -1, 'msg': u'用户名或昵称不能为空！'})
        stuff = self.redis.hget(self.application.settings['users_key'], self.session.data['username'])
        if not stuff:  # 用户不存在
            return self.returnJson({'code': -1, 'msg': u'获取用户信息失败(-1)！'})
        user = json.loads(stuff)
        user['username'] = username
        user['nickname'] = nickname
        user['email'] = email
        self.redis.hset(self.application.settings['users_key'], username, json.dumps(user))
        if username != self.session.data['username']: # 修改了用户名
            self.redis.hdel(self.application.settings['users_key'], self.session.data['username']) # 删除原始数据
        # 更新Session
        self.session.data['username'] = username
        self.session.data['nickname'] = nickname
        return self.returnJson({'code': 0, 'msg': u'保存成功！'})


# 修改密码
class PasswdHandler(BaseHandler):

    @Auth
    def post(self):
        password0 = self.get_argument('password0')
        password = self.get_argument('password')
        if not password0 or not password:
            return self.returnJson({'code': -2, 'msg': u'密码不能为空！'})
        stuff = self.redis.hget(self.application.settings['users_key'], self.session.data['username'])
        if not stuff:  # 用户不存在
            return self.returnJson({'code': -2, 'msg': u'原始密码错误(-1)！'})
        user = json.loads(stuff)
        if password0 != user['password']:
            return self.returnJson({'code': -2, 'msg': u'原始密码错误(-2)！'})
        user['password'] = password
        self.redis.hset(self.application.settings['users_key'], self.session.data['username'],json.dumps(user))
        return self.returnJson({'code': 0, 'msg': u'修改成功，请牢记您的新密码！'})
