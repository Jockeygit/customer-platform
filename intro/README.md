# customer-platform
### 项目说明

2018年毕设项目

- 一个简单的客户管理系统，实现了简单的登录注册
- 包含数据统计、客户管理、合同收费、待办事项、工作报告、部门设置等功能
- 基于flask和sql-achemy，前端运用了bootStrap模板

#### 页面展示

![image-20201210113002837](cms-首页.png)

![image-20201210113002837](cms-客户.png)

![image-20201210113133391](cms-合同.png)

![image-20201210113200152](cms-收费记录.png)

![image-20201210113234068](cms-待办事项.png)

![image-20201210113411669](cms-工作报告.png)



### 安装Flask

```
pip install Flask
```

可以使用镜像源加速下载



### 最简单的Flask应用

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
```

1. 引入 Flask类
2. 创建一个Flask实例，第一个参数是应用模块或者包的名称，这样 Flask 才会知道去哪里寻找模板、静态文件
3. 使用修饰器route()，绑定URL和函数之间的映射关系，函数返回我们想要显示在页面上的信息
4. 使用app.run()在本地运行服务，WSGI工具包可以实现简单的http服务器
5. 默认使用本机IP，端口号是5000



IP地址可以在run()方法里进行修改，同一网段下其他机器也可以访问

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5007')
```



### 路由

用户请求的URL与视图函数之间的映射。Flask框架 根据HTTP请求的URL在路由表中匹配预定义的URL规则，找到

对应的视图函数， 并将视图函数的执行结果返回服务器

```python
@app.route('/')
def index():
    return 'This is home page!'
    
@app.route('/hello')
def hello_world():
    return 'Hello World!'
```



### 模板

Flask使用 Jinja2模板引擎，进行模板的渲染，主要用到的方法是render_template()

需要传递的参数是：

1. 模板的名字，即html的名字

2. 模板中的关键字参数

   它将导入的变量替换掉模板中的变量占位符，并返回渲染后的模板。

```python
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', user=user)
```

```
<html>
  <head>
    <title>{{title}} - microblog</title>
  </head>
  <body>
      <h1>Hello, {{user.nickname}}!</h1>
  </body>
</html>
```



### 模板继承

Flask中的模板可以继承，通过继承可以把模板中许多重复出现的元素抽取出来，放在父模板中，并且父模板通过

定义block给子模板开一个口，子模板根据需要，再实现这个block。

模板的继承主要是为了减少前端代码量

```html
#index.html
{% extends "base.html" %}　　　　　　#代表继承base.html

{% block main %}　　　　　　　　　　　　　　　　#这里的main要与base.html里blcok的设定的名字相同　　
    <h1>这是index页面</h1>　　　　　　　　　　　#将这里的内容传到base.html的block下，并在本文件里应用
{% endblock %}

```

```
#login.html
{% extends "base.html" %}

{% block main %}
    <h1>这是登陆页面</h1>
{% endblock %}
```



### 重定向

redirect()函数把用户重定向到其它地址，url_for()通过视图函数名字返回对应的URL

```
@app.route('/hi')
def hi():
    return redirect(url_for('index'))
```



### 表单

表单是收集用户数据信息的各种表单元素的集合区域。它的作用是实现网页上的数据交互。

收集客户端输入的数据信息，提交到网站服务器端进行处理，可以进行一些简单的前端校验

Flask-WTF中的WTForms可以实现表单的功能

参数FlaskForm表示：customerForm继承FlaskForm类，可以调用父类的一些方法

```python
form.py
# 客户表单
class customerForm(FlaskForm):

    customername = StringField('客户名称', validators=[length(1, 20)])
    phone = StringField('电话', validators=[length(1, 15)])
    email = StringField('邮箱', validators=[length(1, 20)])
    address = StringField('地址', validators=[length(1, 30)

    submit_customer = SubmitField('保存')
```



### 数据库

ORM（Object-Relational Mapping），就是把关系数据库的表结构映射到对象上，把对数据库的操作转化成

对对象的操作，Flask-SQLchemy 可以直接对每个 model 进行不同的 CRUD 操作

1. 安装mysql，创建数据库，设置密码
2. 安装Flask-SQLchemy

