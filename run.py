# -*- coding: utf-8 -*-

# -------------------------------------------------
#   File Name :       run
#   Description :     添加描述信息
#   Author :          zhoujie
#   Created:          2018/1/12  14:43 
# -------------------------------------------------
#   Change Activity:
#                     2018/1/12
# -------------------------------------------------
#!flask/bin/python
import os, sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# from flask.ext.script import Manager, Server
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.model import *

from app import create_app
app = create_app(os.getenv('config') or 'default')

# manager = Manager(app)  # Manager类追踪所有在命令行中调用的命令和处理过程的调用运行情况

migrate = Migrate(app, db)  # 扩展数据库表结构
# manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    app.run()   # Manager.run()启动Manager实例接收命令行中的命令