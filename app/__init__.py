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
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


import sys
reload(sys)

# python2 转换编码格式为 utf8（string and byte）
sys.setdefaultencoding('utf8')

# 定义app对象
app = Flask(__name__)

# 定义Bootstrap对象
bootstrap = Bootstrap(app)

db = SQLAlchemy(app)
login_manager = LoginManager(app)

login_manager.login_view = "views.login"  # 定义登录的视图

# 为app对象注册蓝图，''表示蓝图的挂载位置从根目录开始
from app.auth import view as auth_view
app.register_blueprint(auth_view, url_prefix='')

from app.main import view as main_view
app.register_blueprint(main_view, url_prefix='')





# 启动配置文件
app.config.from_object('config')

#配置数据库地址(格式：mysql://username:password@hostname/database)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:5185425mysql@localhost:3306/mydatabase'

#该配置为True,则每次请求结束都会自动commit数据库的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True




