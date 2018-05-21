# -*- coding: utf-8 -*-

# -------------------------------------------------
#   File Name :       route
#   Description :     添加描述信息
#   Author :          zhoujie
#   Created:          2018/1/21  16:43 
# -------------------------------------------------
#   Change Activity:
#                     2018/1/21
# -------------------------------------------------
from operator import and_

import xlwt as xlwt
from flask import render_template, flash, url_for, request, jsonify, current_app, Response, send_from_directory
from sqlalchemy import func
from werkzeug.utils import secure_filename
from app.main import view, forms
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from app.model import *
from xlrd import open_workbook
import json, time
import os
import io
import app


# 首页
@view.route('/index')
@login_required
def index():
    return render_template('index.html')

"""
-----客户------
"""
@view.route('/customer', methods=['GET', 'POST'])
@login_required
def customer():
    print(request.data)
    add_custom_form = forms.customerForm()
    update_custom_form = forms.updateCustomerForm()
    """
    if add_custom_form.validate_on_submit():
        print("valid")
        flash('创建客户')
        customer = Customer(name=add_custom_form.customername.data, type=add_custom_form.type.data, phone=add_custom_form.phone.data, email=add_custom_form.email.data,address=add_custom_form.address.data, account_id=add_custom_form.manager.data)
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        if add_custom_form.errors:
            print(str(list(add_custom_form.errors.values())[0]).strip("[]'"))
            flash(str(list(add_custom_form.errors.values())[0]).strip("[]'"))
    """
    return render_template('customer.html', add_form=add_custom_form, update_form=update_custom_form)


@view.route('/customer/add', methods=['POST'])
@login_required
def customer_add():
    add_custom_form = forms.customerForm()
    if add_custom_form.validate_on_submit():
        customer = Customer(name=add_custom_form.customername.data, type=add_custom_form.type.data,
                            phone=add_custom_form.phone.data, email=add_custom_form.email.data,
                            address=add_custom_form.address.data, account_id=add_custom_form.manager.data)
        db.session.add(customer)
        db.session.commit()
        return jsonify({'result': '1'})
    else:
        if add_custom_form.errors:
            #print(str(list(add_custom_form.errors.values())[0]).strip("[]'"))
            result=str(list(add_custom_form.errors.values())[0]).strip("[]'")
            return jsonify({'result': '%s' % result})


