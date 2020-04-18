Kvm Man
=========

Kvman = Kvm Man = Kernel-based Virtual Machine Manager


## Version

**v1.0.0-Beta**

![Kvm-Man](static/img/kvman-overview.jpg)


## Dependency Components

### Based environments

* CentOS 7.7 x86_64

* Python 2.7.xx


### Install Kvm requirements

```
yum update -y
yum install -y centos-release-qemu-ev
yum install -y qemu-kvm-ev qemu-kvm-common-ev qemu-img-ev qemu-kvm-tools-ev \
libvirt libvirt-python virt-install
```


### Python requirements

- [Python](http://www.python.org)：2.7.x

- [Torweb](https://github.com/xkstudio/Torweb)：1.0+

- [Tornado](http://www.tornadoweb.org/)：5.0+

- [Jinja2](http://jinja.pocoo.org/)：2.9+

- [Redis-Py](https://github.com/andymccurdy/redis-py)：2.10+

- [Libvirt](https://github.com/libvirt/libvirt-python): 2.0+

- [Supervisor](https://pypi.org/project/setuptools): 3.0+

> pip install tornado==5.1.1 supervisor==3.3.5 Jinja2 redis


## Run Kvman

* Install

> python run.py --install=1

* Run Kvman

> python run.py [--port=8080]


## Configure for Supervisor

```
[program:kvman]
command=/usr/bin/python2.7 run.py --port=8080 2>&1 >> /tmp/kvman.log
autorestart=false
autostart=false
directory=/var/www/kvman
redirect_stderr=true
stdout_logfile=/tmp/kvman.log
```


## Related Links

- [QEMU](https://www.qemu.org/download/)

- [Libvirt](http://libvirt.org/sources/)

- [VirtIO for Windows](https://docs.fedoraproject.org/en-US/quick-docs/creating-windows-virtual-machines-using-virtio-drivers/index.html)

- [Qemu-Guest-Agent](https://wiki.qemu.org/Features/GuestAgent)

- [OSX-KVM](https://github.com/kholia/OSX-KVM)

- [Linux-Kvm](https://www.linux-kvm.org/)