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
from flask import render_template
#from app.auth.route import view


#@view.route('/success')
def success():
    return render_template('ui-elements.html')