```
pip install Flask_sqlalchemy
```

3. 配置本地数据库地址，格式如下

```python
  # 配置mac数据库地址(格式：mysql://username:password@hostname/database)
      
  app.config['SQLALCHEMY_DATABASE_URI'] = 
  
  'mysql://root:5185425mysql@localhost:3306/mydatabase'
```

4. 实例化一个SQLAlchemy()类，初始化app

```
db = SQLAlchemy()

db.init_app(app)
```

5. 创建数据库模型，一个类和一张表对应，逐个字段对应

当 class User 继承自 db.Model 时, SQLAlchemy 与 数据库的连接通过就已经自动的绑定了.db.Column: 其构造器的第一个参数是可选的, 如果传入实参时, 表示创建的字段名. 反之, 则默认使用该实例化对象的名字(即 User 的类属性名); 第二个参数指定了字段的数据类型.

```python
model.py

# 客户表
class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False, unique=True)
    type = db.Column(db.Integer, nullable=False, unique=False)
    phone = db.Column(db.String(30), nullable=True, unique=False)
    email = db.Column(db.String(30), nullable=True, unique=False)
    address = db.Column(db.String(35), nullable=True, unique=False)
    # account_id引用employee表中的id
    account_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

```

6. 根据数据库模型创建表

Flask-SQLchemy会去读取当前导入的模型并映射到数据库中

```python
from app import db

with app.app_context():
    
     db.create_all()
     
     #db.drop_all()
```

7. 数据库的操作：crud

```python
# 查询客户表里名字为税友的数据
customer = Customer.query.filter(Customer.name == “税友”).all()
# 增加/删除/更新 都涉及到事务的提交
db.session.delete(customer)
db.session.add(customer)
db.session.commit()
```

8. 数据库迁移框架

数据库迁移框架能跟踪数据库模式的变化，然后增量式的把变化应用到数据库中。

安装Flask-Migrate 

```
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
```

```
python main.py db init   

创建迁移仓库。会在你项目下生成migrations/目录，保存你数据库每次变更的内容

修改User类。 
python main.py db migrate 

创建迁移脚本。会根据模型定义和数据库当前状态的差异，生成upgrade()和downgrade()函数的内容。 

python main.py db upgrade 执行修改，更新数据库

再看User表，已经改变。 
python main.py db downgrade 回退修改

```

