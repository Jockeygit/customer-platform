# -*- coding: utf-8 -*-

# -------------------------------------------------
#   File Name :       form
#   Description :     添加描述信息
#   Author :          zhoujie
#   Created:          2018/1/13  21:48 
# -------------------------------------------------
#   Change Activity:
#                     2018/1/13
# -------------------------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length

# 登录表单
class loginForm(FlaskForm):
    # 用户名
    username = StringField('用户名', validators=[DataRequired(),
               length(1, 20, message='长度位于1~20之间')], render_kw={'placeholder':'输入用户名'})
    # 密码
    password = PasswordField('密码', validators=[PasswordField,
               length(1, 10, message='长度位于1~10之间')], render_kw={'placeholder':'输入密码'})
    submit = SubmitField('登录')

# 注册表单
class registerForm(FlaskForm):

    # 用户名
    username = StringField('用户名', validators=[DataRequired(), length(1, 20, message='长度位于1~20之间')])
    # 密码
    password = StringField('密码', validators=[DataRequired(), length(1, 10, message='长度位于1~10之间')])
    submit = SubmitField('注册')