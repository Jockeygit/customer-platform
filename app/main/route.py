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
from operator import and_, or_

import xlwt as xlwt
from flask import render_template, flash, url_for, request, jsonify, current_app, Response, send_from_directory
from sqlalchemy import func,extract
from sqlalchemy.testing import in_
from werkzeug.utils import secure_filename
from app.main import view, forms
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from app.model import *
from xlrd import open_workbook
import json, time
import os


def to_dict(row):
    """
    将查询所得的行转化为字典
    :param row:
    :return:
    """
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

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
            result = str(list(add_custom_form.errors.values())[0]).strip("[]'")
            return jsonify({'result': '%s' % result})


@view.route('/customer/import', methods=['POST'])
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
            customer = Customer()
            if Customer.query.filter(Customer.name == row_date[0]).first():
                return jsonify({'result': "2"})
            else:
                customer.name = row_date[0]
            if row_date[1] == u"个人":
                customer.type = 0
            else:
                customer.type = 1
            customer.phone = row_date[2]
            customer.email = row_date[3]
            customer.address = row_date[4]
            if Employee.query.filter(Employee.name ==row_date[5]).first():
                manager_id = db.session.query(Employee.id).filter_by(name=row_date[5]).first()[0]
            else:
                print("客户经理不存在")
                return jsonify({'result': "0"})
            customer.account_id = manager_id
            db.session.add(customer)
            db.session.commit()
            db.session.close()
           # os.remove(file_path)  # 删除导入的文件
    return jsonify({'result': "1"})


@view.route('/customer/export', methods=['POST'])
@login_required
def customer_export():
    # web.header('Content-type', 'application/vnd.ms-excel')  # 指定返回的类型

    # web.header('Transfer-Encoding', 'chunked')
    # web.header('Content-Disposition', 'attachment;filename="export.xls"')  # 设定用户浏览器显示的保存文件名

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
        del (row[0])
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
    # print(request.data)
    # print(json.loads(request.data)["name"])
    data = request.data
    id = json.loads(data)["id"]
    try:
        customer = Customer.query.filter(Customer.id == id).first()
        contract = Contract.query.filter(Contract.customer_id == customer.id).first()
        if contract:
            record = Record.query.filter(Record.contract_id == contract.id).first()
            if record:
                db.session.delete(record)
                db.session.commit()
            db.session.delete(contract)
            db.session.commit()
        db.session.delete(customer)
        db.session.commit()
    except Exception:
        return jsonify({'result': '0'})
    return jsonify({'result': '1'})


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
        Data["cus_id"] = cus.id
        contract = Contract.query.filter(Contract.customer_id == cus.id).first()
        print(contract)
        if contract:
            Data["id"] = contract.id
            Data["is_create"] = 1
            if contract.status == 0:
                Data['status'] = u"未生效"
            else:
                Data['status'] = u"生效"
            Data["start_date"] = contract.start_date
            Data["expiry_date"] = contract.expiry_date

            # 是否收费
            record = Record.query.filter(Record.contract_id == contract.id).first()
            if record:
                Data["is_charge"] = "1"
            else:
                Data["is_charge"] = contract.isCheck

            # 服务项目
            agree_name = ''
            agreements = contract.agreements.all()
            for agree in agreements:
                agree_name = agree_name + " " + agree.name

            Data['agreements'] = agree_name
        else:
            Data["is_create"] = 0
            Data['status'] = ' '
            Data["start_date"] = ' '
            Data["expiry_date"] = ' '
            Data["is_charge"] = ' '
            Data['agreements'] = ' '

        jsonData.append(Data)

    jsondatar = json.dumps(jsonData, ensure_ascii=False)
    jsondatar = jsondatar.replace("null", '"-"')
    jsondatar = '{"data":' + jsondatar + "}"
    return jsondatar


@view.route('/contract/add/<id>', methods=['POST'])
@login_required
def contract_add(id):
    contact_form = forms.contractFrom()
    if contact_form.validate_on_submit():
        contact = Contract(start_date=contact_form.startDate.data, expiry_date=contact_form.expiryDate.data,
                           status=contact_form.status.data, isCheck=0,
                           customer_id=id)
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
        return jsonify({'result': '1'})

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
        # 查询是否有收费记录
        record = Record.query.filter(Record.contract_id == contract.id).first()
        if record:
            db.session.delete(record)
            db.session.commit()
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
    charge = '%.2f' % float(charge)
    return jsonify({'result': '%s' % charge})


