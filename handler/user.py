#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from BaseHandler import BaseHandler
#import pam

class LoginHandler(BaseHandler):

    users_key = 'kvman_users'

    def get(self):
        if not self.session.isGuest:
            return self.redirect('/') # 已登录则跳转到首页
        next = self.get_argument("next", "/")
        self.render('user/login.html', next=next)

    # For PAM
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
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        remember = self.get_argument("remember", "no")
        if not username or not password: # 参数为空
            return self.returnJson({'code': -1, 'msg': u'用户名或密码错误(-1)！'})
        user_data = self.redis.hget(self.users_key,username)
        if not user_data: # 用户不存在
            return self.returnJson({'code': -2, 'msg': u'用户名或密码错误(-2)！'})
        print user_data
        return self.returnJson({'code': 0, 'msg': u'Successful'})



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