@view.route('/customer/import', methods=['POST'], strict_slashes=False)
@login_required
def customer_import():
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_dir = os.path.join(basedir, current_app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and f.filename.rsplit('.', 1)[1] in ['xls', 'xlsx']:  # 判断是否是允许上传的文件类型
        ext = f.filename.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
        file_path = os.path.join(file_dir, new_filename)
        f.save(file_path)  # 保存文件到upload目录

    bk = open_workbook(file_path, encoding_override="utf-8")
    try:
        sh = bk.sheet_by_index(0)
    except:
        print("no sheet in %s named sheet1" % new_filename)
    else:
        nrows = sh.nrows
        ncols = sh.ncols
        print(os.getcwd(), "行数 %d,列数 %d" % (nrows, ncols))
        row_list = []
        for i in range(1, nrows):
            row_date = sh.row_values(i)
            print(row_date)
            n = i - 1
            max_id = db.session.query(db.func.max(Customer.id)).scalar()
            customer = Customer()
            customer.id = max_id + 1
            customer.name = row_date[0]
            if row_date[1] == u"个人":
                customer.type = 0
            else:
                customer.type = 1
            customer.phone = row_date[2]
            customer.email = row_date[3]
            customer.address = row_date[4]
            manager_id = db.session.query(Employee.id).filter_by(name=row_date[5]).first()[0]
            customer.account_id = manager_id
            db.session.add(customer)
            db.session.commit()
            db.session.close()
            os.remove(file_path)  #删除导入的文件
    return "1"

@view.route('/customer/export', methods=['POST'])
@login_required
def customer_export():
   # web.header('Content-type', 'application/vnd.ms-excel')  # 指定返回的类型

   # web.header('Transfer-Encoding', 'chunked')
    #web.header('Content-Disposition', 'attachment;filename="export.xls"')  # 设定用户浏览器显示的保存文件名

    file = xlwt.Workbook()
    file.encoding = 'gbk'
    sheet = file.add_sheet(u'客户数据', cell_overwrite_ok=True)

    data = []
    row0 = [u'客户名称', u'类型', u'电话', u'邮箱', u'地址', u'客户经理']
    data.append(row0)

    cus_json = customer_list()
    cus_lists = json.loads(cus_json)['data']
    print(cus_lists)

    # 得到数据
    for cus in cus_lists:
        row = list(cus.values())
        del(row[0])
        data.append(row)
        print(row)

    # 写入数据
    for i in range(0, len(data)):
        for j in range(0, len(row)):
            style = xlwt.XFStyle()
            font = xlwt.Font()
            font.name = 'Times New Roman'
            font.height = 220
            font.bold = False
            style.font = font
            sheet.write(i, j, data[i][j], style)

    file.save('app/main/upload/demo.xls')

    # 下载文件
    dirpath = os.path.join(view.root_path, 'upload')

   # exist_file = os.path.exists("demo.xls")
   # if exist_file:  # 生成的文件会在项目文件里存留，所以在下载或者发送之后要删除
    #    os.remove('demo.xls')
    return send_from_directory(dirpath, 'demo.xls', as_attachment=True)


@view.route('/customer/update/<id>', methods=['POST'])
@login_required
def customer_update(id):
    form = forms.updateCustomerForm()
    if form.validate_on_submit():
     customer = Customer.query.filter(Customer.id == id).first()
     customer.name = form.customername.data
     customer.type = form.type.data
     customer.phone = form.phone.data
     customer.email = form.email.data
     customer.address = form.address.data
     customer.account_id = form.manager.data
     db.session.add(customer)
     db.session.commit()
     return jsonify({'result': '1'})
    else:
     if form.errors:
         result = str(list(form.errors.values())[0]).strip("[]'")
         return jsonify({'result': '%s' % result})


@view.route('/customer/del', methods=['POST'])
@login_required
def customer_del():
    #print(request.data)
    #print(json.loads(request.data)["name"])
    data = request.data
    name = json.loads(data)["name"]
    try:
         customer = Customer.query.filter(Customer.name == name).first()
         db.session.delete(customer)
         db.session.commit()
    except Exception:
        return "0"
    return "1"


@view.route('/customer/listJson')
@login_required
def customer_list():
    if request.args.get('name'):
     print(request.args.get('name'))
     customer = Customer.query.filter(Customer.name == request.args.get('name')).all()
    else:
     accountId = db.session.query(User.account_id).filter_by(id=current_user.id).first()[0]
     positionId = db.session.query(Employee.position_id).filter_by(id=accountId).first()[0]
     if (positionId == 1):
         departmentId = db.session.query(Employee.department_id).filter_by(id=accountId).first()[0]
         customer = db.session.query(Customer).join(Employee, Customer.account_id == Employee.id).filter(
             Employee.department_id == departmentId).all()
     else:
         customer = Customer.query.filter(Customer.account_id == accountId).all()

    jsonData = []
    for cus in customer:
     cusData = {}
     cusData['id'] = cus.id
     cusData['name'] = cus.name
     if cus.type == 0:
         cusData['type'] = u"个人"
     else:
         cusData['type'] = u"企业"
     cusData['phone'] = cus.phone
     cusData['email'] = cus.email
     cusData['address'] = cus.address
     cusData['manager'] = db.session.query(Employee.name).filter_by(id=cus.account_id).first()[0]
     jsonData.append(cusData)

    jsondatar = json.dumps(jsonData, ensure_ascii=False)
    jsondatar = jsondatar.replace("null", '"-"')
    jsondatar = '{"data":' + jsondatar + "}"
    return jsondatar

# customer = Customer.query.filter_by(account_id=current_user).all()  # 查询客户表里符合客户经理的所有数据


"""
--------合同-------
"""
@view.route('/contract', methods=['GET'])
@login_required
def contract():
    form = forms.contractFrom()
    return render_template("contract.html", form=form)


@view.route('/contract/listJson')
@login_required
def contract_list():
    accountId = db.session.query(User.account_id).filter_by(id=current_user.id).first()[0]
    positionId = db.session.query(Employee.position_id).filter_by(id=accountId).first()[0]
    if (positionId == 1):
        departmentId = db.session.query(Employee.department_id).filter_by(id=accountId).first()[0]

        customer = db.session.query(Customer).join(Employee, Customer.account_id == Employee.id).filter(
            Employee.department_id == departmentId).all()

    else:
        customer = Customer.query.filter(Customer.account_id == accountId).all()

    jsonData = []
    print(customer)
    for cus in customer:
        print(cus.name)
        Data = {}
        Data["cus_name"] = cus.name
        contract = Contract.query.filter(Contract.customer_id == cus.id).first()
        print(contract)
        if contract:
            print(contract.expiry_date)
            Data["is_create"] = 1
            if contract.status == 0:
                Data['status'] = u"未生效"
            else:
                Data['status'] = u"生效"
            Data["start_date"] = contract.start_date
            Data["expiry_date"] = contract.expiry_date
            Data["is_charge"] = contract.isCheck

            # 服务项目
            agree_name = ''
            agreements = contract.agreements.all()
            for agree in agreements:
                agree_name = agree_name + " " +agree.name

            Data['agreements'] = agree_name
        else:
            Data["is_create"] = 0
            Data['status'] = '-'
            Data["start_date"] = '-'
            Data["expiry_date"] = '-'
            Data["is_charge"] = '-'
            Data['agreements'] = '-'

        jsonData.append(Data)


    jsondatar = json.dumps(jsonData, ensure_ascii=False)
    jsondatar = jsondatar.replace("null", '"-"')
    jsondatar = '{"data":' + jsondatar + "}"
    return jsondatar

@view.route('/contract/add/<name>', methods=['POST'])
@login_required
def contract_add(name):
    contact_form = forms.contractFrom()
    if contact_form.validate_on_submit():
        customerId = db.session.query(Customer.id).filter_by(name=name).first()[0]
        contact = Contract(start_date=contact_form.startDate.data, expiry_date=contact_form.expiryDate.data,
                            status=contact_form.status.data, isCheck=0,
                           customer_id=customerId)
        agreements = contact_form.agreement.data
        for agree in agreements:
            agreement = Agreement.query.filter(Agreement.id == agree).first()
            contact.agreements.append(agreement)
        db.session.add(contact)
        db.session.commit()
        return jsonify({'result': '1'})
    else:
        if contact_form.errors:
            # print(str(list(add_custom_form.errors.values())[0]).strip("[]'"))
            result = str(list(contact_form.errors.values())[0]).strip("[]'")
            return jsonify({'result': '%s' % result})

@view.route('/contract/update/<id>', methods=['POST'])
@login_required
def contract_update(id):
    form = forms.contractFrom()
    if form.validate_on_submit():
        contract = Contract.query.filter(Contract.id == id).first()
        agreements = contract.agreements.all()
        for agree in agreements:
            contract.agreements.remove(agree)
        agreeme = form.agreement.data
        for agree in agreeme:
            agreement = Agreement.query.filter(Agreement.id == agree).first()
            contract.agreements.append(agreement)
        contract.status = form.status.data
        contract.start_date = form.startDate.data
        contract.expiry_date = form.expiryDate.data
        db.session.add(contract)
        db.session.commit()
        return jsonify({'result': '合同更新成功'})

    else:
        if form.errors:
            result = str(list(form.errors.values())[0]).strip("[]'")
            return jsonify({'result': '%s' % result})

@view.route('/contract/del', methods=['POST'])
@login_required
def contract_del():
    data = request.data  # 存放contract_id
    id = json.loads(data)['id']
    try:
        contract = Contract.query.filter(Contract.id == id).first()
        db.session.delete(contract)
        db.session.commit()
    except Exception:
        return "0"
    return "1"

@view.route('/contract/getchar', methods=['POST'])
@login_required
def contract_getchar():
    data = request.data  # 存放contract_id
    id = json.loads(data)['id']
    charge = 0
    agreements = Contract.query.filter(Contract.id == id).first().agreements.all()
    print(agreements)
    for agree in agreements:
        print(agree.id)
        price = db.session.query(Agreement.price).filter_by(id=agree.id).first()[0]
        charge = charge + price
    return '价格是:%d' % charge

@view.route('/contract/char/<id>', methods=['POST'])
@login_required
def contract_char(id):
    charge_form = forms.chargeFrom()
    if charge_form.validate_on_submit():
        record = Record(charge = charge_form.charge.data, charge_date = charge_form.chargeDate.data,
                        description = charge_form.description.data, contract_id = id)
        db.session.add(record)
        db.session.commit()
        return jsonify({'result': 'charge success'})
    else:
        if charge_form.errors:
            result = str(list(charge_form.errors.values())[0]).strip("[]'")
            return jsonify({'result': '%s' % result})

"""
--------收费记录-------
"""
@view.route('/record', methods=['GET'])
@login_required
def record():
    return render_template("record.html")


@view.route('/record/listJson', methods=['GET'])
@login_required
def record_list():
    accountId = db.session.query(User.account_id).filter_by(id=current_user.id).first()[0]
    positionId = db.session.query(Employee.position_id).filter_by(id=accountId).first()[0]
    if (positionId == 1):
        departmentId = db.session.query(Employee.department_id).filter_by(id=accountId).first()[0]
        customer = db.session.query(Customer).join(Employee, Customer.account_id == Employee.id).filter(
            Employee.department_id == departmentId).all()
    else:
        customer = Customer.query.filter(Customer.account_id == accountId).all()

    jsonData = []
    for cus in customer:
        Data = {}
        Data["cus_name"] = cus.name
        contract = Contract.query.filter(Contract.customer_id == cus.id).first()
        if contract:
            record = Record.query.filter(Record.contract_id == contract.id).first()
            print({'contractId:': '%s' % contract.id})
            if record:
                Data["charge"] = record.charge
                Data["charge_date"] = record.charge_date
                Data["description"] = record.description
            else:
                Data = {}

            jsonData.append(Data)

    jsondatar = json.dumps(jsonData, ensure_ascii=False)
    jsondatar = jsondatar.replace("null", '"-"')
    jsondatar = '{"data":' + jsondatar + "}"
    return jsondatar

@view.route('/record/undo')
@login_required
def record_undo():
    #data = request.data  # 存放record.id
    #id = json.loads(data)['id']
    try:
        record = Record.query.filter(Record.id == 1).first()
        db.session.delete(record)
        db.session.commit()
    except Exception as e:
        print(e)
        return "0"
    return "undo success"

# 待办事项
@view.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    print(request.data)
    form = forms.todolistFrom()
    return render_template('todo.html')

@view.route('/todo/listJson', methods=['GET'])
@login_required
def todo_list():
    accountId = db.session.query(User.account_id).filter_by(id=current_user.id).first()[0]
    todo = db.session.query(Todolist.content).filter_by(account_id=accountId).all()
    data = []
    for list in todo:
        content = list
        data.append(content)
        print (content)
        jsondatar = json.dumps(data, ensure_ascii=False)
    return jsondatar

@view.route('/todo/add', methods=['POST'])
@login_required
def todo_add():
    todo_form = forms.todolistFrom()
    if todo_form.validate_on_submit():
        accountId = db.session.query(User.account_id).filter_by(id=current_user.id).first()[0]
        todolist = Todolist(content = todo_form.content.data, account_id=accountId)
        db.session.add(todolist)
        db.session.commit()
        return jsonify({'result': 'save success'})
    else:
        if todo_form.errors:
            result = str(list(todo_form.errors.values())[0]).strip("[]'")
            return jsonify({'result': '%s' % result})

@view.route('/todo/update/<id>', methods=['POST'])
@login_required
def todo_update(id):
    form = forms.todolistFrom()
    if form.validate_on_submit():
        todolist = Todolist.query.filter(Todolist.id == id).first()
        todolist.content = form.content.data
        db.session.add(todolist)
        db.session.commit()
        return jsonify({'result': 'content update success！'})
    else:
        if form.errors:
            result = str(list(form.errors.values())[0]).strip("[]'")
            return jsonify({'result': '%s' % result})

@view.route('/todo/del', methods=['POST'])
@login_required
def todo_del():
    data = request.data  #存放todolist.id
    id = json.loads(data)['id']
    try:
        todolist = Todolist.query.filter(Todolist.id == id).first()
        db.session.delete(todolist)
        db.session.commit()
    except Exception:
        return "0"
    return "1"

# 部门设置
@view.route('/depart', methods=['GET', 'POST'])
@login_required
def depart():
    print(request.data)
    add_depart_form = forms.adddepartmentFrom()
    update_depart_form = forms.departmentFrom()
    return render_template('todo.html')

@view.route('/depart/listJson', methods=['GET'])
@login_required
def depart_list():
    jsonData = []
    departments = Department.query.filter().all()
    for department in departments:
        departmentname = db.session.query(Department.name).filter_by(id=department.id).first()
        depdata = {}
        employeename = ''
        depdata['name'] = departmentname
        director = Employee.query.filter(and_(Employee.department_id == department.id, Employee.position_id == 1)).first()
        if director:
            depdata['director'] = director.name
        else:
            depdata['director'] = '-'
        employees = Employee.query.filter(and_(Employee.department_id == department.id, Employee.position_id == 2)).all()
        if employees:
            for employee in employees:
                employeename = employeename + " " + employee.name
                depdata['staff'] = employeename
        else:
            depdata['staff'] = '-'
        jsonData.append(depdata)
    depnone = {}
    nononame = ''
    depnone['name'] = '未分配'
    depnone['director'] = '-'
    none = Employee.query.filter(and_(Employee.department_id == None, Employee.position_id == None)).all()
    for no in none:
        nononame = nononame + " " + no.name
        depnone['staff'] = nononame
    jsonData.append(depnone)

    jsondatar = json.dumps(jsonData, ensure_ascii=False)
    jsondatar = jsondatar.replace("null", '"-"')
    jsondatar = '{"data":' + jsondatar + "}"
    return jsondatar

@view.route('/depart/add')
@login_required
def depart_add():
    form = forms.departmentFrom()
    if form.validate_on_submit():
        department = Department(name=form.name.data)
        db.session.add(department)
        db.session.commit()
        return jsonify({'result': '1'})
    else:
        if form.errors:
            result=str(list(form.errors.values())[0]).strip("[]'")
            return jsonify({'result': '%s' % result})

@view.route('/depart/update/<id>', methods=['POST'])
@login_required
def depart_update(id):
    form = forms.departmentFrom()
    if form.validate_on_submit():
        department = Department.query.filter(Department.id == id).first()
        department.name = form.name.data
        if form.director.data:
            director = Employee.query.filter(Employee.id == form.director.data).first()
            director.position_id = 1
            db.session.add(director)
            db.session.commit()
        if form.staff.data:
            staff = Employee.query.filter(Employee.department_id == id).all()
            db.session.delete(staff)
            db.session.commit()
            staffId = form.staff.data
            for Id in staffId:
                name = db.session.query(Employee.name).filter_by(id=Id).first()[0]
                employee = Employee(name=name, department_id=id, position_id=2)
                db.session.add(employee)
                db.session.commit()
        return jsonify({'result': '部门更新成功'})
    else:
        if form.errors:
            result = str(list(form.errors.values())[0]).strip("[]'")
            return jsonify({'result': '%s' % result})

@view.route('/depart/del', methods=['POST'])
@login_required
def depart_del():
    data = request.data  #存放department.id
    id = json.loads(data)['id']
    try:
        department = Department.query.filter(Department.id == id).first()
        db.session.delete(department)
        db.session.commit()
        employees = Employee.query.filter(Employee.department_id == id).all()
        for employee in employees:
            employee.position_id = None
            employee.department_id = None
            db.session.add(employee)
            db.session.commit()
    except Exception:
        return "0"
    return "1"


# 工作报告
@view.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    print(request.data)
    return render_template('report.html')

@view.route('/report/data', methods=['GET'])
@login_required
def report_data():
    # 客户统计数据
    #sum_cus = db.session.query(Customer.account_id, func.count('*').label("cus_count")).group_by(Customer.account_id).all()
    sum_cus = db.session.query(func.count('*')).filter(Customer.id > 0).scalar()
    accountId = db.session.query(User.account_id).filter_by(id=current_user.id).first()[0]
    user_cus = db.session.query(func.count('*')).filter(Customer.account_id == accountId).scalar()

    # 合同统计数据
    sum_con = db.session.query(func.count('*')).filter(Contract.id > 0).scalar()
    #customerId = db.session.query(Customer.id).filter_by(account_id=accountId).all()
    CustomerId = Customer.query.filter(Customer.account_id == accountId).all()
    #user_con = db.session.query(func.count(Contract.id)).filter(Contract.customer_id.in_(customerId)).scalar()
    cuslist = []
    for cus in CustomerId:
        cuslist.append(cus.id)
    user_con = db.session.query(Contract.id).filter(Contract.customer_id.in_(cuslist)).count()

    # 收费统计数据
    sum_char = db.session.query(func.sum(Record.charge)).scalar()
    sum_char = float(sum_char)
    contractId = Contract.query.filter(Contract.customer_id.in_(cuslist)).all()
    conlist = []
    for con in contractId:
        conlist.append(con.id)
    user_char = db.session.query(func.sum(Record.charge)).filter(Record.contract_id.in_(conlist)).scalar()
    user_char = float(user_char)

    data = {}
    data['sum_cus'] = sum_cus
    data['user_cus'] = user_cus
    data['sum_con'] = sum_con
    data['user_con'] = user_con
    data['sum_char'] = sum_char
    data['user_char'] = user_char

    jsonData = []
    jsonData.append(data)
    jsondatar = json.dumps(jsonData, ensure_ascii=False)
    jsondatar = '{"data":' + jsondatar + "}"
    return jsondatar

