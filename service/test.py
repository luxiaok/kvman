#!/usr/bin/python
# -*- coding:utf8 -*-
# Powered By XK Studio

import libvirt
import sys
from xml.dom import minidom

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
            'title': guest.metadata(libvirt.VIR_DOMAIN_METADATA_TITLE,None),
            'description': guest.metadata(libvirt.VIR_DOMAIN_METADATA_DESCRIPTION,None),
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


    # get metadata
    def getMetaData(self,name,uri='https://github.com/luxiaok/kvman'):
        guest = self.getGuest(name)
        flag = libvirt.VIR_DOMAIN_AFFECT_CONFIG
        stuff = guest.metadata(libvirt.VIR_DOMAIN_METADATA_ELEMENT,uri,flag)
        print stuff
        doc = minidom.parseString(stuff)
        print doc


    # set metadata
    def setMetaData(self,name,key='kvman',uri='https://github.com/luxiaok/kvman'):
        guest = self.getGuest(name)
        flag = libvirt.VIR_DOMAIN_AFFECT_CONFIG
        data = '<instance test="11"><foo type="22">Foo</foo><bar type="33"></bar></instance>'
        ret = guest.setMetadata(libvirt.VIR_DOMAIN_METADATA_ELEMENT, data, key, uri, flag)
        print ret


def info(k,name):
    info = k.getGuestInfo(name)
    for i in info:
        print '===== %s =====' % i
        print info[i]

def metadata(k,name):
    k.setMetaData(name)
    k.getMetaData(name)


if __name__ == '__main__':
    name = sys.argv[1]
    k = kvm()
    #info(k,name)
    metadata(k,name)
