# -*- coding: utf-8 -*-

# -------------------------------------------------
#   File Name :       form
#   Description :     登录相关表单
#   Author :          zhoujie
#   Created:          2018/1/13  21:48 
# -------------------------------------------------
#   Change Activity:
#                     2018/1/13
# -------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, length, EqualTo, Regexp
from wtforms import ValidationError
from ..model import User,Employee


# 登录表单
class LoginForm(FlaskForm):
    # 用户名
    username = StringField('用户名', validators=[DataRequired(),
                                              length(1, 20, message='长度位于1~20之间')], render_kw={'placeholder': '输入用户名'})
    # 密码
    password = PasswordField('密码', validators=[PasswordField,
                                               length(1, 10, message='长度位于1~10之间')], render_kw={'placeholder': '输入密码'})
    remember_me = BooleanField('记住我？')
    submit = SubmitField('登录')


# 注册表单
class RegisterForm(FlaskForm):
    # 用户名
    username = StringField('用户名', validators=[DataRequired(), length(1, 20, message='长度位于1~20之间'),
                                              Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                     '用户名只能包括字母、数字、点或下划线.')])
    realname = StringField('真实姓名', validators=[DataRequired()])
    # 密码
    password = PasswordField('密码', validators=[DataRequired(), length(1, 10, message='长度位于1~10之间'),
                                               EqualTo('password_confirm', message='两次密码必须一致.')])
    password_confirm = PasswordField('确认密码', validators=[PasswordField, length(1, 10, message='长度位于1~10之间.')])
    submit = SubmitField('注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在.')

    def validate_realname(self, field):
        if Employee.query.filter_by(name=field.data).first():
            raise ValidationError('真实姓名已存在.请在姓名后加上个人标识')

#修改个人资料
class EditUserProfileFor(FlaskForm):
    realname = StringField('真实姓名', validators=[DataRequired()])
