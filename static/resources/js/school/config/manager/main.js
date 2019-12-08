/**
 * Created by jie on 2017/3/27.
 */

/**
 * Created by Xi Chen on 3/27/2017.
 */

var vm= new Vue({
    el: '#content',
    data: {
        multiple: false,
        urlString:'',
        teacherName:'',
        teacherId:''
    },
    computed: {

    },
    methods: {

    }
});

$(document).ready(function(){

    //加载grid表格
    myjqGrid( $('#grid') ,{
        url: '/api/list/admin_user',
        colNames:['id','管理员姓名','管理应用', '管理内容', '联系电话','最近登录','操作'],
        colModel: [
            {name: 'user_role_id',hidden:true},
            {name: 'user_name', width: 100, align: "center", sortable: false},
            {name: 'service_name', width: 100, align: "center", sortable: false},
            {name: 'role_name', width: 150, align: "center", sortable: false},
            {name: 'mobile', width: 100, align: "center", sortable: false},
            {name: 'last_login', width: 100, align: "center", sortable: false},
            {name: 'oper', width:100, formatter: fmt_oper, align:"center",sortable:false}
        ],
        totalTitle: '',
        selectedTitle: '',
        multiselect: false
    },function(){});
    function fmt_oper(cellvalue, options, rowObject){
        var id= rowObject.user_role_id;
        return  '<a  onclick="del('+id+')">删除</a>'
    }
});

/**添加管理员第一步**/
function addDetail(){
    var init_teacher_list = function(){/**获取教师列表**/
        myajax({
            url:'/api/list/teacher',
            data: {
                name_or_code : $.trim($("#name_or_code").val())
            },
            async:false,
            success:function(data){
                var temp=data.d;
                var html='';
                for(var i=0;i<temp.length;i++) {
                    html +=
                        '<div class="teacherDiv" teacherId="'+temp[i].id+'" teacherName="'+temp[i].full_name+'" pUrl="'+(temp[i].image_url?temp[i].image_url:'/static/resources/images/icon/photo-default.png')+'" id="newAdmin'+i+'">' +
                            '<img id="profile'+i+'" class="photo" alt="text" src="'+(temp[i].image_url?temp[i].image_url:'/static/resources/images/icon/photo-default.png')+'">' +
                            '<span class="name">'+temp[i].full_name+'</span>' +
                        '</div>';
                }
                $('#teacher-box').html(html);
            }
        });
        $('.teacherDiv').on('click', function() {//选择管理员
            //所有的div去掉blue,添加
            $('.teacherDiv').removeClass('blue');
            //当前div选中
            $(this).addClass('blue');
            $('#showPic')[0].src = $(this).attr('pUrl');
            vm.teacherName = $(this).attr('teacherName');
            vm.teacherId = $(this).attr('teacherId');
        });
    };
    layer.open({
        type: 1,
        area: ['880px', '480px'], //宽高
        title:'添加管理员',
        content: '<div id="modal-setManager" style="height:300px">'+
                '<div id="ulForAdd">'+
                    '<div style="text-align: right;">'+
                        '<input id="name_or_code" placeholder="请输入姓名">'+
                        '<button id="init-teacher-btn" type="button" class="hx-margin20-l">查询</button>'+
                    '</div>'+
                    '<div id="teacher-box"></div>'+
                '</div>'+
            '</div>',
        btn:['下一步','取消'],
        yes: function (index) {
            if ( $('#modal-setManager .teacherDiv.blue').length > 0 ){
                layer.close(index);
                addAdmin();
            }else{
                layer.msg('未选择管理员');
                return;
            }
        },
        cancel: function(index){
           layer.close(index);
        }
    });
    init_teacher_list();
    $('#init-teacher-btn').on('click',function(){
        init_teacher_list();
    });
}

