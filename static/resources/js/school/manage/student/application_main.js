/**
 * Created by jie on 2016/10/21.
 */

var vm= new Vue({
    el: '#content',
    data: {
        multiple: false,
        application_status: "", //申请状态(1, u"未处理")(2, u"已同意")(3, u"已拒绝")，空为全部
    },
    computed: {
    },
    methods: {
    }
});

$(document).ready(function(){
    // 点击侧面导菜单
    $('.left-view li').unbind().on('click',function(){
        // 清除原来的当前选中样式
        var li_dom_list = $("#left_menu").children();
        li_dom_list.find("el").remove();
        li_dom_list.find("a").removeClass("active");

        // 设置新的当前选中样式
        $('#'+this.id).prepend('<el class="li-active-tag"></el>');
        $('#'+this.id).children('a').addClass('active');

        switch (this.id){
            case "total": {
                vm.application_status = "";
                break;
            }
            case "not_process": {
                vm.application_status = 1;
                break;
            }
            case "approved": {
                vm.application_status = 2;
                break;
            }
            case "refused": {
                vm.application_status = 3;
                break;
            }
        }
        reloadGrid();
    });

    //加载grid表格
    myjqGrid( $('#grid') ,{
        url: '/api/list/student_class_application',
        postData: {
            status: vm.application_status
        },
        colNames:['id', '学生姓名','学号','申请理由','状态', '操作'],
        colModel:[
            {name:'id',index:'id', hidden:true},
            {name:'student_full_name',index:'student_full_name', formatter: fmt_full_name, width:100, align:"left", sorttype:"string"},
            {name:'student_code',index:'student_code', width:150, align:"center", sorttype:"string"},
            {name:'comments',index:'comments', width:200, align:"center", sorttype:"string"},
            {name:'status',index:'status', width:80, align:"center", formatter:fmt_status, sorttype:"string"},
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
    function fmt_status(cellvalue, options, rowObject){
       switch (cellvalue){
            case 1: {
                return "未处理";
            }
            case 2: {
                return "已同意";
            }
            case 3: {
                return "已拒绝";
            }
        }
    };
    function fmt_oper(cellvalue, options, rowObject){
        var role_mask = $("#role_mask").val();
        var id= rowObject.id;
        var status = rowObject.status;
        var _html = '<span class="mytooltip">...<span class="mytooltiptext">';
        if (status==1){
            _html += '<li  onclick="approve('+id+')">同意</li>';
            _html += '<li  onclick="refuse('+id+')">拒绝</li>';
        }else if (status==2 || status==3){
            _html += '<li  onclick="del('+id+')">删除</li>';
        }
        _html += '</span></span>';
        return  _html;
    };
});

/**刷新gird**/
function reloadGrid(){
    var data = {
        status :vm.application_status,
        student_name : $.trim($("#name_or_code").val()),
    };
    $("#grid").jqGrid('setGridParam', {
        url: '/api/list/student_class_application',
        datatype: "json",
        mtype: "POST",
        postData: data,
        page: 1
    }).trigger("reloadGrid"); //重新载入
}

function approve(id){
    update_application(id, 2)
}

function refuse(id){
    update_application(id, 3)
}

function update_application(id, status){
    var ids;
    if (id){
        ids = [id];
    }else{
        if (!hascheckedrows(function (data) {ids = data;})){return;}
    }
    title_msg = "是否同意加入班级？";
    if (status == 3){
        title_msg = "是否拒绝加入班级"
    }
    layer.confirm(title_msg, {
        icon: 3,
        title: '提示',
        btn: ['确定', '取消'],
        btn1: function (index) {
            myajax({
                url: '/api/update/student_class_application',
                data: {
                    id_list: JSON.stringify(ids),
                    status: status
                }
            }, function (data) {
                //涉及到班级人数时，清理班级缓存
                HX_CACHE.refresh();
                reloadGrid();
                if (data.c == 0) {
                    layer.msg('操作成功');
                }
            });
            layer.close(index);
        },
        cancel: function(index){
            layer.close(index);
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
                    url: '/api/delete/student_class_application',
                    data: {
                        id_list: JSON.stringify(ids)
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
