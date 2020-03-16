#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio


from BaseHandler import BaseHandler
#from tornado.web import authenticated as Auth

class IndexHandler(BaseHandler):

    #@Auth
    def get(self):
        self.title = u'网络'
        self.render('network/index.html')
