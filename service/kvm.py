#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By Luxiaok

import libvirt
import json
import base64
import time
import os
from libvirt_qemu import qemuAgentCommand
from xml.dom import minidom
from PIL import Image


class kvm:


    os_type = [
        {
            'name': 'Linux',
            'os': [
                {'os_id': 'centos5.11', 'name': 'CentOS 5'},
                {'os_id': 'centos6.10', 'name': 'CentOS 6'},
                {'os_id': 'centos7.0', 'name': 'CentOS 7'},
                {'os_id': 'rhel8.0', 'name': 'CentOS 8'},
                {'os_id': 'rhel5.11', 'name': 'RHEL 5'},
                {'os_id': 'rhel6.10', 'name': 'RHEL 6'},
                {'os_id': 'rhel7.8', 'name': 'RHEL 7'},
                {'os_id': 'rhel8.0', 'name': 'RHEL 8'},
                {'os_id': 'ubuntu18.04', 'name': 'Ubuntu'},
                {'os_id': 'fedora29', 'name': 'Fedora'},
                {'os_id': 'ubuntu18.04', 'name': 'OpenWrt'},
                {'os_id': 'centos6.10', 'name': 'Other Linux kernel OS'},
            ]
        },
        {
            'name': 'Windows',
            'os': [
                {'os_id': 'win2k3', 'name': 'Windows Server 2003'},
                {'os_id': 'win2k8', 'name': 'Windows Server 2008'},
                {'os_id': 'winxp', 'name': 'Windows XP'},
                {'os_id': 'win7', 'name': 'Windows 7'},
                {'os_id': 'win8', 'name': 'Windows 8'},
                {'os_id': 'win10', 'name': 'Windows 10'},
            ]
        },
        {
            'name': 'Android',
            'os': [
                {'os_id': '', 'name': 'Android x86 4.0'},
                {'os_id': '', 'name': 'Android x86 5.0'},
                {'os_id': '', 'name': 'Android x86 6.0'},
                {'os_id': '', 'name': 'Android x86 7.0'},
                {'os_id': '', 'name': 'Android x86 8.0'},
                {'os_id': '', 'name': 'Android x86 9.0'},
            ]
        },
        {
            'name': 'MacOS',
            'os': [
                {'os_id': 'macosx10.7', 'name': 'macOS Sierra 10.12.6'},
                {'os_id': 'macosx10.7', 'name': 'macOS High Sierra 10.13.6'},
                {'os_id': 'macosx10.7', 'name': 'macOS Mojave 10.14.6'},
                {'os_id': 'macosx10.7', 'name': 'macOS Catalina 10.15.4'},
            ]
        }
    ]


    def __init__(self,uri=None):
        #print 'Init kvm service ...'
        self.code = 0
        self.msg = 'success'
        self.uri = None
        if uri:
            if isinstance(uri,str):
                self.uri = uri
            elif isinstance(uri,dict):
                self.uri = self.getUri(uri)
        self.conn = self.openConnect(self.uri)
        #print self.conn.getVersion() # Qemu
        #print self.conn.getLibVersion() # Libvirt
        #print self.conn.getSysinfo() # System Infomation
        #print self.conn.getHostname() # Hostname for Kvm Server


    def getUri(self,config=None):
        if not config:
            return None
        if config['protocol'] == 'qemu' and config['hostname'] in ['localhost','127.0.0.1']:
            uri = 'qemu:///system'
        elif config['protocol'] in ['qemu+ssh','qemu+libssh2','qemu+libssh']:
            if config['port']:
                uri = '%s://%s@%s:%s/system' % (config['protocol'], config['username'], config['hostname'], config['port'])
            else:
                uri = '%s://%s@%s/system' % (config['protocol'], config['username'], config['hostname'])
        elif config['protocol'] == 'qemu+tcp':
            if config['port']:
                uri = '%s://%s:%s/system' % (config['protocol'], config['hostname'], config['port'])
            else:
                uri = '%s://%s/system' % (config['protocol'], config['hostname'])
        else:
            if config['port']:
                uri = '%s://%s:%s/system' % (config['protocol'],config['hostname'],config['port'])
            else:
                uri = '%s://%s/system' % (config['protocol'], config['hostname'])
        if config.get('parameters'):
            uri = '%s?%s' % (uri,config['parameters'])
        return uri


    def openConnect(self,uri):
        if not uri:
            self.code = -500
            self.msg = 'Not uri'
            return None
        try:
            # conn = libvirt.openReadOnly(uri)
            conn = libvirt.open(uri)
        except libvirt.libvirtError, e:
            self.code = -501
            self.msg = e.message
            conn = None
        except Exception, e:
            self.code = -502
            self.msg = e.message
            conn = None
        return conn


    def close(self):
        self.conn.close()


    def getVersion(self):
        if not self.conn:
            return {
                'libvirt': 'UnKnown',
                'qemu': 'UnKnown'
            }
        lv = str(self.conn.getLibVersion())
        qv = str(self.conn.getVersion())
        libvirt_version = [str(lv[0]),str(int(lv[1:4])),str(int(lv[4:]))]
        qemu_version = [str(qv[0]),str(int(qv[1:4])),str(int(qv[4:]))]
        return {
            'libvirt': '.'.join(libvirt_version),
            'qemu': '.'.join(qemu_version)
        }


    def getGuestsNum(self):
        if not self.conn:
            return ''
        return len(self.conn.listAllDomains(0))


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
        except libvirt.libvirtError, e:
            dom = None
            self.code = -1
            self.msg = e.message
        except Exception, e:
            dom = None
            self.code = -2
            self.msg = 'Not found guest: ' + name
        return dom


    def qemuAgentCommand(self,guest,cmd,timeout=3,flag=0):
        try:
            stuff = qemuAgentCommand(guest, cmd, timeout, flag)
            result = json.loads(stuff)
            data = result['return']
        except Exception, e:
            #print e.message
            data = {}
        return data


    def getVncPort(self,name):
        if not self.conn:
            return 0
        guest = self.getGuest(name)
        raw_xml = guest.XMLDesc(0)
        xml = minidom.parseString(raw_xml)
        graphics = xml.getElementsByTagName('graphics')
        port = -1
        for i in graphics:
            if i.getAttribute('type') == 'vnc':
                port = i.getAttribute('port')
                #address = i.getAttribute('listen')
                #print "VNC: %s - %s" % (address,port)
            #listen = i.getElementsByTagName('listen')
            #for x in listen:
            #    print 'VNC Listen: %s - %s' % (x.getAttribute('type'),x.getAttribute('address'))
        return int(port)


    def getGuestUUID(self,name):
        if not self.conn:
            return None
        guest = self.getGuest(name)
        return guest.UUIDString()


    # disks = xml.getElementsByTagName('disk')
    def getDisk(self,disks):
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


    def getInterfaces(self,interfaces):
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
        if not self.conn:
            return guests
        doms = self.conn.listAllDomains(0)
        for i in doms:
            raw_xml = i.XMLDesc(0)
            xml = minidom.parseString(raw_xml)
            #tag_title = xml.getElementsByTagName('title')
            #title = tag_title[0].childNodes[0].nodeValue if len(tag_title) > 0 else ''
            #tag_desc = xml.getElementsByTagName('description')
            #desc = tag_desc[0].childNodes[0].nodeValue if len(tag_desc) > 0 else ''
            state,maxmem,mem,cpus,cpu_time = i.info()
            hdd = self.getDisk(xml.getElementsByTagName('disk'))
            network = self.getInterfaces(xml.getElementsByTagName('interface'))
            state,reason = i.state()
            dom = {
                'id': i.ID(),
                'name': i.name(),
                'title': i.metadata(libvirt.VIR_DOMAIN_METADATA_TITLE,None),
                'desc': i.metadata(libvirt.VIR_DOMAIN_METADATA_DESCRIPTION,None),
                'os_type': i.OSType(), # return "hvm", useless!
                'cpu': cpus,
                'mem': self.formatNum( mem * 1024 ), # unit: KiB
                'hdd': hdd,
                'network': network,
                'autostart': i.autostart(),
                'state': state,
                'status': i.isActive()
            }
            guests.append(dom)
        return sorted(guests,key=lambda item : item['name'].lower()) # Sort by Name


    def getIPAddress(self,guest,ignore127=True,ignoreIPv6=True):
        ifaces = guest.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
        ip = []
        interfaces = {}
        for (name, val) in ifaces.iteritems():
            interfaces[name] = {'name': name}
            if name == 'lo': continue
            if val['hwaddr']:
                interfaces[name]['mac'] = val['hwaddr']
            if val['addrs']:
                for ipaddr in val['addrs']:
                    if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                        if ipaddr['addr'].startswith('127.0') and ignore127:
                            del(interfaces[name])
                            continue
                        interfaces[name]['ipv4'] = {'address': ipaddr['addr'], 'netmask': ipaddr['prefix']}
                        ip.append(ipaddr['addr'])
                    elif ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV6 and not ignoreIPv6:
                        interfaces[name]['ipv6'] = {'address': ipaddr['addr'], 'netmask': ipaddr['prefix']}
        return {'ip':ip,'interfaces':interfaces}


    # 开机时间：Just for Linux
    def getBootTime(self,guest):
        cmd = '{"execute": "guest-exec","arguments":{"path":"/bin/cat","arg":["/proc/uptime"],"capture-output":true}}'
        data = self.qemuAgentCommand(guest,cmd)
        pid = data['pid']
        time.sleep(2)
        cmd = '{"execute": "guest-exec-status","arguments":{"pid":%s}}' % pid
        data = self.qemuAgentCommand(guest,cmd) # exitcode:0,out-data:Base64Encode,exited:true
        result = base64.b64decode(data['out-data'])
        uptime = result.split(' ')
        return int(time.time()-float(uptime[0]))


    def getGuestDetail(self,name):
        if not self.conn:
            return None
        guest = self.getGuest(name)
        raw_xml = guest.XMLDesc(0)
        xml = minidom.parseString(raw_xml)
        state, maxmem, mem, cpus, cpu_time = guest.info()
        hdd = self.getDisk(xml.getElementsByTagName('disk'))
        network = self.getInterfaces(xml.getElementsByTagName('interface'))
        state, reason = guest.state()
        # Get VNC Port
        graphics = xml.getElementsByTagName('graphics')
        vnc_port = -1
        for i in graphics:
            if i.getAttribute('type') == 'vnc':
                vnc_port = i.getAttribute('port')
        qga_version = self.qemuAgentCommand(guest,'{"execute": "guest-info"}')
        if qga_version:
            qga_version = qga_version['version']
        else:
            qga_version = ''
        guest_os = self.qemuAgentCommand(guest,'{"execute": "guest-get-osinfo"}')
        if guest_os:
            guest_os = guest_os.get('pretty-name','')
        else:
            guest_os = ''
        try:
            hostname = guest.hostname()
            ip = self.getIPAddress(guest)
        except Exception, e:
            #print e.message # Guest agent is not responding: QEMU guest agent is not connected
            hostname = ''
            ip = {'ip':[]}
        detail = {
            'id': guest.ID(),
            'uuid': guest.UUIDString(),
            'name': guest.name(),
            'hostname': hostname,
            'ip': ip['ip'] or network,
            'title': guest.metadata(libvirt.VIR_DOMAIN_METADATA_TITLE, None),
            'desc': guest.metadata(libvirt.VIR_DOMAIN_METADATA_DESCRIPTION, None),
            'os_type': guest.OSType(),  # return "hvm", useless!
            'os': guest_os,
            'cpu': cpus,
            'mem': self.formatNum(mem * 1024),  # unit: KiB
            'hdd': hdd,
            'network': network,
            'vnc_port': vnc_port,
            'autostart': guest.autostart(),
            'qga_version': qga_version,
            #'uptime': self.getBootTime(guest),
            'xml': raw_xml,
            'state': state,
            'status': guest.isActive()
        }
        return detail


    def setAutostart(self,name,flag):
        guest = self.getGuest(name)
        return guest.setAutostart(flag)


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
            self.code = -1
            self.msg = 'Halt failed'
            return False


    def rebootGuest(self,name):
        dom = self.getGuest(name)
        if not dom:
            return False
        if dom.reboot() == 0:
            return True
        else:
            self.code = -1
            self.msg = 'Reboot fail'
            return False


    def getStoragePools(self):
        storages = []
        if not self.conn:
            return storages
        pools = self.conn.listAllStoragePools(0)
        for i in pools:
            info = i.info()
            raw_xml = i.XMLDesc(0)
            xml = minidom.parseString(raw_xml)
            sp = {
                'name': i.name(),
                'uuid': i.UUIDString(),
                'size': self.formatNum(info[1]),
                'used': self.formatNum(info[2]),
                'free': self.formatNum(info[3]),
                'type': xml.getElementsByTagName('pool')[0].getAttribute('type'),
                'vol_num': i.numOfVolumes(),
                'vols': i.listVolumes(),
                'autostart': i.autostart(),
                'active': i.isActive(),
                'state': info[0]
            }
            storages.append(sp)
        return sorted(storages,key=lambda item : item['name'].lower()) # Sort by name


    def getStorageVols(self,pool):
        vols = []
        if not self.conn:
            return vols
        try:
            pl = self.conn.storagePoolLookupByName(pool)
        except Exception, e:
            self.code = -1
            self.msg = e.message
            return vols
        vls = pl.listVolumes()
        for i in vls:
            vol = pl.storageVolLookupByName(i)
            info = vol.info()
            _vl = {
                'name': i,
                'type': info[0],
                'path': vol.path(),
                'total': self.formatNum(info[1]),
                'used': self.formatNum(info[2])
            }
            vols.append(_vl)
        return sorted(vols,key=lambda item : item['name'].lower()) # 按name字段排序，忽略大小写！！！


    # 刷新存储池
    def refreshStorage(self,pool_name):
        pool = self.conn.storagePoolLookupByName(pool_name)
        return pool.refresh()


    # 获取网卡流量，仅限Kvm本机
    def getNetworkTraffic(self,interface='eth0'):
        f = open('/proc/net/dev','r')
        content = f.readlines()
        f.close()
        filter = '%s:' % interface # ':' is important!!!
        traffic_in = 0
        traffic_out = 0
        for line in content:
            if filter in line:
                raw = line.split()
                traffic_in = raw[1]
                traffic_out = raw[9]
                break
        return {'in': self.formatNum(int(traffic_in)), 'out': self.formatNum(int(traffic_out))}


    def getNetworks(self):
        networks = []
        if not self.conn:
            return networks
        net_lists = self.conn.listNetworks()
        for i in net_lists:
            network = self.conn.networkLookupByName(i)
            raw_xml = network.XMLDesc(0)
            xml = minidom.parseString(raw_xml)
            ip = xml.getElementsByTagName('ip')
            traffic = self.getNetworkTraffic(network.bridgeName())
            data = {
                'name': i,
                'uuid': network.UUIDString(),
                'autostart': network.autostart(),
                'bridge': network.bridgeName(),
                'ip': ip[0].getAttribute('address'),
                'netmask': ip[0].getAttribute('netmask'),
                'dhcp': len(network.DHCPLeases()),
                'traffic_in': traffic['in'],
                'traffic_out': traffic['out'],
                'active': network.isActive()
            }
            networks.append(data)
        return sorted(networks,key=lambda item : item['name']) # Sort by name


    def screenshotHandler(self,stream, buf, fd):
        os.write(fd, buf)


    def screenshot(self,name,filename='screenshot.pbm'):
        domain = self.getGuest(name)
        stream = self.conn.newStream(0)
        mimetype = domain.screenshot(stream, 0, 0)
        #print "MIME Type:", mimetype ### image/x-portable-pixmap
        fd = os.open(filename, os.O_WRONLY | os.O_TRUNC | os.O_CREAT, 0644)
        stream.recvAll(self.screenshotHandler, fd)


    def convertImg(self,raw,pic):
        try:
            img = Image.open(raw)
            img.convert('RGB').save(os.getcwd()+pic)
            img.close()
            os.remove(raw)
        except:
            pic = ''
            self.code = -1
            self.msg = u'生成控制台缩率图失败(-1)'
        return pic


    def getScreenshotImg(self,name,force=False):
        app_dir = os.getcwd()
        base_dir = 'static/img/console'
        filename_raw = '%s/%s/%s.pbm' % (app_dir, base_dir, name)
        filename_img = '/%s/%s.jpg' % (base_dir, name)
        filename_img_full_path = app_dir + filename_img
        guest = self.getGuest(name)
        if guest.isActive():
            if force:
                self.screenshot(name, filename_raw)
                return self.convertImg(filename_raw,filename_img)
            elif os.path.exists(filename_img_full_path):
                stat = os.stat(filename_img_full_path)
                if time.time() - stat.st_mtime > 300:
                    #print 'More than 300 Seconds'
                    self.screenshot(name,filename_raw)
                    return self.convertImg(filename_raw, filename_img)
                else:
                    #print 'Less 300 Seconds'
                    return filename_img
            else:
                self.screenshot(name, filename_raw)
                return self.convertImg(filename_raw, filename_img)
        else:
            self.code = -1
            self.msg = u'已关机'
            return ''

