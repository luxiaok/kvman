#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth
from service.kvm import kvm

class IndexHandler(BaseHandler):

    @Auth
    def get(self):
        k = kvm()
        networks = k.getNetworks()
        self.render('network/index.html',data=networks)
