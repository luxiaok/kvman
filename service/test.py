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

    # 获取虚拟机信息
    def getGuestInfo(self,name):
        guest = self.getGuest(name)
        print "Hostname: %s" % guest.hostname()
        ifaces = guest.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
        for (name, val) in ifaces.iteritems():
            if val['addrs']:
                for ipaddr in val['addrs']:
                    if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                        print ipaddr['addr'] + " VIR_IP_ADDR_TYPE_IPV4"
                    elif ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV6:
                        print ipaddr['addr'] + " VIR_IP_ADDR_TYPE_IPV6"


if __name__ == '__main__':
    k = kvm()
    k.getGuestInfo(sys.argv[1])
