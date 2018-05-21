# -*- coding: utf-8 -*-

# -------------------------------------------------
#   File Name :       createtable
#   Description :     添加描述信息
#   Author :          zhoujie
#   Created:          2018/5/3  13:38 
# -------------------------------------------------
#   Change Activity:
#                     2018/5/3
# -------------------------------------------------
import app

app = app.create_app('default')

from app import db
from app.model import Department, Position

with app.app_context():

    db.create_all()
    #db.drop_all()