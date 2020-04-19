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
        interfaces = {}
        for (name, val) in ifaces.iteritems():
            interfaces[name] = {'name': name}
            if val['hwaddr']:
                interfaces[name]['mac'] = val['hwaddr']
            if val['addrs']:
                for ipaddr in val['addrs']:
                    if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                        interfaces[name]['ipv4'] = {'address': ipaddr['addr'], 'netmask': ipaddr['prefix']}
                    elif ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV6:
                        interfaces[name]['ipv6'] = {'address': ipaddr['addr'], 'netmask': ipaddr['prefix']}
        host['interfaces'] = interfaces
        return host


if __name__ == '__main__':
    k = kvm()
    print k.getGuestInfo(sys.argv[1])