@view.route('/contract/char', methods=['POST'])
@login_required
def contract_char():
    data = request.data
    data = json.loads(data)
    if Record.query.filter(Record.contract_id == data["id"]).first():
        return jsonify({'result': '2'})
    try:
        record = Record(charge=data["charge"], charge_date=data["charge_date"],
                        description=data["description"], contract_id=data["id"])
        db.session.add(record)
        db.session.commit()
        return jsonify({'result': '1'})
    except Exception:
        return jsonify({'result': '0'})


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
            print(record)
            if record:
                Data["id"] = record.id
                charge = '%.2f' % float(record.charge)
                Data["charge"] = charge
                Data["charge_date"] = record.charge_date
                Data["description"] = record.description

                jsonData.append(Data)

    jsondatar = json.dumps(jsonData, ensure_ascii=False)
    jsondatar = jsondatar.replace("null", '"-"')
    jsondatar = '{"data":' + jsondatar + "}"
    return jsondatar


@view.route('/record/undo', methods=['POST'])
@login_required
def record_undo():
    data = request.data  # 存放record.id
    id = json.loads(data)['id']
    print(id)
    try:
        record = Record.query.filter(Record.id == id).first()
        db.session.delete(record)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'result': '0'})
    return jsonify({'result': '1'})


# 待办事项
@view.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    print(request.data)
    form = forms.todolistFrom()
    return render_template('todo.html')


@view.route('/subtodo', methods=['GET', 'POST'])
@login_required
def subtodo():
    print(request.data)
    # form = forms.todolistFrom()
    return render_template('subtodo.html')


@view.route('/todo/listJson', methods=['GET'])
@login_required
def todo_list():
    accountId = db.session.query(User.account_id).filter_by(id=current_user.id).first()[0]
    category1 = db.session.query(Category).filter_by(account_id=accountId).all()
    category2 = db.session.query(Category).filter(Category.id.in_([1, 2])).all()
    category = category1 + category2

    catedata = []
    categoryMap = {}
    for cate in category:
        todo = cate.todolists
        Data = {}
        Data["cate_id"] = cate.id
        Data["name"] = cate.name
        Data["count"] = len(todo)

        catedata.append(Data)

        for list in todo:
            Data = {}
            Data["todo_id"] = list.id
            Data["content"] = list.content
            Data["deadline"] = list.deadline
            if list.category_id not in categoryMap.keys():
                categoryMap[list.category_id] = []
            categoryMap[list.category_id].append(Data)

    todojson = json.dumps(categoryMap, ensure_ascii=False)
    catejson = json.dumps(catedata, ensure_ascii=False)
    jsondatar = '{"todo":' + todojson + ',"category":' + catejson + '}'

    return jsondatar

@view.route('/category/add', methods=['POST'])
def new_category():
    data = request.data  # 存放record.id
    name = json.loads(data)['name']
    accountId = db.session.query(User.account_id).filter_by(id=current_user.id).first()[0]
    try:
        category = Category(name=name,account_id=accountId)
        db.session.add(category)
        db.session.commit()
    except Exception:
        return jsonify({'result': '0'})
    return jsonify({'result': '1'})

@view.route('/category/del', methods=['POST'])
@login_required
def cate_del():
    data = request.data  # 存放todolist.id
    id = json.loads(data)['id']
    try:
        category = Category.query.filter(Category.id == id).first()
        db.session.delete(category)
        db.session.commit()
    except Exception:
        return jsonify({'result': '0'})
    return jsonify({'result': '1'})

@view.route('/todo/add', methods=['POST'])
@login_required
def todo_add():
    data = request.data  # 存放record.id
    name = json.loads(data)['name']
    category = json.loads(data)['category']
    try:
        todo = Todolist(content=name, category_id=category, is_finish=0, deadline="")
        db.session.add(todo)
        db.session.commit()
    except Exception:
        return jsonify({'result': '0'})
    return jsonify({'result': '1'})


@view.route('/todo/update', methods=['POST'])
@login_required
def todo_update():
    data = request.data  # 存放record.id
    id = json.loads(data)['id']
    content = json.loads(data)['content']
    deadline = json.loads(data)['deadline']
    try:
        todo = Todolist.query.filter(Todolist.id == id).first()
        print(todo)
        todo.content = content
        todo.deadline = deadline
        db.session.add(todo)
        db.session.commit()
    except Exception:
        return jsonify({'result': '0'})
    return jsonify({'result': '1'})

