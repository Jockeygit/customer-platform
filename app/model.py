# -*- coding: utf-8 -*-

# -------------------------------------------------
#   File Name :       model
#   Description :     本系统所有数据表的模型
#   Author :          zhoujie
#   Created:          2018/4/28  15:46 
# -------------------------------------------------
#   Change Activity:
#                     2018/4/28
# -------------------------------------------------
from app import db
from datetime import datetime

# 员工表
class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False, unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True, unique=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=True, unique=True)

# 部门表
class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False, unique=True)

# 职位表
class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False, unique=True)

# 客户表
class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False, unique=True)
    type = db.Column(db.Integer, nullable=False, unique=False)
    phone = db.Column(db.String(30), nullable=True, unique=False)
    email = db.Column(db.String(30), nullable=True, unique=False)
    address = db.Column(db.String(35), nullable=True, unique=False)
    # account_id引用employee表中的id
    account_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False, unique=True)

# 合同表
class Contract(db.Model):
    __tablename__ = 'contract'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False, unique=False)
    expiry_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    isCheck = db.Column(db.Boolean, nullable=False, unique=False)
    # agreement_id引用agreement表的id
    agreement_id = db.Column(db.Integer, db.ForeignKey('agreement.id'), nullable=True, unique=True)
    # customer_id引用customer表的id
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, unique=True)

# 服务项目表
class Agreement(db.Model):
    __tablename__ = 'agreement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False, unique=True)

# 收费记录表
class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=True, unique=False)
    charge = db.Column(db.Integer, nullable=False, unique=False)
    charge_date = db.Column(db.Date, nullable=False, unique=False)
    # contract_id引用contract表的id
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'), nullable=False, unique=True)

# 合同-服务项目表
# class Contract_Agreement(db.Model):
#    __tablename__ = 'contract_agreement'
 #   id = db.Column(db.Integer, primary_key=True)
  #  contract_id = db.Column(db.Integer, nullable=False, unique=True)
   # agreement_id = db.Column(db.Integer, nullable=False, unique=True)

# 待办事项表
class Todolist(db.Model):
    __tablename__ = "todolist"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False, unique=False)
    # account_id引用employee表的id
    account_id = db.Column(db.Integer, nullable=False, unique=True)
