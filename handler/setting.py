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

    @Auth
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        protocol = self.get_argument('protocol')
        hostname = self.get_argument('hostname')
        qemu_username = self.get_argument('qemu_username')
        qemu_password = self.get_argument('qemu_password')


    # 初始化时创建用户
    def create_user(self,username,password):
        data = {
            'uid': 1000,
            'username': username,
            'password': password,
            'reg_time': int(time.time())
        }
        self.redis.hset(self.users_key,username,json.dumps(data))

