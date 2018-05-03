# -*- coding: utf-8 -*-

# -------------------------------------------------
#   File Name :       route
#   Description :     添加描述信息
#   Author :          zhoujie
#   Created:          2018/1/21  16:25
# -------------------------------------------------
#   Change Activity:
#                     2018/1/21
# -------------------------------------------------
from flask import render_template, flash, request, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import redirect

from app import login_manager, db
from app.auth import view
from app.auth.form import LoginForm, RegisterForm
from app.model import User


# 用户登录
@view.route('/', methods=('POST', 'GET'))
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()  # 查询对应表里符合用户名的第一条数据

        if user is not None and user.verify_password(form.password.data):
            flash('登录成功')

            login_user(user)  # 用户登录，为其注册会话

            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            if user is None:
                # 渲染表单
                flash('用户名不存在')
            elif form.password.data != user.password:
                flash('密码不正确')
    return render_template('login.html', form=form)

    # return redirect(url_for('main.index'))


# 用户登出
@view.route('/logout')
@login_required
def logout():
    logout_user()  # 用户登出，为其删除会话
    return redirect(url_for('auth.login'))


# 用户注册
@view.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    status = ''
    if form.validate_on_submit():
        print('valid')
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)  # 添加会话
        db.session.commit()  # 提交会话
        flash('注册成功，请登录')
        return redirect(url_for('auth.login'))
    else:
        if form.errors:
            flash(str(list(form.errors.values())[0]).strip("[]'"))
    return render_template('register.html', form=form)


# 回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff

    return redirect(url_for('auth.login', next=request.url))
