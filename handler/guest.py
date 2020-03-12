#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# Guests

from BaseHandler import BaseHandler
#from tornado.web import authenticated as Auth

class IndexHandler(BaseHandler):

    #@Auth
    def get(self):
        self.log.info('Guest list') # Log Test
        self.render('guest/index.html')
