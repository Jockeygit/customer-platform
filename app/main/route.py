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
from flask import render_template, flash, url_for, request, jsonify
from app.main import view, forms
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from app.model import *
import json


# 首页
@view.route('/index')
@login_required
def index():
    return render_template('index.html')


# 客户
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
            result=str(list(form.errors.values())[0]).strip("[]'")
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


#合同
@view.route('/contact', methods=['GET'])
@login_required
def contact():
    form = forms.contractFrom()

    return render_template("contact.html", form=form)


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
                Data['status'] = u"失效"
            else:
                Data['status'] = u"生效"
            Data["start_date"] = contract.start_date
            Data["expiry_date"] = contract.expiry_date
            Data["is_charge"] = contract.isCheck

            # 服务项目
            agree_name = ''
            agreements = contract.agreements.all()
            for agree in agreements:
                agree_name = agree_name + agree.name

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