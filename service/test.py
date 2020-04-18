#!/usr/bin/python
# -*- coding:utf8 -*-
# Powered By XK Studio

import libvirt
import sys

class kvm:

    def __init__(self,uri='qemu:///system'):
        self.conn = libvirt.open(uri)


    def getGuest(self,name):
        return self.conn.lookupByName(name)

    # 获取主机名
    def getHostname(self,name):
        guest = self.getGuest(name)
        print guest.hostname()

if __name__ == '__main__':
    k = kvm()
    k.getHostname(sys.argv[1])
