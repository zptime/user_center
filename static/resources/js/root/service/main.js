/**
 * Created by Xi Chen on 3/30/2017.
 */

var vm= new Vue({
    el: '#content',
    data: {
        multiple: false,
        frozen_flag: false, //毕业的学生视图开关
        grade_num: '',
        class_id: '',
        grade_list: HX_CACHE.GRADE_LIST,
        class_list: HX_CACHE.CLASS_LIST,
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

$(document).ready(function () {

    myjqGrid( $('#grid') ,{
        url: '/api/admin/list/service',
        ispaged: true,
        colNames: ['id','服务代码', '服务名称','内网地址', '外网地址'],
        colModel: [
            {name: 'id',hidden:true},
            {name: 'code', width: 100, align: "center", sortable: false},
            {name: 'name', width: 100, align: "center", sortable: false},
            {name: 'intranet_url', width: 100, align: "center", sortable: false},
            {name: 'internet_url', width: 100, align: "center", sortable: false},
            //{name: 'oper',width:100,formatter: fmt_oper, align:"center",sortable:false}
        ],
        multiselect: false,
    },function(){});

    function fmt_oper(cellvalue, options, rowObject){
        var id= rowObject.id;
        var account_id = rowObject.account_id;
        var _html = '<span class="mytooltip">...<span class="mytooltiptext">';
        _html += '<li  onclick="edit('+id+')">编辑</li>';
        if (vm.frozen_flag){
            _html += '<li  onclick="freeze('+id+')">解除冻结</li></span></span>';
        }else{
            _html += '<li  onclick="freeze('+id+')">冻结</li></span></span>';
        }
        return  _html;
    }

});

function reloadGrid(){
    var data= {
        name_or_code: $.trim($('#serviceCodeOrNameInput').val())
    };
    $("#grid").jqGrid('setGridParam', {
        url: '/api/admin/list/service',
        dataType: "json",
        mType: "POST",
        postData:data,
        page: 1
    }).trigger("reloadGrid");
}

function add(){
    layer.open({
        type: 1,
        title: '添加科目',
        area: ['550px', '330px'],
        content : $('#addSub'),
        btn:['确定','取消'],
        btn1: function(index){
            var subNam= $('#subNameAdd').val();
            var data={
                subject_name:subNam
            };
            myajax({
                aysnc: false,
                url: '/api/admin_add/subject',
                data:data
            },function(data){
                reloadGrid();
                layer.msg(data.m);
            });
        },
        cancel: function(index){
            layer.close(index);
        }
    });
}


function edit(id){
    var rowObject = $("#grid").getLocalRow(id);
    if(!rowObject) {
        rowObject = $("#grid").getRowData(id);
    }
    if (!rowObject){
        rowObject = $("#grid").getGridRowById(id);
    }
    $("#subName").val(rowObject.name);
    layer.open({
        type: 1,
        title: '编辑学科',
        area: ['550px', '330px'],
        content : $('#editSub'),
        btn:['确定','取消'],
        btn1: function(index){
            var data = {
                subject_id: id,
                subject_name: $("#subName").val()
            };
            myajax({
                aysnc: false,
                url: '/api/admin_edit/subject',
                data:  data
            },function(data){
                if(data.c == 0){
                    reloadGrid();
                    layer.close(index);
                    layer.msg('操作成功');
                }
            })
        },
        cancel: function(index){
            layer.close(index);
        }
    });
}

/**导入**/
function importExcel(){
    $.btImport({
        templateURL: '/static/files/subject_template.xlsx',
        url: '/api/admin_import/subject',
        fileDesc: '请下载EXCEL模板后填写并上传科目信息',
        success: function(){
            reloadGrid();
        },
        successInfo: '科目导入成功，您可以在科目管理中查看!'
    });
}

/**导出**/
function exportExcel(){
    var form_data = [
        { name: 'is_active', value: 1}
    ];
    submit_with_parameters('/api/admin_export/subject', "POST", form_data);
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
                    url: '/api/admin_delete/subject',
                    data: {
                        subject_id_list: JSON.stringify(ids)
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
}

//冻结 、 解除冻结
function freeze(id){
    var ids;
    var url = "/api/admin_freeze/subject";
    if (id){
        ids = [id];
    }else{
        if (!hascheckedrows(function (data) {ids = data;})){return;}
    }
    var msg = "";
    if (vm.frozen_flag){
        msg = '确认执行解除冻结操作吗?';
        url = '/api/admin_unfreeze/subject';
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
                    url: url,
                    data: {
                        subject_id_list: JSON.stringify(ids),
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
