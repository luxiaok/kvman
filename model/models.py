#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from sqlalchemy import Column, Integer, SmallInteger, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'kvm_users'

    id = Column(Integer,primary_key=True,autoincrement=True)
    nickname = Column(VARCHAR(64), nullable=False)
    username = Column(VARCHAR(32),nullable=False,unique=True)
    password = Column(VARCHAR(128),nullable=False)
    email = Column(VARCHAR(32),nullable=True,unique=True)
    role = Column(SmallInteger,nullable=True)
    login_count = Column(Integer,nullable=True)
    login_time = Column(Integer, nullable=True)
    login_ua = Column(VARCHAR(500),nullable=True)
    login_ip = Column(VARCHAR(64),nullable=True)
    #login_location = Column(VARCHAR(32),nullable=True)
    create_time = Column(Integer,nullable=True)
    update_time = Column(Integer,nullable=True)
    status = Column(SmallInteger,nullable=True)
