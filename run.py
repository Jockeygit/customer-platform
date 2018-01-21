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

from app import app

if __name__=='__main__':
    app.debug = True
    app.run()