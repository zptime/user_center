/**
 * Created by jie on 2016/10/21.
 */

var vm= new Vue({
    el: '#content',
    data: {
        multiple: false,
        frozen_flag: false, //冻结的家长视图开关
        grade_num: '',
        class_id: '',
        grade_list: HX_CACHE.GRADE_LIST,
        class_list: HX_CACHE.CLASS_LIST,
        form: {
            full_name: '',
            sex: '男',
            school_code: '',
            title: '',
            mobile: '',
            id_card: '',
            children: [],
        }
    },
    computed: {

    },
    methods: {
        switch_frozen_flag: function(flag){
            this.multiple = false;
            this.frozen_flag = flag;
            reloadGrid();
        },
        grade_id_chged: function () {
            this.class_id = '';
        },
        class_id_chged: function () {
            if (this.class_id){
                this.grade_num = getclassById(this.class_id).grade_num;
            }
        },
        add_child: function () {
            this.form.children.push(
                {
                    student_id: '',
                    student_full_name: '',
                    student_code: '',
                    relation: '',
                    comments: ''
                }
            );
            setTimeout(function(){
                var index = vm.form.children.length - 1;
                var element = $('#student_id_'+index);
                bindAutocomplete(element);
            },100);
        },
        remove_child: function(index){
            if (this.form.children.length <= 1){
                layer.msg('关联学生数量不能少于1个');
                return;
            }else {
                this.form.children.splice(index, 1);
            }
        },
    }
});

$(document).ready(function(){
    //加载grid表格
    myjqGrid( $('#grid') ,{
        url: '/api/list/parent',
        colNames:['id','账号','姓名','性别','children','关联学生','学生学籍号','学生班级','手机','操作'],
        colModel:[
            {name:'id',index:'id', hidden:true},
            {name:'account_id',index:'account_id', hidden:true},
            {name:'full_name',index:'full_name', formatter: fmt_full_name, width:120, align:"left", sorttype:"string"},
            {name:'sex',index:'sex', width:60, align:"center", sorttype:"string"},
            {name:'children',index:'children', hidden:true},
            {name:'children_name',index:'children_name', formatter: fmt_children_name, width:100, align:"center", sorttype:"string"},
            {name:'children_code',index:'children_code', formatter: fmt_children_code, width:130, align:"center", sorttype:"string"},
            {name:'children_class_name',index:'children_class_name', formatter: fmt_children_class_name, width:100, align:"center", sorttype:"string"},
            {name:'mobile',index:'mobile', width:100, align:"center", sorttype:"string"},
            {name:'oper',index:'oper', formatter: fmt_oper, width:100, align:"center"}
        ],
        choosed: function (multiple) {
            vm.multiple = multiple;
        },
        multipleBtn: '#grid_multipleBtn',
        ispaged: true
    },function(){});
    function fmt_full_name(cellvalue, options, rowObject){
        var src=  rowObject.image_url? rowObject.image_url: '/static/resources/images/icon/photo-default.png';
        return '<img class="cell-photo" src="'+src+'">' + cellvalue;
    };
    function fmt_children_name(cellvalue, options, rowObject){
        var child_list  = rowObject.children;
        var res = [];
        for (var i in child_list){
            if (child_list[i].student_full_name){
                res.push(child_list[i].student_full_name);
            }
        }
        return res.join("<br>");
    };
        function fmt_children_code(cellvalue, options, rowObject){
        var child_list  = rowObject.children;
        var res = [];
        for (var i in child_list){
            if (child_list[i].student_code){
                res.push(child_list[i].student_code);
            }
        }
        return res.join("<br>");
    };
        function fmt_children_class_name(cellvalue, options, rowObject){
        var child_list  = rowObject.children;
        var res = [];
        for (var i in child_list){
            if (child_list[i].student_class_name){
                res.push(child_list[i].student_class_name);
            }
        }
        return res.join("<br>");
    };
    function fmt_oper(cellvalue, options, rowObject){
        var id= rowObject.id;
        var account_id = rowObject.account_id;
        var _html = '<span class="mytooltip">...<span class="mytooltiptext">';
        _html += '<li  onclick="edit('+id+')">编辑</li>';
        _html += '<li  onclick="restpwd('+account_id+')">重置密码</li>';
        if (vm.frozen_flag){
             _html += '<li  onclick="freeze('+id+')">解除冻结</li>';
            _html += '<li  onclick="del('+id+')">删除</li>';
        }else{
             _html += '<li  onclick="freeze('+id+')">冻结</li>';
        }
        _html += '</span></span>';
        return  _html;
    };

});

