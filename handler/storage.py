#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth
import libvirt


storage_type = {
    libvirt.VIR_CONNECT_LIST_STORAGE_POOLS_DIR: u'目录',
    libvirt.VIR_CONNECT_LIST_STORAGE_POOLS_LOGICAL: u'逻辑卷',
    libvirt.VIR_CONNECT_LIST_STORAGE_POOLS_NETFS: u'NFS',
    libvirt.VIR_CONNECT_LIST_STORAGE_POOLS_DISK: u'磁盘',
    libvirt.VIR_CONNECT_LIST_STORAGE_POOLS_FS: u'文件系统',
    libvirt.VIR_CONNECT_LIST_STORAGE_POOLS_SCSI: u'SCSI',
    libvirt.VIR_CONNECT_LIST_STORAGE_POOLS_ISCSI: u'iSCSI'
}


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

