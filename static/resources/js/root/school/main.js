var vm= new Vue({
    el: '#content',
    data: {
        multiple: false,
        service_list: [],
    },
    computed: {

    },
    methods: {

    }
});

$(document).ready(function () {

    myjqGrid( $('#grid') ,{
        url: '/api/admin/list/school',
        ispaged: true,
        colNames: ['id','代码','名称',  '管理员', '操作'],
        colModel: [
            {name: 'id',hidden:true},
            {name: 'code', width: 50, align: "center", sortable: false},
            {name: 'name_full', width: 100, align: "center", sortable: false},
            //{name: 'name_simple', width: 100, align: "center", sortable: false},
            {name: 'managers', width: 200, align: "center", sortable: false},
            {name: 'oper',width:100,formatter: fmt_oper, align:"center",sortable:false}
        ],
        multiselect: false,
        //choosed: function (multiple) {
        //    vm.multiple = multiple;
        //},
        //multipleBtn: '#grid_multipleBtn'
    },function(){});

    function fmt_oper(cellvalue, options, rowObject){
        var id = rowObject.id;
        var managers = rowObject.managers;
        var _html = '<span class="mytooltip">...<span class="mytooltiptext">';
        _html += '<li  onclick="edit_service('+id+')">编辑服务</li>';

        _html += '<li  onclick="del('+id+')">删除</li>';
        if (managers.length == 0){
            _html += '<li  onclick="add_manager('+id+')">添加管理员</li>';
        }
        _html += '</span></span>';
        return  _html;
    }

    $("#allSelectService").change(function() {
        debugger;
        if ($("#allSelectService").is(':checked')) {
            for(var i=0; i<vm.service_list.length; i++){
                vm.service_list[i].open = true;
            }
        } else {
            for(var i=0; i<vm.service_list.length; i++){
                vm.service_list[i].open = false;
            }
        }
    });

});

function reloadGrid(){
    var data= {
        name_or_code: $.trim($('#name_or_code').val())
    };
    $("#grid").jqGrid('setGridParam', {
        url: '/api/admin/list/school',
        dataType: "json",
        mType: "POST",
        postData:data,
        page: 1
    }).trigger("reloadGrid");
}

function add(){
    layer.open({
        type: 1,
        title: '添加学校',
        area: ['880px', '480px'], //宽高
        content : $('#addSchool'),
        btn:['确定','取消'],
        btn1: function(index){
            var data={
                school_code: $('#schoolAddCode').val(),
                school_name: $('#schoolAddFullName').val(),
                primary_years: $('#selPrimaryYears').val(),
                junior_years: $('#selJuniorYears').val(),
                senior_years: $('#selSeniorYears').val(),
            };
            myajax({
                aysnc: false,
                url: '/api/admin/add/school',
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


function edit_service(id){
    $("#allSelectService").removeAttr("checked");
    var rowObject = $("#grid").getLocalRow(id);
    if(!rowObject) {
        rowObject = $("#grid").getRowData(id);
    }
    if (!rowObject){
        rowObject = $("#grid").getGridRowById(id);
    }
    $("#subName").val(rowObject.name);
    myajax({
        aysnc: false,
        url: '/api/admin/list/service',
        data:  {school_id: rowObject.id}
    },function(data){
        if(data.c == 0){
            vm.service_list = data.d
            console.info("ajax: " + vm.service_list.length);
            layer.open({
                type: 1,
                title: '编辑服务 - ' + rowObject.name_full,
                area: ['880px', '480px'], //宽高
                content : $('#editService'),
                btn:['确定','取消'],
                btn1: function(index){
                    var service_id_list = [];
                    for(var i=0; i<vm.service_list.length; i++){
                        if (vm.service_list[i].open){
                            service_id_list.push(vm.service_list[i].id)
                        }

                    }
                    var data = {
                        school_id: rowObject.id,
                        service_id_list: JSON.stringify(service_id_list)
                    };
                    myajax({
                        aysnc: false,
                        url: '/api/admin/update/school_service',
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
    });

}


//删除
function del(id){
    layer.confirm('确认删除选中记录吗?', {
           icon: 3,
           title: '提示',
           btn:['确定','取消'],
           btn1: function (index) {
                myajax({
                    aysnc: false,
                    url: '/api/admin/delete/school',
                    data: {
                        school_id: id
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


//添加管理员
function add_manager(id){
    layer.open({
        type: 1,
        title: '添加管理员',
        area: ['880px', '480px'], //宽高
        content : $('#addManager'),
        btn:['确定','取消'],
        btn1: function(index){
            var data={
                school_id: id,
                username: $('#managerUsername').val(),
                full_name: $('#managerName').val(),
                password: $('#managerPassword').val()
            };
            myajax({
                aysnc: false,
                url: '/api/admin/add/manager',
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