/**刷新gird**/
function reloadGrid(){
    var data = {
        is_active : vm.frozen_flag ? '0': '1', //(0: 未冻结， 1：已冻结)
        full_name: $.trim($("#full_name").val()),
        class_id : $.trim($("#class_id").val()),
        grade_name : $.trim($('#grade_num').find("option:selected").attr('grade-name')),
    };
    $("#grid").jqGrid('setGridParam', {
        //url: URLs().Alistparent,
        url: '/api/list/parent',
        datatype: "json",
        mtype: "POST",
        postData: data,
        //page: 1
    }).trigger("reloadGrid"); //重新载入
};

//新增
function add(id){
    disable_scrolling();
    layer.open({
        title: id?'资料变更':'新增家长' ,
        type: 1,
        area: ['880px', '480px'], //宽高
        content: $('#modal_add'),
        btn:['确定','取消'],
        end: restore_scrolling,
        yes: function (index) {
            if (!mycheck({ element: '#modal_add'})) {
                return;
            }
            if (vm.form.children.length <= 0){
                layer.msg('关联学生不能为空');
                vm.add_child();
                return;
            };
            //校验关联学生内容是否被修改
            for (var i=0; i<vm.form.children.length; i++){
                var child = vm.form.children[i];
                var vm_data = child.student_full_name + ' -- '+  child.student_code;
                var dom_data = child.student_nameANDcode;
                if ( vm_data!= dom_data ){
                    layer.msg('无学生[ '+dom_data+' ]信息,重新输入!');
                    $('#student_id_'+i).focus();
                    return;
                }
            }
            var data = {
                    full_name: $.trim(vm.form.full_name),
                    sex: $.trim(vm.form.sex),
                    mobile: $.trim(vm.form.mobile),
                    id_card: $.trim(vm.form.id_card),
                    children: vm.form.children
                };
            if (id){
                data['id'] = id;
            }
            myajax({
                url: id? '/api/update/parent':'/api/add/parent',
                data: {
                    "parent_info": JSON.stringify(data)
                }
            },function(data){
                reloadGrid();
                if (data.c == 0){
                    layer.close(index);
                    layer.msg(id?'编辑成功':'添加成功');
                }
            });
        }
    });
    $('#modal_add').mCustomScrollbar();
    //$('#modal_add input[name="student_id"]').unbind('focus').on('focus', function () {
    //    //禁用滚轮
    //    $(window.document.body).on('mousewheel', function (e) {
    //        e.preventDefault();
    //    });
    //}).on('bulr', function () {
    //    $('#modal_add input[name="student_id"]').unbind('focus');
    //});
}

//修改
function edit(id){
    //初始化layer内form表单信息
    myajax({
        url: 'api/detail/parent',
        data: {
            parent_id: id
        }
    }, function (data) {
        if (data.c == 0){
            for (var i=0; i<data.d[0].children.length; i++){
                var child = data.d[0].children[i];
                child['student_nameANDcode'] = child['student_full_name'] + ' -- '+ child['student_code'];
            }
            extend(vm.form, data.d[0]);
            setTimeout(function(){ //绑定autocompelte
                for (var i=0; i<vm.form.children.length; i++){
                    var element = $('#student_id_'+i);
                    bindAutocomplete(element);
                }
            },100);
        }
    });
    //打开layer 复用添加教师layer
    add(id);
}

//autocomplete
function bindAutocomplete(el){
    $(el).autocomplete({
        source: function (request, response ) {
            $.ajax({
                type:"post",
                url: "/api/list/student",
                dataType: "json",
                data:{
                    rows:8,
                    page:1,
                    name_or_code: request.term
                },
                success: function( data ) {
                    response( $.map( data.d.items, function( item ) {
                        return { //lable为下拉列表显示数据源。value为选中放入到文本框的值，这种方式可以自定义显示
                            id: item.id,
                            account_id: item.account_id,
                            full_name: item.full_name,
                            code: item.code,
                            label: item.full_name + ' -- ' + item.code,
                            value: item.full_name + ' -- ' + item.code
                        }
                    }));
                }
            });
        },
        minLength: 1,
        select: function( event, ui ) {
            $(event.target).attr('student-id', ui.item.id);
            var index = $(event.target).attr('index');
            vm.form.children[index].student_id =  ui.item.id;
            vm.form.children[index].student_full_name = ui.item.full_name;
            vm.form.children[index].student_code = ui.item.code;
        }
    });
}


