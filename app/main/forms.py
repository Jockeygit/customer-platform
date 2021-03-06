# -*- coding: utf-8 -*-

# -------------------------------------------------
#   File Name :       form
#   Description :     各模块表单
#   Author :          zhoujie
#   Created:          2018/5/2  15:36 
# -------------------------------------------------
#   Change Activity:
#                     2018/5/2
# -------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, DateField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, length
from wtforms import ValidationError
from app.model import *
from flask_login import current_user

# 客户表单
class customerForm(FlaskForm):

    customername = StringField('客户名称', validators=[DataRequired('用户名称不能为空'),
                   length(1, 20, message='客户名称长度位于1~20之间')], render_kw={'placeholder':'请输入客户名称'})
    type = RadioField('客户类型', validators=[DataRequired()], choices=[('0', '个人'), ('1', '企业')], default='1')
    phone = StringField('电话', validators=[length(1, 15, message='电话长度位于1~15之间')],
                    render_kw={'placeholder':'请输入电话'})
    email = StringField('邮箱', validators=[length(1, 20, message='邮箱长度位于1~20之间')],
                    render_kw={'placeholder': '请输入邮箱'})
    address = StringField('地址', validators=[length(1, 30, message='地址长度位于1~30之间')],
                    render_kw={'placeholder': '请输入地址'})
    manager = SelectField('客户经理', coerce=int, validators=[DataRequired()])

    submit_customer = SubmitField('保存')

    # 初始化客户经理下拉框
    def __init__(self, *args, **kwargs):
        super(customerForm, self).__init__(*args, **kwargs)
        self.manager.choices = [(employee.id, employee.name)
                                       for employee in Employee.query.order_by(Employee.name).all()]

    def validate_customername(self, field):
        if Customer.query.filter_by(name=field.data).first():
            raise ValidationError('该客户已存在.')

    #    self.manager.default = [(Employee.id, Employee.name)
                   #        for customerForm in Employee.query.order_by(Employee.name).all()]

# 更新客户表单
class updateCustomerForm(FlaskForm):
    customername = StringField('客户名称', validators=[DataRequired('用户名称不能为空'),
                                                       length(1, 20, message='客户名称长度位于1~20之间')],
                                   render_kw={'placeholder': '请输入客户名称'})
    type = RadioField('客户类型', validators=[DataRequired()], choices=[('0', '个人'), ('1', '企业')], default='1')
    phone = StringField('电话', validators=[length(1, 15, message='电话长度位于1~15之间')],
                            render_kw={'placeholder': '请输入电话'})
    email = StringField('邮箱', validators=[length(1, 20, message='邮箱长度位于1~20之间')],
                            render_kw={'placeholder': '请输入邮箱'})
    address = StringField('地址', validators=[length(1, 30, message='地址长度位于1~30之间')],
                              render_kw={'placeholder': '请输入地址'})
    manager = SelectField('客户经理', coerce=int, validators=[DataRequired()])

    submit_customer = SubmitField('保存')

    # 初始化客户经理下拉框
    def __init__(self, *args, **kwargs):
        super(updateCustomerForm, self).__init__(*args, **kwargs)
        self.manager.choices = [(employee.id, employee.name)
                                for employee in Employee.query.order_by(Employee.name).all()]

# 创建/编辑合同
class contractFrom(FlaskForm):

    agreement = SelectMultipleField('服务项目', coerce=int, validators=[DataRequired()])

    status = RadioField('状态', validators=[DataRequired()], choices=[('0', '未生效'), ('1', '生效')], default='1')

    startDate = DateField('开始日期', default='', validators=[DataRequired()], format='%Y-%m-%d')

    expiryDate = DateField('到期日期', default='', validators=[DataRequired()], format='%Y-%m-%d')

    submit = SubmitField('保存')

    # 初始化服务项目下拉框
    def __init__(self, *args, **kwargs):
        super(contractFrom, self).__init__(*args, **kwargs)
        self.agreement.choices = [(agreements.id, agreements.name)
                                       for agreements in Agreement.query.order_by(Agreement.name).all()]

class contractFrom(FlaskForm):
    agreement = SelectMultipleField('服务项目', coerce=int, validators=[DataRequired()])

    status = RadioField('状态', validators=[DataRequired()], choices=[('0', '未生效'), ('1', '生效')], default='1')

    startDate = DateField('开始日期', default='', validators=[DataRequired()], format='%Y-%m-%d')

    expiryDate = DateField('到期日期', default='', validators=[DataRequired()], format='%Y-%m-%d')

    submit = SubmitField('保存')

    # 初始化服务项目下拉框
    def __init__(self, *args, **kwargs):
        super(contractFrom, self).__init__(*args, **kwargs)
        self.agreement.choices = [(agreements.id, agreements.name)
                                      for agreements in Agreement.query.order_by(Agreement.name).all()]

# 合同收费
class chargeFrom(FlaskForm):
    charge = IntegerField('应收费用', validators=[DataRequired()])

    chargeDate = DateField('收费日期', default='', validators=[DataRequired()], format='%Y-%m-%d')

    description = StringField('说明', validators=[length(1, 50, message='说明字数不超过50')],
                    render_kw={'placeholder': '请输入说明'})

    submit = SubmitField('确定')


class adddepartmentFrom(FlaskForm):
    name = StringField('部门名称', validators=[length(1, 10, message='部门名称字数不超过10')],
                       render_kw={'placeholder': '请输入名称'})
    submit = SubmitField('保存')


# 更新部门
class departmentFrom(FlaskForm):
    name = StringField('部门名称', validators=[length(1, 10, message='部门名称字数不超过10')],
                              render_kw={'placeholder': '请输入名称'})

    parent = SelectField('上级部门', coerce=int)

    submit = SubmitField('保存')

    # 初始化部门主管下拉框
    def __init__(self, *args, **kwargs):
        super(departmentFrom, self).__init__(*args, **kwargs)
        self.parent.choices = [(department.id, department.name)
                                for department in Department.query.order_by(Department.name).all()]

# 更新员工
class employeeFrom(FlaskForm):
    name = StringField('员工名称', validators=[length(1, 10, message='员工名称字数不超过10')],
                       render_kw={'placeholder': '请输入名称'})

    department = SelectField('所属部门', coerce=int)

    position = SelectField('职位', coerce=int)

    submit = SubmitField('保存')

    # 初始化下拉框
    def __init__(self, *args, **kwargs):
        super(employeeFrom, self).__init__(*args, **kwargs)
        self.department.choices = [(department.id, department.name)
                               for department in Department.query.order_by(Department.name).all() if
                               department.id != 1]

        self.position.choices = [(position.id, position.name)
                               for position in Position.query.order_by(Position.name).all()]

# 新建/编辑待办事项
class todolistFrom(FlaskForm):
    content = StringField('', validators=[length(1, 100, message='字数不超过100')],
                              render_kw={'placeholder': '请输入内容'})

    submit = SubmitField('保存')

# 报告
class reportForm(FlaskForm):
    employee = SelectField('下属', coerce=int)

    # 初始化下拉框
    def __init__(self, *args, **kwargs):
        super(reportForm, self).__init__(*args, **kwargs)
        accountId = db.session.query(User.account_id).filter_by(id=current_user.id).first()[0]
        positionId = db.session.query(Employee.position_id).filter_by(id=accountId).first()[0]
        if (positionId == 1):
            departmentId = db.session.query(Employee.department_id).filter_by(id=accountId).first()[0]
            self.employee.choices = [(employee.id, employee.name)
                        for employee in Employee.query.filter(Employee.department_id == departmentId).all()]
        else:
            self.employee.choices = []