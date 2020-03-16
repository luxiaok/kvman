#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# Guests

from BaseHandler import BaseHandler
from service.kvm import kvm
#from tornado.web import authenticated as Auth

class IndexHandler(BaseHandler):

    #@Auth
    def get(self):
        k = kvm()
        guests = k.getGuests()
        k.close()
        status = [u'<span style="color:#ccc;">已关机</span>',u'<span style="color:green;">运行中</span>']
        self.title = u'虚拟机实例'
        self.render('guest/index.html',guests=guests,status=status)


class CreateGuestHandler(BaseHandler):

    def get(self):
        self.title = u'创建虚拟机'
        self.render('guest/create.html')


class DetailHandler(BaseHandler):

    def get(self):
        name = self.get_argument('name')
        self.title = u'虚拟机详情 - ' + name
        self.render('guest/detail.html',name=name)