9. 表结构一览

   **用户表（user）**

   | 字段名称 | 字段名     | 字段说明    | 数据类型 | 允许为空 | 唯一 | 是否外键 |
   | -------- | ---------- | ----------- | -------- | -------- | ---- | -------- |
   | id       | id         | 主键        | int      | 否       | 是   | 否       |
   | 用户名   | username   | 邮箱        | string   | 否       | 是   | 否       |
   | 密码     | password   |             | string   | 否       | 否   | 否       |
   | 员工id   | account_id | employee.id | int      | 是       | 是   | 是       |

   注册的时候，真实姓名、邮箱、密码补充完整，然后进行登录

   **员工表（employee）**

   | 字段名称 | 字段名        | 字段说明      | 数据类型 | 允许为空 | 唯一 | 是否外键 |
   | -------- | ------------- | ------------- | -------- | -------- | ---- | -------- |
   | id       | id            | 主键          | int      | 否       | 是   | 否       |
   | 员工名   | name          | 真实姓名      | string   | 否       | 是   | 否       |
   | 部门     | department_id | department.id | Int      | 是       | 是   | 是       |
   | 职位     | position_id   |               | int      | 是       | 是   | 是       |

   **部门表（department）**

   | 字段名称 | 字段名 | 字段说明 | 数据类型 | 允许为空 | 唯一 | 是否外键 |
   | -------- | ------ | -------- | -------- | -------- | ---- | -------- |
   | id       | id     | 主键     | int      | 否       | 是   | 否       |
   | 部门名   | name   |          | string   | 否       | 是   | 否       |

   **职位表（position）**

   | 字段名称 | 字段名 | 字段说明                       | 数据类型 | 允许为空 | 唯一 | 是否外键 |
   | -------- | ------ | ------------------------------ | -------- | -------- | ---- | -------- |
   | id       | id     | 主键                           | int      | 否       | 是   | 否       |
   | 职位名   | name   | 普通员工、部门主管、机构负责人 | string   | 否       | 是   | 否       |

   普通员工：1

   部门主管：2

   机构负责人：3

   **客户表（customer）**

   | 字段名称 | 字段名     | 字段说明             | 数据类型 | 允许为空 | 唯一 | 是否外键 |
   | -------- | ---------- | -------------------- | -------- | -------- | ---- | -------- |
   | id       | id         | 主键                 | int      | 否       | 是   | 否       |
   | 客户名称 | name       |                      | string   | 否       | 是   | 否       |
   | 客户类型 | type       | 企业（1）、个人（0） | int      | 否       | 否   | 否       |
   | 电话     | phone      |                      | string   | 否       | 是   |          |
   | 邮箱     | email      |                      | string   | 是       | 否   | 否       |
   | 地址     | address    |                      | string   | 是       | 否   | 否       |
   | 客户经理 | manager_id | employee.id          | int      | 是       | 是   | 是       |

   **合同表（contract）**

   | 字段名称 | 字段名       | 字段说明            | 数据类型 | 允许为空 | 唯一 | 是否外键 |
   | -------- | ------------ | ------------------- | -------- | -------- | ---- | -------- |
   | id       | id           | 主键                | int      | 否       | 是   | 否       |
   | 到期日   | expiry_date  |                     | Data     | 否       | 否   | 否       |
   | 状态     | status       | 是否生效()          | int      | 否       | 否   | 否       |
   | 是否收费 | isCharge     | 是否收费（0否 1是） | int      | 否       | 否   | 否       |
   | 关联客户 | customer_id  | customer.id         | Int      | 否       | 是   | 是       |
   | 服务项目 | agreement_id | agreement.id        | int      | 是       | 否   | 否       |

   注：一个客户只有一个合同，一个合同只有一个服务项目

   **服务项目表（agreement）**

   | 字段名称     | 字段名 | 字段说明 | 数据类型 | 允许为空 | 唯一 | 是否外键 |
   | ------------ | ------ | -------- | -------- | -------- | ---- | -------- |
   | id           | id     | 主键     | int      | 否       | 是   | 否       |
   | 服务项目名称 | name   |          | string   | 否       | 是   | 否       |
   | 价格         | price  |          | string   | 否       | 否   | 否       |

   **合同-服务项目表（contract_agreement）**

   | 字段名称 | 字段名       | 字段说明     | 数据类型 | 允许为空 | 唯一 | 是否外键 |
   | -------- | ------------ | ------------ | -------- | -------- | ---- | -------- |
   | id       | id           | 主键         | int      | 否       | 是   | 否       |
   | 合同     | contract_id  | contract.id  | Int      | 否       | 否   | 是       |
   | 服务项目 | agreement_id | agreement.id | Int      | 否       | 否   | 是       |

   **收费记录表（record）**

   | 字段名称 | 字段名      | 字段说明    | 数据类型 | 允许为空 | 唯一 | 是否外键 |
   | -------- | ----------- | ----------- | -------- | -------- | ---- | -------- |
   | id       | id          | 主键        | int      | 否       | 是   | 否       |
   | 说明     | description |             | string   | 是       | 否   | 否       |
   | 金额     | charge      |             | Int      | 否       | 否   | 否       |
   | 收款时间 | chargedate  |             | date     | 否       | 否   | 否       |
   | 合同id   | contract_id | contract.id | int      | 否       | 是   | 是       |

   **待办事项（todolist）**

   | 字段名称 | 字段名     | 字段说明    | 数据类型 | 允许为空 | 唯一 | 是否外键 |
   | -------- | ---------- | ----------- | -------- | -------- | ---- | -------- |
   | id       | id         | 主键        | int      | 否       | 是   | 否       |
   | 内容     | content    |             | string   | 否       | 否   | 否       |
   | 员工     | account_id | employee.id | Int      | 否       | 否   | 是       |



### 接口定义

**1. 客户模块**

**增加客户：addCustomer**

