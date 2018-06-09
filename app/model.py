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
from werkzeug.security import generate_password_hash, check_password_hash
import sys
sys.path.append("..")
from app import db, create_app
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False, unique=True)
    password = db.Column(db.String(24), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    head_image = db.Column(db.String(252), nullable=True)
    # account_id引用employee表中的id
    account_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False, unique=True)

    def __init__(self, username, password, account_id):
        self.username = username
        self.password = password
        self.account_id = account_id

    @property
    def password(self):
        """
        设置密码的只写属性
        """
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        """
        为密码hash赋值
        :param password: 原密码
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        对比输入密码与模型中的hash是否相等
        :param password:需要对比的密码
        :return:True即为密码正确
        """
        return check_password_hash(self.password_hash, password)

# 员工表
class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False, unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=True)

# 部门表
class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, nullable=False)
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
    account_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

Contract_Agreement = db.Table('contract_agreement',
                              db.Column('contract_id', db.Integer, db.ForeignKey('contract.id')),
                              db.Column('agreement_id', db.Integer, db.ForeignKey('agreement.id')),
                     )

# 合同表
class Contract(db.Model):
    __tablename__ = 'contract'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False, unique=False)
    expiry_date = db.Column(db.String(15), nullable=False)
    start_date = db.Column(db.String(15), nullable=False)
    isCheck = db.Column(db.Boolean, nullable=False, unique=False)
    # customer_id引用customer表的id
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, unique=True)
    agreements = db.relationship('Agreement',
                                 secondary=Contract_Agreement,
                                 backref=db.backref('contracts', lazy='dynamic'),
                                 lazy='dynamic')

# 服务项目表
class Agreement(db.Model):
    __tablename__ = 'agreement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)

# 收费记录表
class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=True, unique=False)
    # 金额
    charge = db.Column(db.Integer, nullable=False, unique=False)
    charge_date = db.Column(db.String(15), nullable=False, unique=False)
    # contract_id引用contract表的id
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'), nullable=True, unique=True)

# 合同-服务项目表
"""
class Contract_Agreement(db.Model):
    __tablename__ = 'contract_agreement'
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, nullable=False, unique=True)
    agreement_id = db.Column(db.Integer, nullable=False, unique=True)
"""
# 待办事项表
class Todolist(db.Model):
    __tablename__ = "todolist"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False, unique=False)
    is_finish = db.Column(db.Boolean, nullable=False, unique=False)
    deadline = db.Column(db.String(15))
    # account_id引用employee表的id
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False, unique=True)
    # account_id引用employee表的id
    account_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    todolists = db.relationship('Todolist', backref='category')

if __name__ == '__main__':
    app = create_app('default')
    with app.app_context():
        db.create_all()

    #待办事项
    inbox = Category(name=u'收件箱')
    done = Category(name=u'已完成')
    #职位
    staff = Position(name=u'普通员工')
    director = Position(name=u'主管')
    db.session.add_all([inbox, done, staff, director])
    db.session.commit()
