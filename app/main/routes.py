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
from flask_login import current_user, login_required
from datetime import datetime
from flask import render_template, g
from app.main import view
from app import db
from app.model import Customer, User, Employee
from app.main.forms  import  customerForm

# 首页
@view.route('/index')
def index():
    return render_template('index.html')

# 客户
@view.route('/customer', methods=('GET', 'POST'))
def customer():
    return render_template('customer.html')

@view.route('/customer/list')
def customer_list():
    form = customerForm
    accountId = db.session.query(User.account_id).filter_by(id = 1)
    positionId = db.session.query(Employee.position_id).filter_by(id = accountId)
    if (positionId == 1):

        departmentId = db.session.query(Employee.department_id).filter_by(id = accountId)

        managerid = db.session.query(Employee.id).filter_by(department_id = departmentId)

    customer = db.session.query_property(Customer.name,Customer.phone,Customer.address,Customer.email).filter_by(account_id = managerid)

    #customer = Customer.query.filter_by(account_id=current_user).all()  # 查询客户表里符合客户经理的所有数据

    return customer
# 合同
@view.route('/contract')
def contract():
    return render_template('contract.html')