| 方法描述   | 新增客户                                                     |
| ---------- | ------------------------------------------------------------ |
| class      | CustomerFacade                                               |
| method     | addCustomer                                                  |
| 参数说明   | "customeraName"：{客户名称}"type"：{客户类型  0个人  1企业}"phone"：{电话号码}"email"：{邮箱}"address"：{地址}"manager"：{客户经理} |
| 返回值说明 | null                                                         |

注：1. 有必要时，增加客户重名校验   2. 客户经理默认为本人，可更改为下属

**查询客户列表：queryCustomers**

| 方法描述   | 查询客户列表                                                 |
| ---------- | ------------------------------------------------------------ |
| class      | CustomerFacade                                               |
| method     | queryCustomers                                               |
| 参数说明   | "accountId"：{list：员工id}"nameOrlike"：{查询关键词}"pageNo"：{当前页码}  默认为1"pageSize"：{分页条数} |
| 返回值说明 | CustomerDict:"customerName"：{客户名称}"type"：{客户类型  0个人  1企业}"phone"：{电话号码}"email"：{邮箱}"address"：{地址}"manager"：{客户经理} |

注：部门主管会返回自己以及下属作为客户经理的客户

**删除客户：deleteCustomer**

| 方法描述   | 删除单个客户           |
| ---------- | ---------------------- |
| class      | CustomerFacade         |
| method     | deleteCustomer         |
| 参数说明   | "customerId"：{客户id} |
| 返回值说明 | null                   |

注：删除客户后，需要再次调用查询客户接口，刷新客户列表

**更新客户：updateCustomer**

| 方法描述   | 更新单个客户                                                 |
| ---------- | ------------------------------------------------------------ |
| class      | CustomerFacade                                               |
| method     | updateCustomer                                               |
| 参数说明   | CustomerDict:"customerId"：{客户id}"customerName"：{客户名称}"type"：{客户类型  0个人  1企业}"phone"：{电话号码}"email"：{邮箱}"address"：{地址}"manager"：{客户经理} |
| 返回值说明 | log：更新成功 - 更新失败                                     |

注：更新客户后，需要再次调用查询客户接口，刷新客户列表

**导入客户：importCustomer**

| 方法描述   | 批量导入客户                              |
| ---------- | ----------------------------------------- |
| class      | CustomerFacade                            |
| method     | importCustomer                            |
| 参数说明   | excel                                     |
| 返回值说明 | "failed"：{失败条数}"success"：{成功条数} |

**2. 合同模块**

**查询合同列表：getContracts**

| 方法描述   | 查询、筛选合同列表                                           |
| ---------- | ------------------------------------------------------------ |
| class      | ContractFacade                                               |
| method     | getContracts                                                 |
| 参数说明   | "accountId"：{list：员工id}"nameOrlike"：{查询关键词}"pageNo"：{当前页码}  默认为1"pageSize"：{分页条数} |
| 返回值说明 | ContractDict:"customerName"：{客户名称}"status"：{是否生效  0无效  1生效}"create"：{是否创建   true   false}"agreement"：{服务项目}"expiryDate"：{到期日}''isCharge"：{是否收费} |

注：合同未创建时，是否生效、服务项目、到期日都显示空白

**新建合同：createContract**

| 方法描述   | 创建合同               |
| ---------- | ---------------------- |
| class      | ContractFacade         |
| method     | createContract         |
| 参数说明   | "customerId"：{客户id} |
| 返回值说明 | "contractId"：{合同id} |

注：合同创建后，需要调用查询接口刷新合同列表

**删除合同：deleteContract**

| 方法描述   | 删除合同                                      |
| ---------- | --------------------------------------------- |
| class      | ContractFacade                                |
| method     | deleteContract                                |
| 参数说明   | "customerId"：{客户id} "contractId"：{合同id} |
| 返回值说明 | null                                          |

注：合同删除后，需要调用查询接口刷新合同列表

**更新合同：updateContract**

| 方法描述   | 编辑合同信息                                                 |
| ---------- | ------------------------------------------------------------ |
| class      | ContractFacade                                               |
| method     | updateContract                                               |
| 参数说明   | "customerId"：{客户id} "contractId"：{合同id}"agreementId"：{服务项目id}"expiryDate"：{到期日} |
| 返回值说明 | null                                                         |