//删除
function del(id){
    var ids;
    if (id){
        ids = [id];
    }else{
        if (!hascheckedrows(function (data) {ids = data;})){return;}
    }
    layer.confirm('确认删除选中记录吗?', {
           icon: 3,
           title: '提示',
           btn:['确定','取消'],
           btn1: function (index) {
                myajax({
                    aysnc: false,
                    url: '/api/delete/parent',
                    data: {
                        parent_id_list: JSON.stringify(ids)
                    }
                },function(data){
                    reloadGrid();
                    if(data.c == 0){
                        layer.msg('删除成功');
                    }
                });
                layer.close(index);
           },
           cancel: function(index){
               layer.close(index);
           }
    });
};

//导入
function importExcel(){
    $.btImport({
        templateURL: '/static/files/parent_template.xlsx',
        url: '/api/import/parent',
        fileDesc: '请下载EXCEL模板后填写并上传家长信息' +
                    '<br>注：新用户默认密码为手机号后六位',
        success: function(){
            reloadGrid();
        },
        successInfo: '家长账号导入成功，您可以在家长管理中查看!'
    });
}

/**下载Excel模板**/
function downloadExcelTemplate(){
    var element_iframe = document.createElement("iframe");
    var url= '/static/files/parent_template.xlsx';
    element_iframe.src = url;
    element_iframe.style.display = "none";
    document.body.appendChild(element_iframe);
}

/**导出**/
function exportExcel(){
    var form_data = [
        { name: 'student_name', value: $('#student_name').val()},
        { name: 'full_name', value: $('#full_name').val()},
        { name: 'is_active', value: vm.frozen_flag? 0: 1 },
    ];
    submit_with_parameters('/api/export/parent', "POST", form_data);
}

/**查看详情**/
function view(id){
    url_go(URLs().Pparentview+'?id='+id);
}

//重置密码
function restpwd(id){
    var ids;
    if (id){
        ids = [id];
    }else{
        ids = [];
        var rowids;
        if (!hascheckedrows(function (data) {rowids = data;})){return;}
        for (i in rowids){
            var rowData =$('#grid').jqGrid('getRowData', rowids[i]);
            ids.push(rowData.account_id)
        }


    }
    layer.confirm('密码将会重置为默认密码“123456”！<br>您确定要重置密码吗？', {
           icon: 3,
           title: '提示',
           btn:['确定','取消'],
           btn1: function (index) {
                myajax({
                    aysnc: false,
                    url: '/api/batch_reset/password',
                    data: {
                        account_id_list: JSON.stringify(ids),
                        new_password: "123456"
                    }
                },function(data){
                    if(data.c == 0){
                        layer.msg('重置成功');
                    }
                });
                layer.close(index);
           },
           cancel: function(index){
               layer.close(index);
           }
    });
};


//冻结 、 解除冻结
function freeze(id){
    debugger;
    var ids;
    var is_active = 0;
    if (id){
        ids = [id];
    }else{
        if (!hascheckedrows(function (data) {ids = data;})){return;}
    }
    var msg = "";
    if (vm.frozen_flag){
        is_active = 1;
        msg = '确认执行解除冻结操作吗?';
    } else {
        msg = '确认执行冻结操作吗?';
    }
    layer.confirm(msg, {
           icon: 3,
           title: '提示',
           btn:['确定','取消'],
           btn1: function (index) {
                myajax({
                    aysnc: false,
                    url: '/api/active/parent',
                    data: {
                        parent_id_list: JSON.stringify(ids),
                        is_active: is_active
                    }
                },function(data){
                    reloadGrid();
                    if(data.c == 0){
                        layer.msg('操作成功');
                    }
                });
                layer.close(index);
           },
           cancel: function(index){
               layer.close(index);
           }
    });
};

//禁止滚动条
function disable_scrolling(){
    $('html, body').css({
        overflow: 'hidden',
        height: '100%'
    });
}

function restore_scrolling() {
    $('html, body').css({
        overflow: 'auto',
        height: 'auto'
    });
}