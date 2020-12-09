# -*- coding: utf-8 -*-

# -------------------------------------------------
#   File Name :       __init__
#   Description :     添加描述信息
#   Author :          zhoujie
#   Created:          2018/1/7  15:55
# -------------------------------------------------
#   Change Activity:
#                     2018/1/7
# -------------------------------------------------
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)

    print(__name__)
    # 启动配置文件
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"  # 定义登录的视图

    # 为app对象注册蓝图，''表示蓝图的挂载位置从根目录开始
    from app.auth import view as auth_view
    app.register_blueprint(auth_view, url_prefix='')

    from app.main import view as main_view
    app.register_blueprint(main_view, url_prefix='')

    return app

