# -*- coding: utf-8 -*-

# -------------------------------------------------
#   File Name :       config
#   Description :     添加描述信息
#   Author :          zhoujie
#   Created:          2018/1/13  15:49 
# -------------------------------------------------
#   Change Activity:
#                     2018/1/13
# -------------------------------------------------
import os
basedir = os.path.abspath(os.path.dirname(__file__))
from datetime import timedelta


class Config:
    # 建立加密的令牌，用于验证Form表单提交
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SSL_REDIRECT = False
    CSRF_ENABLED = True
    # 该配置为True,则每次请求结束都会自动commit数据库的变动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    UPLOAD_FOLDER = 'upload'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    print('use dev config')
    DEBUG = True
    # 该配置为True,则每次请求结束都会自动commit数据库的变动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 配置windows数据库地址(格式：mysql://username:password@hostname/database)
   # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #    'mysql+pymysql://root:root@localhost:3306/cms_test'

    # 配置mac数据库地址(格式：mysql://username:password@hostname/database)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    'mysql+pymysql://root:5185425mysql@localhost:3306/mydatabase'
      # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:5185425mysql@localhost:3306/mydatabase'

    #设置静态资源缓存时间为1秒
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)


config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}