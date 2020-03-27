#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By Luxiaok

import libvirt
from xml.dom import minidom
from config.settings import config


class kvm:


    VIR_DOMAIN_NOSTATE = libvirt.VIR_DOMAIN_NOSTATE
    VIR_DOMAIN_RUNNING = libvirt.VIR_DOMAIN_RUNNING
    VIR_DOMAIN_BLOCKED = libvirt.VIR_DOMAIN_BLOCKED
    VIR_DOMAIN_PAUSED = libvirt.VIR_DOMAIN_PAUSED
    VIR_DOMAIN_SHUTDOWN = libvirt.VIR_DOMAIN_SHUTDOWN
    VIR_DOMAIN_SHUTOFF = libvirt.VIR_DOMAIN_SHUTOFF
    VIR_DOMAIN_CRASHED = libvirt.VIR_DOMAIN_CRASHED
    VIR_DOMAIN_PMSUSPENDED = libvirt.VIR_DOMAIN_PMSUSPENDED


    def __init__(self):
        uri = 'qemu:///system'
        self.conn = self.openConnect(uri)
        #print self.conn.getVersion() # Qemu
        #print self.conn.getLibVersion() # Libvirt
        #print self.conn.getSysinfo() # System Infomation
        #print self.conn.getHostname() # Hostname for Kvm Server
        self._code = 0
        self._msg = 'success'


    def openConnect(self,uri):
        #return libvirt.openReadOnly(uri)
        return libvirt.open(uri)


    def close(self):
        self.conn.close()


    def getVersion(self):
        lv = str(self.conn.getLibVersion())
        qv = str(self.conn.getVersion())
        libvirt_version = [str(lv[0]),str(int(lv[1:4])),str(int(lv[4:]))]
        qemu_version = [str(qv[0]),str(int(qv[1:4])),str(int(qv[4:]))]
        return {
            'libvirt': '.'.join(libvirt_version),
            'qemu': '.'.join(qemu_version)
        }


    # num = xxxxx bytes
    def formatNum(self,num):
        s = num / 1024.0
        if s < 1024:
            human_num = int(s) if s == int(s) else "%.2f" % s
            return "%s %s" % (human_num,'KB')
        s = s / 1024
        if s < 1024:
            human_num = int(s) if s == int(s) else "%.2f" % s
            return "%s %s" % (human_num,'MB')
        s = s / 1024
        if s < 1024:
            human_num = int(s) if s == int(s) else "%.2f" % s
            return "%s %s" % (human_num, 'GB')
        s = s / 1024
        if s < 1024:
            human_num = int(s) if s == int(s) else "%.2f" % s
            return "%s %s" % (human_num, 'TB')


    def getGuest(self,name):
        try:
            dom = self.conn.lookupByName(name)
        except:
            dom = None
            self._code = -1
            self._msg = 'Not found guest: ' + name
        return dom


    # disks = xml.getElementsByTagName('disk')
    def getHdd(self,disks):
        hdd = []
        type_to_path = {'file': 'file', 'block': 'dev'}
        for d in disks:
            if d.getAttribute('device') == 'disk': # disk or cdrom
                hdd_type = d.getAttribute('type')  # file or block
                hddNodes = d.childNodes
                for n in hddNodes:
                    if n.nodeName == 'source':
                        hdd_path = n.getAttribute(type_to_path[hdd_type])  # hdd src, eg: /kvm/images/guest.img
                        vol = self.conn.storageVolLookupByPath(hdd_path)
                        info = vol.info()
                        total = self.formatNum(info[1])
                        used = self.formatNum(info[2])
                        hdd.append("%s / %s" % (used, total))
        return hdd


    def getNetwork(self,interfaces):
        net = []
        for i in interfaces:
            type = i.getAttribute('type')
            iNodes = i.childNodes
            mac,link,drive = ('','','')
            for tag in iNodes:
                if tag.nodeName == 'mac':
                    mac = tag.getAttribute('address')
                elif tag.nodeName == 'source':
                    link = tag.getAttribute(type) # kvm network pool name,eg: default,br0,...
                elif tag.nodeName == 'model':
                    drive = tag.getAttribute('type') # e1000,virtio,...
                else:
                    pass
            net.append('%s -> %s' % (mac,link))
        return net


    def getGuests(self):
        guests = []
        doms = self.conn.listAllDomains(0)
        for i in doms:
            raw_xml = i.XMLDesc(0)
            xml = minidom.parseString(raw_xml)
            tag_title = xml.getElementsByTagName('title')
            title = tag_title[0].childNodes[0].nodeValue if len(tag_title) > 0 else ''
            tag_desc = xml.getElementsByTagName('description')
            desc = tag_desc[0].childNodes[0].nodeValue if len(tag_desc) > 0 else ''
            state,maxmem,mem,cpus,cpu_time = i.info()
            hdd = self.getHdd(xml.getElementsByTagName('disk'))
            network = self.getNetwork(xml.getElementsByTagName('interface'))
            state,reason = i.state()
            dom = {
                'id': i.ID(),
                'name': i.name(),
                'title': title,
                'desc': desc,
                'os_type': i.OSType(), # return "hvm", useless!
                'cpu': cpus,
                'mem': self.formatNum( mem * 1024 ), # unit: KiB
                'hdd': hdd,
                'network': network,
                'state': state,
                'status': i.isActive()
            }
            guests.append(dom)
        return guests


    def startGuest(self,name):
        dom = self.getGuest(name)
        if not dom:
            return False
        if dom.create() < 0:
            return False
        else:
            return True


    def shutdownGuest(self,name,force=False):
        dom = self.getGuest(name)
        if not dom:
            return False
        if force:
            result = dom.destroy()
        else:
            result = dom.shutdown()
        if result == 0:
            return True
        else:
            self._code = -1
            self._msg = 'Halt failed'
            return False


    def rebootGuest(self,name):
        dom = self.getGuest(name)
        if not dom:
            return False
        if dom.reboot() == 0:
            return True
        else:
            self._code = -1
            self._msg = 'Reboot fail'
            return False


    def getStoragePools(self):
        storages = self.conn.listAllStoragePools()
        #print storages[1].name()
        #print storages[1].info()
        #print storages[1].listVolumes()
        return storages
