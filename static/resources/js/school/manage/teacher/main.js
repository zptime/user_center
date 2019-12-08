/**
 * Created by jie on 2016/10/21.
 */

var vm= new Vue({
    el: '#content',
    data: {
        multiple: false,
        leave_flag: false, //离职的教师视图开关
        title_list: [], //职务列表
        form: {
            full_name: '',
            sex: '男',
            school_code: '',
            title: '',
            mobile: '',
            id_card: '',
        }
    },
    computed: {

    },
    methods: {
        switch_leave_flag: function(flag){
            this.multiple = false;
            this.leave_flag = flag;
            reloadGrid();
        },
        title_list_filter: function(title) {
          return title.name != "班主任";
        }
    }
});

$(document).ready(function(){
    get_title_list();  //获取职务列表

    //加载grid表格
    myjqGrid( $('#grid') ,{
        //url: '/static/mock/student_list.json',
        url: '/api/list/teacher',
        colNames:['id','用户账户ID','姓名','性别','工号','职务','手机号','最近使用时间','操作'],
        colModel:[
            {name:'id',index:'id', hidden:true},
            {name:'account_id',index:'account_id', hidden:true},
            {name:'full_name',index:'full_name', formatter: fmt_full_name, width:100, align:"left", sorttype:"string"},
            {name:'sex',index:'sex', width:100, align:"center", sorttype:"string"},
            {name:'school_code',index:'school_code', width:150, align:"center", sorttype:"string"},
            {name:'title',index:'title', width:150, align:"center", sorttype:"string"},
            {name:'mobile',index:'mobile', width:100, align:"center", sorttype:"string"},
            {name:'last_login',index:'last_login', width:150, align:"center", sorttype:"string"},
            {name:'oper',index:'oper', formatter: fmt_oper, width:100, align:"center"}
        ],
        choosed: function (multiple) {
            vm.multiple = multiple;
        },
        multipleBtn: '#grid_multipleBtn',
        ispaged: true,
    },function(){});
    function fmt_full_name(cellvalue, options, rowObject){
        var src=  rowObject.image_url? rowObject.image_url: '/static/resources/images/icon/photo-default.png';
        return '<img class="cell-photo" src="'+src+'">' + cellvalue;
    };
    function fmt_oper(cellvalue, options, rowObject){
        var id= rowObject.id;
        var account_id = rowObject.account_id;
        var _html = '<span class="mytooltip">...<span class="mytooltiptext">';
        _html += '<li  onclick="edit('+id+')">编辑</li>';
        _html += '<li  onclick="restpwd('+account_id+')">重置密码</li>';
        if (vm.leave_flag){
             _html += '<li  onclick="leave('+id+')">返回学校</li>';
            _html += '<li  onclick="del('+id+')">删除</li>';
        }else{
             _html += '<li  onclick="leave('+id+')">离校</li>';
        }
        _html += '</span></span>';
        return  _html;
    };

});

//获取职务列表
function get_title_list(){
    myajax({
        //url: '/static/mock/title_list.json',
        url: '/api/list/title',
    }, function (data) {
        if (data.c == 0){
            vm.title_list = data.d;
        }
    })
}

/**刷新gird**/
function reloadGrid(){
    data = {
        verbose : vm.leave_flag ? '1': '0', //在此添加是否毕业的学生参数(0: 在读， 1：已毕业)
        title: $.trim($("#title").val()),
        name_or_code : $.trim($("#name_or_code").val()),
    };
    $("#grid").jqGrid('setGridParam', {
        url: '/api/list/teacher',
        datatype: "json",
        mtype: "POST",
        postData: data,
        //page: 1
    }).trigger("reloadGrid"); //重新载入
};

//新增
function add(id){
    layer.open({
        title: id?'资料变更':'新增教师' ,
        type: 1,
        area: ['880px', '480px'], //宽高
        content: $('#modal_add'),
        btn:['确定','取消'],
        yes: function (index) {
            if (!mycheck({ element: '#modal_add'})) {
                return;
            }
            var data = Serializetojson($('#modal_add form').formSerialize());
            if (id){
                data['id'] = id;
            }
            myajax({
                url: id? '/api/update/teacher':'/api/add/teacher',
                data: {
                    "teacher_info": JSON.stringify(data)
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
}

//修改
function edit(id){
    //初始化layer内form表单信息
    myajax({
        url: 'api/detail/teacher',
        data: {
            teacher_id: id
        }
    }, function (data) {
        if (data.c == 0){
            extend(vm.form, data.d[0]);
        }
    });
    //打开layer 复用添加教师layer
    add(id);
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
                    url: '/api/delete/teacher',
                    data: {
                        teacher_id_list: JSON.stringify(ids)
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

//离校 、 返回学校
function leave(id){
    var ids;
    var is_leave = 1;
    if (id){
        ids = [id];
    }else{
        if (!hascheckedrows(function (data) {ids = data;})){return;}
    }
    var msg = "";
    if (vm.leave_flag){
        is_leave = 0;
        msg = '确认执行返校操作吗?';
    } else {
        msg = '确认执行离校操作吗?';
    }
    layer.confirm(msg, {
           icon: 3,
           title: '提示',
           btn:['确定','取消'],
           btn1: function (index) {
                myajax({
                    aysnc: false,
                    url: '/api/leave/teacher',
                    data: {
                        teacher_id_list: JSON.stringify(ids),
                        is_leave: is_leave
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

//重置密码
function restpwd(id){
    var ids;
    if (id){
        ids = [id];
    }else{
        ids = [];
        debugger;
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

/**导入**/
function importExcel(){
    $.btImport({
        templateURL: '/static/files/teacher_template.xlsx',
        url: '/api/import/teacher',
        fileDesc: '请下载EXCEL模板后填写并上传教师信息' +
                    '<br>注：新用户默认密码为手机号后六位',
        success: function(){
            reloadGrid();
        },
        successInfo: '教师账号导入成功，您可以在教师管理中查看!'
    });
}

/**下载Excel模板**/
function downloadExcelTemplate(){
    var element_iframe = document.createElement("iframe");
    var url= '../../../static/files/teacher_template.xlsx';
    element_iframe.src = url;
    element_iframe.style.display = "none";
    document.body.appendChild(element_iframe);
}

/**导出**/
function exportExcel(){
    var form_data = [
        { name: 'name_or_code', value: $('#name_or_code').val()},
        { name: 'verbose', value: vm.leave_flag?1:0}
    ]
    submit_with_parameters('/api/export/teacher', "POST", form_data);
}

/**查看详情**/
function view(id){
    url_go(URLs().Pteacherview+'?id='+id);
}



