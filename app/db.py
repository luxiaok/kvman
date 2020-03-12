#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

import MySQLdb

# Wrapper MySQL
class DB:

    def __init__(self,host,port,user,passwd,db,charset="utf8"):
        self._conn = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        self._cur = self._conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)

    def close(self):
        self._cur.close()
        self._conn.close()

    def select(self,sql):
        self._cur.execute(sql)
        return self._cur.fetchall()

    def get(self,sql):
        self._cur.execute(sql)
        return self._cur.fetchone()

    def update(self,sql):
        pass

    def delete(self,sql):
        pass

    def insert(self,sql):
        pass
