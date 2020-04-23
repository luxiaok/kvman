#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth


class IndexHandler(BaseHandler):

    @Auth
    def get(self):
        sid = self.get_argument('sid', None)
        k = self.kvm(sid)
        if k:
            networks = k.getNetworks()
        else:
            networks = []
        self.render('network/index.html',sid=sid,data=networks)
