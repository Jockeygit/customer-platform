# -*- coding: utf-8 -*-

# -------------------------------------------------
#   File Name :       route
#   Description :     添加描述信息
#   Author :          zhoujie
#   Created:          2018/1/21  16:43 
# -------------------------------------------------
#   Change Activity:
#                     2018/1/21
# -------------------------------------------------
from flask import render_template
from app.main import view
from flask_login import login_user, logout_user, login_required


# 首页
@view.route('/index')
@login_required
def index():
    return render_template('index.html')

# 客户
@view.route('/customer')
@login_required
def customer():
    return render_template('customer.html')






