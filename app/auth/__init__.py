# -*- coding: utf-8 -*-

# -------------------------------------------------
#   File Name :       __init__.py
#   Description :     添加描述信息
#   Author :          zhoujie
#   Created:          2018/1/21  16:24 
# -------------------------------------------------
#   Change Activity:
#                     2018/1/21
# -------------------------------------------------

from flask import Blueprint

view = Blueprint('auth', __name__)

from app.auth import route



