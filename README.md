Kvm Man
=========

Kvman = Kvm Man = Kernel-based Virtual Machine Manager


## Version

**v1.0.0-Beta**

![Kvm-Man](static/img/kvman-overview.jpg)


## Dependency Components

### Install Kvm requirements

```
yum update -y
yum install -y centos-release-qemu-ev
yum install -y qemu-kvm-ev qemu-kvm-common-ev qemu-img-ev qemu-kvm-tools-ev libvirt libvirt-python virt-install
```

### Python requirements

- [Python](http://www.python.org)：2.7.x

- [Torweb](https://github.com/xkstudio/Torweb)：1.0+

- [Tornado](http://www.tornadoweb.org/)：5.0+

- [Jinja2](http://jinja.pocoo.org/)：2.9+

- [Redis-Py](https://github.com/andymccurdy/redis-py)：2.10+

- [Libvirt](https://github.com/libvirt/libvirt-python): 2.0+

> pip install tornado==5.1.1 supervisor==3.3.5 Jinja2 redis


## Run Kvman

* Install

> python run.py --install=1

* Run Kvman

> python run.py [--port=8080]
