#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth


class IndexHandler(BaseHandler):

    @Auth
    def get(self):
        storages = self.kvm.getStoragePools()
        self.render('storage/index.html',storages=storages)


class VolumeHandler(BaseHandler):

    @Auth
    def get(self):
        pool = self.get_argument('pool')
        vols = self.kvm.getStorageVols(pool)
        self.render('storage/volume.html',vols=vols,pool=pool)


# 刷新存储池
class RefreshStorageHandler(BaseHandler):

    @Auth
    def post(self):
        pool = self.get_argument('pool')
        self.kvm.refreshStorage(pool)
        self.returnJson({'code': 0, 'msg': u'刷新成功！'})
