
/*------------------------------------------------------
    Author :     zhoujie
    Description :     添加描述信息
---------------------------------------------------------  */
       //customerList存放所有客户信息
        customerList = {};
        del_id = "";
        uodate_id = "";
        $(document).ready(function () {
            $('#dataTables-example').dataTable({
                "oLanguage": {
                 "sSearch":"请输入查找关键字： ",
                "sLengthMenu": "每页显示 _MENU_ 条记录",
                "sZeroRecords": "抱歉， 没有找到",
                "sInfo": "从 _START_ 到 _END_ /共 _TOTAL_ 条数据",
                "sInfoEmpty": "没有数据",
                "sInfoFiltered": "(从 _MAX_ 条数据中检索)",
                "oPaginate": {
                    "sFirst": "首页",
                    "sPrevious": "前一页",
                    "sNext": "后一页",
                    "sLast": "尾页"
                    }
                },
                "sDom": "lfrtip",
                "iDisplayLength": 15,
                //"sAjaxSource": "/customer/listJson",
                "ajax": {
                    url :  "/customer/listJson" ,
                    dataSrc: function (json) {
                        for(var i = 0; i<json.data.length;i++){
                            var cus = json.data[i];
                            customerList[cus.id] = cus;
                        }
                        console.log(customerList);
                        return json.data;
                    }
                },
                 "columns": [
                    {"data": "name"},
                    {"data": "type"},
                    {"data": "phone"},
                    {"data": "email"},
                    {"data": "address"},
                    {"data": "manager"},
                    {"render" : function(data, type,row) {
                        var id = '"' + row.id + '"';
                        //var row = JSON.stringify(row).replace(/\"/g,"'")
                        //console.log(id)
                        var html = ""//<a href='javascript:void(0);'  class='delete btn btn-default btn-xs'  ><i class='fa fa-times'></i> 查看</a>"
                        html += "<a onclick='setDefaultData("+id+")' type='button' class = 'btn btn-info btn-sm edit-btn' data-toggle='modal' data-target='#updateModal' style='font-size: 12px; padding: 2px 10px; margin:1px 5px'> 编辑</a>"
                        html += "<a href='javascript:void(0);' type='button'  onclick='setDelId("+id+")'   data-toggle='modal' data-target='#deleteModal' class = 'btn btn-info btn-sm edit-btn' style='font-size: 12px; padding: 2px 10px;'> 删除</a>"
                        return html;
                    }}
                 ],
                 'bStateSave': true,

            } );
        });

        $("body").on('click',"#add_customer", function () {
            //$("#add_customer_form").reset();
            var f = document.forms[0];        //获取表单DOM
            f.reset();
        });

        //新增客户
    function ajaxForm(form_id){
        var form= new FormData(document.getElementById(form_id));
        $.ajax({
            url:"customer/add",
            type:"post",
            data:form,
            dataType: 'json',
            processData:false,
            contentType:false,
            success:function(data){
                if(data.result == 1){
                    $("#myModal .btn-default").click()
                    console.log($("#myModal .btn-default"))
                    $("#dataTables-example").DataTable().ajax.reload();
                    toastr.success("客户新增成功");
                }
                else {
                    var body = '<div class="alert alert-warning"> <button type="button" class="close" data-dismiss="alert">&times;</button>'+data.result+ '</div>'

                    $('#'+form_id+' .modal-body').prepend(body)
                }

            },
            error:function(e){
                console.error("新增客户：没有取得数据");
            }
        })
    }

    function setDelId(id){
         del_id = id;
     }
    //删除客户
    function deleteThisRowPapser(){
        $.ajax({
            url:decodeURI("customer/del"),
            type:"post",
            data:JSON.stringify({"id":del_id}),
            dataType: 'json',
            processData:false,
            contentType:false,
            success:function(data){
                 if (data.result==1){
                     console.log("del success")
                     $("#deleteModal .btn-default").click()
                     $("#dataTables-example").DataTable().ajax.reload();

                     toastr.success("客户删除成功");
                 }
            },
            error:function(e){
                    alert("没有取得数据");
            }
        })
    }
    //编辑客户
    function updateThisRowPapser(form_id){
        var form= new FormData(document.getElementById(form_id));
        $.ajax({
            url:"customer/update/"+update_id,
            type:"post",
            data:form,
            dataType: 'json',
            processData:false,
            contentType:false,
            success:function(data){
                if(data.result == 1){
                    setTimeout($("#updateModal .btn-default").click(),1000);
                    console.log($("#updateModal .btn-default"));
                    toastr.success("编辑客户成功")
                    $("#dataTables-example").DataTable().ajax.reload(null, false);
                }
                else {
                    var body = '<div class="alert alert-warning"> <button type="button" class="close" data-dismiss="alert">&times;</button>'+data.result+ '</div>'

                    $('#'+form_id+' .modal-body').prepend(body)
                }
            },
            error:function(e){
                console.log("没有取得数据");
            }
        })

    }
    //编辑设置默认值
    function setDefaultData(id){
        var data = customerList[id];
        update_id=id;

        $("#update_customer_form #update_name").val(data.name);
        if(data.type=="个人"){
            $("#update_customer_form #type-0").prop("checked",true);
            $("#update_customer_form #type-1").removeAttr("checked");
        }
        else {
            $("#update_customer_form #type-1").prop("checked",true);
            $("#update_customer_form #type-0").removeAttr("checked");
        }
        $("#update_customer_form #update_phone").val(data.phone);
        $("#update_customer_form #update_email").val(data.email);
        $("#update_customer_form #update_address").val(data.address);

        $("#update_customer_form #update_manager option").filter(function(){return $(this).text()==data.manager;}).prop("selected",true);
    }

    function missButton(form_id){
        $("#"+form_id+" .btn-default").click();
    }

    //导入客户
    function importCustomer(){
        var form= new FormData(document.getElementById('import_form'));
        $.ajax({
            url:"customer/import",
            type:"post",
            data:form,
            dataType: 'json',
            processData:false,
            contentType:false,
            success:function(data){
                if(data.result == 1){
                    $("#importModal .btn-default").click();
                    $("#dataTables-example").DataTable().ajax.reload();
                    toastr.success("客户导入成功");
                }
                else if(data.result == "0"){
                    $("#importModal .btn-default").click();
                    toastr.error("客户经理不存在，导入失败");
                }
                else if(data.result == "2"){
                    $("#importModal .btn-default").click();
                    toastr.warning("客户已存在，不能重复导入");
                }
                var f = document.forms[1];        //获取表单DOM
                f.reset(); //清空表单

            },
            error:function(e){
                console.log("没有取得数据");
            }
        })
    }