@view.route('/todo/finish', methods=['POST'])
@login_required
def todo_finish():
    data = request.data  # 存放record.id
    id = json.loads(data)['id']
    try:
        todo = Todolist.query.filter(Todolist.id == id).first()
        todo.category_id = 2
        db.session.add(todo)
        db.session.commit()
    except Exception:
        return jsonify({'result': '0'})
    return jsonify({'result': '1'})

@view.route('/todo/del', methods=['POST'])
@login_required
def todo_del():
    data = request.data  # 存放todolist.id
    id = json.loads(data)['id']
    try:
        todolist = Todolist.query.filter(Todolist.id == id).first()
        db.session.delete(todolist)
        db.session.commit()
    except Exception:
        return jsonify({'result': '0'})
    return jsonify({'result': '1'})


# 部门设置
@view.route('/depart', methods=['GET', 'POST'])
@login_required
def depart():
    print(request.data)
    add_depart_form = forms.departmentFrom()
    update_depart_form = forms.departmentFrom()
    return render_template('department.html', add_depart_form=add_depart_form)


@view.route('/depart/listJson', methods=['GET'])
@login_required
def depart_list():
    jsonData = []
    departments = Department.query.filter().all()
    for department in departments:
        depdata = {}
        employeename = ''
        depdata['name'] = department.name
        depdata['id'] = department.id
        director = Employee.query.filter(
            and_(Employee.department_id == department.id, Employee.position_id == 1)).first()
        if director:
            depdata['director'] = director.name
        else:
            depdata['director'] = ' '
        emp_count = db.session.query(Employee.id).filter(Employee.department_id == department.id).count()
        # emp_count = db.session.query(Employee.id).filter(and_(Employee.department_id==department.id, Employee.position_id!=1)).count()
        depdata['count'] = emp_count
        if department.parent_id != department.id:
            depdata['parentId'] = department.parent_id
        jsonData.append(depdata)
    depnone = {}
    depnone['name'] = '未分配'
    depnone['director'] = ' '
    depnone['id'] = 0
    emp_count = Employee.query.filter(Employee.department_id == None).count()
    depnone['count'] = emp_count
    jsonData.append(depnone)

    jsondatar = json.dumps(jsonData, ensure_ascii=False)
    jsondatar = jsondatar.replace("null", '" "')
    return jsondatar

@view.route('/depart/add', methods=['POST'])
@login_required
def depart_add():
    form = forms.departmentFrom()
    if form.validate_on_submit():
        department = Department(name=form.name.data, parent_id=form.parent.data)
        db.session.add(department)
        db.session.commit()
        return jsonify({'result': '1'})
    else:
        if form.errors:
            result = str(list(form.errors.values())[0]).strip("[]'")
            return jsonify({'result': '%s' % result})


@view.route('/depart/update/<id>', methods=['POST'])
@login_required
def depart_update(id):
    form = forms.departmentFrom()
    if form.validate_on_submit():
        department = Department.query.filter(Department.id==id).first()
        department.name = form.name.data
        department.parent_id = form.parent.data
        db.session.add(department)
        db.session.commit()
        return jsonify({'result': '1'})
    else:
        if form.errors:
            result = str(list(form.errors.values())[0]).strip("[]'")
            return jsonify({'result': '%s' % result})


@view.route('/depart/del', methods=['POST'])
@login_required
def depart_del():
    data = request.data  # 存放department.id
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

@view.route('/employee', methods=['GET', 'POST'])
@login_required
def employee():
    employee_form = forms.employeeFrom()
    return render_template('employee.html', employee_form=employee_form)


@view.route('/employee/listJson', methods=['GET'])
@login_required
def emploee_list():
    jsonData = []
    employees = Employee.query.filter().all()
    for emp in employees:
        Date={}
        Date["id"] = emp.id
        Date["name"] = emp.name
        if emp.department_id:
            depart = Department.query.filter(Department.id==emp.department_id).first().name
        else:
            depart="-"
        Date["department"] = depart
        if emp.position_id:
            position = Position.query.filter(Position.id==emp.position_id).first().name
        else:
            position="-"
        Date["position"] = position

        jsonData.append(Date)

    jsondatar = json.dumps(jsonData, ensure_ascii=False)
    jsondatar = jsondatar.replace("null", '"-"')
    jsondatar = '{"data":' + jsondatar + "}"
    return jsondatar

