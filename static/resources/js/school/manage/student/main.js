/**
 * Created by jie on 2016/10/21.
 */

var vm= new Vue({
    el: '#content',
    data: {
        multiple: false,
        graduate_flag: false, //毕业的学生视图开关
        nograde: false, //无年级学生开关
        grade_num: '',
        graduate_year: '',
        class_id: '',
        grade_list: HX_CACHE.get_grade_list(),
        class_list: HX_CACHE.get_class_list(),
        graduate_class_list: [],
        graduate_year_obj:{
            //2016: '2016届',
        },
        year_list : HX_CACHE.YEAR_LIST,
        kind_list: CONST_ARR.KIND_LIST,
        form: {
            full_name: '',
            sex: '男',
            code: '',
            grade_num: '',
            class_id: '',
            mobile: '',
            id_card: '',
            is_in: '1',
            kind: '正常'
        },
        update_class_form: {
            grade_list: HX_CACHE.get_grade_list(),
            class_list: HX_CACHE.get_class_list(),
            grade_num: '',
            class_id: ''
        }
    },
    computed: {
        graduate_year_obj: function () {
            var list = this.graduate_class_list;
            var res = {};
            for(var i=0; i<list.length; i++){
                var item = list[i];
                res[item.graduate_year] = item.graduate_year +  '届';
            }
            return res;
        }
    },
    methods: {
        switch_graduate_flag: function(flag){
            this.multiple = false;
            this.graduate_flag = flag;
            get_graduate_class_list();
            $("#class_id").val('')
            $("#graduate_year").val(''),
            $('#grade_num').val(''),
            $("#name_or_code").val(''),
            $('#kind').val('');
            vm.class_id= '';
            vm.graduate_year = '';
            vm.grade_num = '';
            reloadGrid();
        },
        /*跳转到班级申请页面*/
        class_application_page: function(){
            window.open("/page/application/main")
        },
        grade_id_chged: function () {
            this.class_id = '';
        },
        graduate_year_chged: function () {
            this.class_id = '';
        },
        class_id_chged: function () {
            if (this.class_id){
                this.grade_num = getclassById(this.class_id).grade_num;
            }
        },
        form_grade_id_chged: function () {
            this.form.class_id = '';
        },
        form_class_id_chged: function () {
            if (this.form.class_id){
                this.form.grade_num = getclassById(this.form.class_id).grade_num;
            }
        }
    }
});

$(document).ready(function(){
    var URL_graduate_year = getURLString('graduate_year');
    var URL_class_id = getURLString('class_id');
    if (URL_graduate_year){
        vm.graduate_flag = true;
        vm.graduate_year = URL_graduate_year;
        get_graduate_class_list();
    }
    if (URL_class_id){
        vm.class_id = URL_class_id;
    }

    //加载grid表格
    myjqGrid( $('#grid') ,{
        url: '/api/list/student',
        postData: {
            verbose : vm.graduate_flag ? '1': '0', //在此添加是否毕业的学生参数(0: 在读， 1：已毕业)
            graduate_year : URL_graduate_year ? URL_graduate_year: '',
            class_id : URL_class_id ? URL_class_id: ''
        },
        colNames:['id','account_id', '学生姓名','性别','学号','班级','帐号','在读','状态','最近使用时间','操作'],
        colModel:[
            {name:'id',index:'id', hidden:true},
            {name:'account_id',index:'account_id', hidden:true},
            {name:'full_name',index:'full_name', formatter: fmt_full_name, width:100, align:"left", sorttype:"string"},
            {name:'sex',index:'sex', width:50, align:"center", sorttype:"string"},
            {name:'code',index:'code', width:170, align:"center", sorttype:"string"},
            {name:'class_name',index:'class_name', width:80, align:"center", sorttype:"string"},
            {name:'username',index:'username', width:80, align:"center", sorttype:"string"},
            {name:'is_in',index:'is_in', formatter: fmt_is_in, width:40,  align:"center", sorttype:"string"},
            {name:'kind',index:'kind', width:60, align:"center", sorttype:"string"},
            {name:'last_login',index:'last_login', width:150, align:"center", sorttype:"string"},
            {name:'oper',index:'oper', formatter: fmt_oper, width:80, align:"center"}
        ],
        choosed: function (multiple) {
            vm.multiple = multiple;
        },
        multipleBtn: '#grid_multipleBtn',
        ispaged: true,
    },function(){
        vm.multiple = false;
    });
    function fmt_full_name(cellvalue, options, rowObject){
        var src=  rowObject.image_url? rowObject.image_url: '/static/resources/images/icon/photo-default.png';
        return '<img class="cell-photo" src="'+src+'">' + cellvalue;
    };
    function fmt_is_in(cellvalue, options, rowObject){
        return getYNname(cellvalue);
    };
    function fmt_oper(cellvalue, options, rowObject){
        var role_mask = $("#role_mask").val();
        var id= rowObject.id;
        var account_id = rowObject.account_id;
        var _html = '<span class="mytooltip">...<span class="mytooltiptext">';
        if (vm.graduate_flag){
            _html += '<li  onclick="view('+id+')">查看</li>';
        }else{
            if (role_mask != 8){
                _html += '<li  onclick="edit('+id+')">编辑</li>';
            }
        }
        _html += '<li  onclick="restpwd('+account_id+')">重置密码</li>';
        if (role_mask != 8) {
            _html += '<li  onclick="del(' + id + ')">删除</li></span></span>';
        }
        return  _html;
    };

    //
    $('#modal_add input[type="radio"][name="is_in"]').on('click',function(){
        var val = $(this).val(); //当前radio选项
        var kind = $('#modal_add select[name="kind"]').val();
        var index = vm.kind_list.indexOf(kind);
        if (val==1){ //在读
            if (index<0||index>1)
                vm.form.kind = CONST_ARR.KIND_LIST[0]
        }else if(val==0){ //不在读
            if (index<=1)
                vm.form.kind = CONST_ARR.KIND_LIST[2]
        }
    });
    $('#modal_add select[name="kind"]').on('change',function(){
        var kind = $(this).val();
        var index = vm.kind_list.indexOf(kind);
        if (index<=1)
            vm.form.is_in = '1'
        else{
            vm.form.is_in = '0'
        }
    });
});

