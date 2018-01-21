# -*- coding: utf-8 -*-

# -------------------------------------------------
#   File Name :       views
#   Description :     添加描述信息
#   Author :          zhoujie
#   Created:          2018/1/12  14:33 
# -------------------------------------------------
#   Change Activity:
#                     2018/1/12
# -------------------------------------------------
from flask import render_template, flash, Blueprint, url_for
from werkzeug.utils import redirect
from app.form import loginForm, registerForm
from app.model import User
from app import login_manager, db
from flask_login import login_user, logout_user, login_required

# 定义蓝图对象
view = Blueprint('view', __name__)

# 用户登录
@view.route('/', methods = ('POST','GET'))
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() # 查询对应表里符合用户名的第一条数据
        if user is not None and user.password == form.password.data:
            flash('登录成功')
            login_user(user)   # 用户登录，为其注册会话
            return redirect(url_for('view.defult'))
        else:
            if user is None:
            # 渲染表单
             flash('用户名不存在')
            elif form.password.data != user.password:
             flash('密码不正确')
    return render_template('login.html', form=form)

# 用户登出
@view.route('/logout')
@login_required
def logout():
    logout_user() # 用户登出，为其删除会话
    flash('你已退出登录')
    return redirect(url_for('login'))

# 用户注册
@view.route('/register', methods =('GET', 'POST'))
def register():
    form = registerForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user) # 插入数据
        db.session.commit() # 提交更改
        flash('注册成功，请登录')
        return redirect(url_for('view.login'))
    return render_template('register.html', form = form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()






@view.route('/home')
def defult():
    user = {'nickname':'mark'}
    posts = [
        {   'author':{'nickname':'Lily'},
            'body':'Today is cold!'},
        {'author':{'nickname':'BOb'},
            'body':'Today is warm!'}
        ]
    return render_template('index.html', title='blog', user=user, posts=posts)


@view.route('/success')
def success():
    return '<h1>Success！</h1>'




