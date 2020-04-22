#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# Server Page

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth
from service.kvm import kvm


class IndexHandler(BaseHandler):

    @Auth
    def get(self):
        servers = self.get_kvm_server()
        for i in servers:
            k = kvm(config=i)
            i['guests'] = k.getGuestsNum()
        self.render('server/index.html',data=servers)
