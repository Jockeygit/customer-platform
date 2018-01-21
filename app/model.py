# -*- coding: utf-8 -*-

# -------------------------------------------------
#   File Name :       models
#   Description :     添加描述信息
#   Author :          zhoujie
#   Created:          2018/1/14  15:05 
# -------------------------------------------------
#   Change Activity:
#                     2018/1/14
# -------------------------------------------------
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False, unique=True)
    password = db.Column(db.String(24), nullable=False, unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

