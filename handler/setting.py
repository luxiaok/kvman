#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from BaseHandler import BaseHandler
#from tornado.web import authenticated as Auth


class IndexHandler(BaseHandler):

    #@Auth
    def get(self):
        self.title = u'系统设置'
        self.render('setting/index.html')


    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        protocol = self.get_argument('protocol')
        hostname = self.get_argument('hostname')
        qemu_username = self.get_argument('qemu_username')
        qemu_password = self.get_argument('qemu_password')

