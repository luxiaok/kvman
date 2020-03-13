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
        status = [u'<span style="color:#ccc;">已关机</span>',u'<span style="color:green;">运行中</span>']
        self.render('guest/index.html',guests=guests,status=status)


class CreateGuestHandler(BaseHandler):

    def get(self):
        self.render('guest/create.html')

