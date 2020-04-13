#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# Server Page

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth
#from service.kvm import kvm


class IndexHandler(BaseHandler):

    #@Auth
    def get(self):
        #k = kvm()
        self.title = u'服务器'
        self.render('server/index.html')
