#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------------------
#   File Name :       createtable.py
#   Description :     添加基础表
#   Author :          zhoujie
#   Created:          2018/5/3 15:58
# -------------------------------------------------
#   Change Activity:
#                     2018/5/3
# -------------------------------------------------

import app
from app.model import *

app = app.create_app('default')

from app import db

with app.app_context():

     db.create_all()
     #db.drop_all()

     inbox = Category(name=u'收件箱')
     done = Category(name=u'已完成')
     #职位
     employee = Position(name=u'普通员工')
     director = Position(name=u'主管')
     #管理员
     department = Department(name=u'管理员', parent_id=1)
     #收费
     agreement1 = Agreement(name=u'代理记账', price=120)
     agreement2 = Agreement(name=u'代理报税', price=160)
     agreement3 = Agreement(name=u'代理注册', price=200)

     report1 = Report(content="hahahah", account_id=1)
     db.session.add_all([inbox, done, director, employee, department, agreement1, agreement2, agreement3,report1])
     db.session.commit()