@view.route('/employ/update/<id>', methods=['POST'])
@login_required
def emptyloy_update(id):
    form = forms.employeeFrom()
    if form.validate_on_submit():
        employee = Employee.query.filter(Employee.id ==id).first()
        employee.name = form.name.data
        employee.department_id = form.department.data
        employee.position_id = form.position.data
        db.session.add(employee)
        db.session.commit()
        return jsonify({'result': '1'})
    else:
        if form.errors:
            result = str(list(form.errors.values())[0]).strip("[]'")
            return jsonify({'result': '%s' % result})

# 工作报告
@view.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    print(request.data)
    form = forms.reportForm()
    return render_template('report.html',form=form)


@view.route('/report/data', methods=['GET'])
@login_required
def report_data():
    # 客户统计数据
    accountId = db.session.query(User.account_id).filter_by(id=current_user.id).first()[0]
    sum_cus_per = db.session.query(func.count('*')).filter(and_(Customer.id > 0, Customer.type == 0)).scalar()
    user_cus_per = db.session.query(func.count('*')).filter(and_(Customer.account_id == accountId, Customer.type == 0)).scalar()

    sum_cus_com = db.session.query(func.count('*')).filter(and_(Customer.id > 0, Customer.type == 1)).scalar()
    user_cus_com = db.session.query(func.count('*')).filter(and_(Customer.account_id == accountId, Customer.type == 1)).scalar()

    # 合同统计数据
    sum_con = db.session.query(func.count('*')).filter(Contract.id > 0).scalar()
    CustomerId = Customer.query.filter(Customer.account_id == accountId).all()
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

    data = {}
    data['sum_cus_per'] = sum_cus_per
    data['user_cus_per'] = user_cus_per
    data['sum_cus_com'] = sum_cus_com
    data['user_cus_com'] = user_cus_com

    data['sum_con'] = sum_con
    data['user_con'] = user_con
    data['sum_char'] = sum_char
    if user_char:
        data['user_char'] = int(user_char)
    else:
        data['user_char'] = 0

    jsonData = []
    jsonData.append(data)
    jsondatar = json.dumps(jsonData, ensure_ascii=False)
    jsondatar = '{"data":' + jsondatar + "}"
    return jsondatar

# 工作报告
@view.route('/report/listJson', methods=['POST'])
@login_required
def report_list():
    data = request.data
    year = json.loads(data)['year']
    month = json.loads(data)['month']
    accountId = json.loads(data)['id']
    my_accountId = db.session.query(User.account_id).filter_by(id=current_user.id).first()[0]
    if accountId == 0:
        accountId = my_accountId
    reports = db.session.query(Report).filter(Report.account_id==accountId).filter(
        and_(extract('month', Report.modify_time) == month, extract('year', Report.modify_time) == year)).order_by(Report.modify_time.desc())
    count = db.session.query(Report).filter_by(account_id=accountId).count()
    data = {}
    data["data"] = []
    for report in reports:
        print(to_dict(report))
        data["data"].append(to_dict(report))
    if data["data"]:
        data["result"] = 1
    else:
        if accountId!=my_accountId or year!=datetime.now().year or month!=datetime.now().month:
            data["result"] = 0
    data["count"] = count
    data["user"] = my_accountId
    dateJson = json.dumps(data, ensure_ascii=False)
    return dateJson

@view.route('/report/query', methods=['POST'])
@login_required
def report_query():
    data = request.data
    date = json.loads(data)['date']
    accountId = json.loads(data)['id']
    if accountId == 0:
        accountId = db.session.query(User.account_id).filter_by(id=current_user.id).first()[0]
    report = db.session.query(Report).filter(Report.account_id==accountId).filter(
        and_(Report.account_id==accountId, db.cast(Report.modify_time, db.DATE) == db.cast(date, db.DATE))).first()
    return_data = {}
    if report:
        return_data["result"] = 1
        return_data["data"] = to_dict(report)
    else:
        return_data["result"] = 0
    print(json.dumps(return_data, ensure_ascii=False))
    return json.dumps(return_data, ensure_ascii=False)

@view.route('/report/update', methods=['POST'])
@login_required
def report_update():
    data = request.data
    content = json.loads(data)['content']
    accountId = db.session.query(User.account_id).filter_by(id=current_user.id).first()[0]
    report = db.session.query(Report).filter(
        and_(Report.account_id == accountId,  db.cast(Report.modify_time, db.DATE) == db.cast(datetime.now(), db.DATE))).first()
    print(report)
    if report:
        report.content = content
        report.modify_time = datetime.now()
    else:
        report = Report(content=content, modify_time=datetime.now(), account_id=accountId)
    try:
        db.session.add(report)
        db.session.commit()
        return jsonify({'result': '1'})
    except:
        return jsonify({'result': '0'})