**获取所有服务项目：queryAgreements**

| 方法描述   | 获取所有可选的服务项目            |
| ---------- | --------------------------------- |
| class      | ContractFacade                    |
| method     | queryAgreements                   |
| 参数说明   | null                              |
| 返回值说明 | "name"：{服务项目}"price"：{价格} |

**点击收费：querychargeByDate**

| 方法描述   | 点击收费，收费弹窗                               |
| ---------- | ------------------------------------------------ |
| class      | ContractFacade                                   |
| method     | querychargeByDate                                |
| 参数说明   | "customerId"：{客户id} "contractId"：{合同id}    |
| 返回值说明 | "charge"：{应收费用}"date"：{收费日期：当前日期} |

**收费：updateCharge**

| 方法描述   | 合同收费，生成收费记录                                       |
| ---------- | ------------------------------------------------------------ |
| class      | ContractFacade                                               |
| method     | updateCharge                                                 |
| 参数说明   | "customerId"：{客户id}"charge"：{应收费用}"description"：{说明}"date"：{收款时间} |
| 返回值说明 | null                                                         |

**查询收费记录：queryChargeRecord**

| 方法描述   | 查询收费记录                                                 |
| ---------- | ------------------------------------------------------------ |
| class      | ContractFacade                                               |
| method     | queryChargeRecord                                            |
| 参数说明   | "accountId"：{list：员工id}"nameOrlike"：{查询关键词}"pageNo"：{当前页码}  默认为1"pageSize"：{分页条数} |
| 返回值说明 | "customerName"：{客户名称} "description"：{说明} "charge"：{收取金额} "date"：{收款日期} |

**撤销收费记录：undoChargeRecord**

| 方法描述   | 撤销收费记录                                   |
| ---------- | ---------------------------------------------- |
| class      | ContractFacade                                 |
| method     | undoChargeRecord                               |
| 参数说明   | "customerId"：{客户id}"recordId"：{收费记录id} |
| 返回值说明 | null                                           |

**3. 待办事项**

**查询待办事项：queryToDoList**

| 方法描述   | 撤销收费记录          |
| ---------- | --------------------- |
| class      | ToDoFacade            |
| method     | queryToDoList         |
| 参数说明   | "accountId"：{员工id} |
| 返回值说明 | "content"：{内容}     |

#### 查询列表（GET）

1. 点击客户tab时，通过url_for()方法，获取customer函数的URL，并且跳转
2. 触发customer()函数，开始渲染customer模板
3. 在渲染过程中，调用JQuery事件方法，触发绑定函数
4. datatable类里发送ajax请求，请求的URL会路由到customer_list()函数
5. customer_list()函数通过session里携带的UserId查询出当前用户下的客户
6. 把查询的客户序列化成JSON格式返回给前端
7. 模板引擎把返回的数据渲染到页面上，列表查询就完成了



模板也可以发请求

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <title>login</title>
  </head>
  <body>
    <form  style="margin:20px;border:1px solid red" method="post" action="/login">
        <span>username:</span><input type="text" name="username" id="username"><br/>
        <span>password:</span><input type="password" name="password" id="password"><br/>
        <button type="submit" id="loginBtn">login</button>
    </form>
    {% if error %}
        <h1 style="color:red">{{ error }}!</h1>
    {% endif %}
  </body>
</html>
```





#### 新增客户（POST）

1. 点击客户tab时，customer函数里实例化了客户表单对象
2. 在调用渲染方法时，把这个客户表单对象作为参数传给前端模板，程序通过这个表单和网页交互
3. 填好客户信息，提交表单后，调用ajaxForm()方法，参数是客户表单的id属性
4. ajaxForm()通过客户表单实例化一个表单对象，对象里包含提交的表单数据
5. 发送ajax请求，把表单数据post给后端，请求的URL会路由到customer_add()函数
6. customer_add()将接收的表单数据转化成数据库模型对象，添加到数据库中，返回结果码1
7. ajaxForm()获取到成功的结果，利用reload()方法重新加载表格数据，刷新列表利用flask搭建一个web应用