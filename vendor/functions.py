#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from random import Random
import hashlib

def hash(text='123456',type='md5'):
    if type == 'md5':
        return hashlib.md5(text).hexdigest()
    elif type == 'sha1':
        return hashlib.sha1(text).hexdigest()
    elif type == 'sha256':
        return hashlib.sha256(text).hexdigest()
    elif type == 'sha512':
        return hashlib.sha512(text).hexdigest()
    else:
        return text

# 生成指定长度的随机字符
def random_str(N=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(N):
        str += chars[random.randint(0, length)]
    return str