/**刷新gird**/
function reloadGrid(){
    var data = {
        verbose : vm.graduate_flag ? '1': '0', //在此添加是否毕业的学生参数(0: 在读， 1：已毕业)
        class_id : $.trim($("#class_id").val()),
        graduate_year : $.trim($("#graduate_year").val()),
        grade_name : $.trim($('#grade_num').find("option:selected").attr('grade-name')),
        name_or_code : $.trim($("#name_or_code").val()),
        kind: $.trim($('#kind').val())
    };
    if ( $('#grade_num').val() == -1 ){ //无年级学生特殊处理
        data ['verbose'] = 2;
        data ['grade_name'] = '';
        data ['class_id'] = '';
        vm.nograde = true;
    }else{
        vm.nograde = false;
    };
    $("#grid").jqGrid('setGridParam', {
        url: '/api/list/student',
        datatype: "json",
        mtype: "POST",
        postData: data,
        //page: 1
    }).trigger("reloadGrid"); //重新载入
};

//获取毕业班级
function get_graduate_class_list(){
    if (vm.graduate_class_list.length <= 0){
        myajax({
            url:'/api/list/graduated_class',
        }, function (data) {
            if (data.c==0){
                vm.graduate_class_list = data.d;
            }
        })
    }
}

//新增
function add(id,undiet_flag){
    if(undiet_flag){
        $('#modal_add input').attr('disabled','disabled');
        $('#modal_add select').attr('disabled','disabled');
    }else{
        $('#modal_add input').removeAttr('disabled');
        $('#modal_add select').removeAttr('disabled');
    }
    layer.open({
        title: id?'资料变更':'新增学生' ,
        type: 1,
        area: ['880px', '480px'], //宽高
        content: $('#modal_add'),
        btn: undiet_flag?false:['确定','取消'],
        yes: function (index) {
            if (!mycheck({ element: '#modal_add'})) {
                return;
            }
            if ($('#modal_add select[name="grade_num"]').val()){
                if (!$('#modal_add select[name="class_id"]').val()){
                    layer.msg('请选择班级');
                    return false;
                }
            };
            if ($('#modal_add input[name="is_in"]:checked').val() == '0'){
                if (!$('#modal_add select[name="kind"]').val()){
                    layer.msg('不在读时，请选择类型');
                    return false;
                }
            }
            var data = Serializetojson($('#modal_add form').formSerialize());
            if (id){
                data['id'] = id;
            }
            myajax({
                url: id? '/api/update/student':'/api/add/student',
                data: {
                    "student_info": JSON.stringify(data)
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
        url: 'api/detail/student',
        data: {
            student_id: id
        }
    }, function (data) {
        if (data.c == 0){
            extend(vm.form, data.d[0]);
            var classObj = getclassById(vm.form.class_id);
            vm.form.grade_num = classObj.grade_num;
        }
    });
    //打开layer 复用添加学生layer
    add(id);
}

//查看
function view(id){
    //初始化layer内form表单信息
    myajax({
        url: 'api/detail/student',
        data: {
            student_id: id
        }
    }, function (data) {
        if (data.c == 0){
            extend(vm.form, data.d[0]);
            var classObj = getclassById(vm.form.class_id);
            vm.form.grade_num = classObj.grade_num;
        }
    });
    //打开layer 复用添加学生layer
    add(id,true);
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
                    url: '/api/delete/student',
                    data: {
                        student_id_list: JSON.stringify(ids)
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

/**导入**/
function importExcel(){
    $.btImport({
        templateURL: '/static/files/students_template.xlsx',
        url: '/api/import/student',
        fileDesc: '请下载EXCEL模板后填写并上传学生信息' +
                    '<br>注：新用户默认密码为学号后六位',
        success: function(){
            reloadGrid();
        },
        successInfo: '学生账号导入成功，您可以在学生管理中查看!'
    });
}

/**导出**/
function exportExcel(){
    var form_data = [
        { name: 'name_or_code', value: $('#name_or_code').val()},
        { name: 'kind', value: $('#kind').val()},
        { name: 'enrollment_year', value: ''},
        { name: 'class_id', value: $('#class_id').val()},
        { name: 'grade_name', value: $('#grade_name').val()},
        { name: 'verbose', value: vm.graduate_flag?1:0}
    ];
    if ( $('#grade_num').val() == -1 ){ //无年级学生特殊处理
        data ['verbose'] = 2;
        data ['grade_name'] = '';
        data ['class_id'] = '';
    };
    submit_with_parameters('/api/export/student', "POST", form_data);
}

/**取消学生班级**/
function clean_class(id){
    var ids;
    if (id){
        ids = [id];
    }else{
        if (!hascheckedrows(function (data) {ids = data;})){return;}
    }

    layer.confirm('是否清除学生班级？', {
        icon: 3,
        title: '提示',
        btn: ['确定', '取消'],
        btn1: function (index) {
            myajax({
                url: '/api/update/student_class',
                data: {
                    student_id_list: JSON.stringify(ids),
                }
            }, function (data) {
                //涉及到班级人数时，清理班级缓存
                HX_CACHE.refresh();
                reloadGrid();
                if (data.c == 0) {
                    layer.msg('取消成功');
                }
            });
            layer.close(index);
        },
        cancel: function(index){
            layer.close(index);
        }
    });
}

/**学生调班**/
function update_class(id){
    var ids;
    if (id){
        ids = [id];
    }else{
        if (!hascheckedrows(function (data) {ids = data;})){return;}
    }
    $('.left-menu').mCustomScrollbar();
    $('.right-class').mCustomScrollbar();
    //涉及到班级人数时，先清理班级缓存，再重新获取。
    HX_CACHE.refresh();
    vm.update_class_form.class_list = HX_CACHE.get_class_list();
    layer.open({
        title: '学生调班',
        type: 1,
        area: ['880px', '480px'], //宽高
        content: $('#modal_update_class'),
        btn:['确定','取消'],
        yes: function (index) {
            if (!vm.update_class_form.class_id){
                layer.msg('未选择班级')
                return;
            }
            myajax({
                url: '/api/update/student_class',
                data: {
                    student_id_list: JSON.stringify(ids),
                    class_id: vm.update_class_form.class_id,
                }
            },function(data){
                //涉及到班级人数时，清理班级缓存
                HX_CACHE.refresh();
                reloadGrid();
                if (data.c == 0){
                    layer.close(index);
                    layer.msg('调班成功');
                }
            });
        }
    });
}

/*学生调班-点击年级*/
function filter_class_list(element){
    var grade_num = $(element).attr('grade-id');
    vm.update_class_form.grade_num = grade_num;
}

/*学生调班-点击班级*/
function choose_class(element){
    var class_id = $(element).attr('class-id');
    vm.update_class_form.class_id = class_id;
}