/**添加管理员第二步**/
function addAdmin(){
     $('#adminDetail').children().remove();
     var role_id_list=[];
     myajax({
                aysnc: false,
                url: '/api/list/admin_role',
                data: {
                    teacher_id:vm.teacherId
                }
            },function(data){
                var temp=data.d;
                var tempServiceName='';
                var statusMe='';
                for(var i=0;i<temp.length;i++){
                    if(i==0){
                        $('#adminDetail').append('<li class="liAlone">'+temp[i].service_name+'</li>'+'<li><ul id="'+i+'ul"><li class="adminLi"><input roleId="'+temp[i].role_id+'" id="'+i+'li" type="checkbox"/><a class="adminAb">'+temp[i].role_name+'</a></li></ul></li>');
                        if(temp[i].is_already==1){
                            $('#'+i+'li').prop('checked', true).next().removeClass('adminAb').addClass('adminA');
                            //$('#'+i+i+'Label').append('<img class="img" src="static/resources/images/icon/checkbox-upper-checked.png">')
                        }
                        tempServiceName=temp[i].service_name;
                        statusMe=i+'ul';
                    }else {
                        if (tempServiceName == temp[i].service_name){
                            $('#'+statusMe).append('<li class="adminLi"><input  roleId="'+temp[i].role_id+'" id="'+i+'li" type="checkbox"><a class="adminAb">'+temp[i].role_name+'</a></li>');
                            if(temp[i].is_already==1){
                                $('#'+i+'li').prop('checked',true).next().removeClass('adminAb').addClass('adminA');
                                //$('#'+i+i+'Label').append('<img class="img" src="static/resources/images/icon/checkbox-upper-checked.png">')
                            }
                        }else{
                            $('#adminDetail').append('<li class="liAlone">'+temp[i].service_name+'</li>'+'<li><ul id="'+i+'ul"><li class="adminLi"><input roleId="'+temp[i].role_id+'" id="'+i+'li" type="checkbox"><a class="adminAb">'+temp[i].role_name+'</a></li></ul></li>');
                            tempServiceName=temp[i].service_name;
                            statusMe=i+'ul';
                            if(temp[i].is_already==1){
                                $('#'+i+'li').prop('checked', true).next().removeClass('adminAb').addClass('adminA');
                               //$('#'+i+i+'Label').append('<img class="img" src="static/resources/images/icon/checkbox-upper-checked.png">')
                            }
                        }
                    }
                }
            });
    layer.open({
        type: 1,
        area: ['705px', '440px'], //宽高
        title:'授予权限',
        content: $('#addAdmin'),
        btn:['确定','取消'],
        btn1: function (index) {
            var roleId="";
            $('#adminDetail').find('input').each(function(){
                    if($(this).is(':checked')){
                        role_id_list.push($(this).attr('roleId'));
                    }
            });
            roleId=JSON.stringify(role_id_list);
            layer.close(index);
            myajax({
                aysnc: false,
                url: '/api/update/admin_user',
                data: {
                    teacher_id:vm.teacherId,
                    role_id_list:roleId
                }
            },function(data){
                reloadGrid();
                if(data.c == 0){
                    layer.msg('添加管理员成功');
                }
            })
        },
        cancel: function(index, layero){
            layer.close(index);
        }
    });
}

/**刷新gird**/
function reloadGrid(){
    var data= {
        user_name: $.trim($('#name_filter').val())
    };
    $("#grid").setGridParam({datatype:'json', page:1}).jqGrid('setGridParam', {
        url: '/api/list/admin_user',
        dataType: "json",
        mType: "POST",
        postData:data,
        page: 1
    }).trigger("reloadGrid"); //重新载入
}





function del(id){
    var ids = "";
    if (id){  // 单条删除
        ids = [id];
    }else if($("#grid").getGridAttr('istypeAll') == true) { // 按照查询条件删除

    }else{ // 选择删除
        if (hascheckedrows(function (data) {
                ids = data;
            })){
        }else{
            return;
        }
    }
    layer.confirm('确认删除选中记录吗?', {
        //icon: 3,
        title: '提示',
        btn:['确定','取消'],
        btn1: function (index) {
            layer.close(index);
            myajax({
                aysnc: false,
                url: '/api/delete/admin_user',
                data: {
                    user_role_id_list: JSON.stringify(ids)
                }
            },function(data){
                reloadGrid();
                if(data.c == 0){
                    layer.msg('删除成功');
                }
            })
        },
        cancel: function(index){
           layer.close(index);
        }
    });
}

//exportExcel
EXPORT_MODE={
    all: 1,
    id_list: 2,
    parameters: 3
};

function exportExcel(mode) {
    if ($("#grid").getGridAttr('istypeAll') == true){
        mode = EXPORT_MODE.parameters
    }
    if (mode == EXPORT_MODE.all) {

    } else if (mode == EXPORT_MODE.id_list) {
        var has_check = hascheckedrows(function (data) {
            ids = data;
            ids = JSON.stringify(ids)
        });
        if (!has_check) {
            return;
        }
    }else if (mode == EXPORT_MODE.parameters) {
    }
    var form_data = [
    ];
    submit_with_parameters('/api/export/admin_user', "POST", form_data);
}

//
//function changeClass(element){
//    if($(element).is(':checked')==true){
//        $(element).addClass('adminInput').next().removeClass('adminAb').addClass('adminA');
//        $(element).parent().find('label').append('<img class="img" src="static/resources/images/icon/checkbox-upper-checked.png">')
//    }else{
//        $(element).removeClass('adminInput').next().removeClass('adminA').addClass('adminAb');
//        $(element).parent().find('label').find('img').remove();
//    }
//}