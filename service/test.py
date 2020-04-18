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
        host = {
            'hostname': guest.hostname()
        }
        ifaces = guest.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
        ip = {}
        for (name, val) in ifaces.iteritems():
            ip[name] = {}
            if val['hwaddr']:
                ip[name]['mac'] = val['hwaddr']
            if val['addrs']:
                for ipaddr in val['addrs']:
                    if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                        #print ipaddr['addr'] + " VIR_IP_ADDR_TYPE_IPV4"
                        ip[name]['ipv4'] = ipaddr['addr']
                    elif ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV6:
                        #print ipaddr['addr'] + " VIR_IP_ADDR_TYPE_IPV6"
                        ip[name]['ipv6'] = ipaddr['addr']
        host['ip'] = ip
        return host


if __name__ == '__main__':
    k = kvm()
    print k.getGuestInfo(sys.argv[1])
