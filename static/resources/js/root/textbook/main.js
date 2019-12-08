/**
 * Created by jie on 2017/3/27.
 */

var vm= new Vue({
    el: '#content',
    data: {
        multiple: false,
        frozen_flag: false, //毕业的学生视图开关
        grade_num: '',
        grade_list: CONST.K12,
        subject_list: '',
        subject_id: '',
        year_list : HX_CACHE.YEAR_LIST,
        kind_list: CONST_ARR.KIND_LIST,
        freezeBookName:'',
    },
    computed: {

    },
    methods: {
        switch_frozen_flag: function(flag){
            this.multiple = false;
            this.frozen_flag = flag;
            reloadGrid();
        },
    }
});

$(document).ready(function(){

    myjqGrid( $('#grid') ,{
        postData:{
        },
        url: '/api/admin_list/textbook',
        colNames: ['id','grade_num','年级','科目','教材版本','章节个数','操作'],
        colModel: [
            {name: 'id',hidden:true},
            {name: 'grade_num',hidden:true},
            {name: 'grade_name', width: 150, align: "center", sortable: false},
            {name: 'subject_name', width: 100, align: "center", sortable: false},
            {name: 'textbook_name', width: 100, align: "center", sortable: false},
            {name: 'chapter_count', width: 100, align: "center", sortable: false},
            {name:'oper',width:200,formatter: fmt_oper, align:"center",sortable:false}
        ],
        choosed: function (multiple) {
            vm.multiple = multiple;
        },
        multiselect: false,
        //multipleBtn: '#grid_multipleBtn',
        ispaged: true
    },function(){

    });
    function fmt_oper(cellvalue, options, rowObject) {
        var id = rowObject.id;
        var _html = '<span class="mytooltip">...<span class="mytooltiptext">';
        if(vm.frozen_flag){
            _html+='<li  onclick="unfreeze(' + id + ')">解除冻结</li><li  onclick="del(' + id + ')">删除</li></span></span>'
            }else{
            _html+='<li  onclick="add_chapter(' + id + ')">添加章节</li><li  onclick="edit(' + id + ')">编辑教材</li><li  onclick="freeze(' + id + ')">冻结</li></span></span>'
        }
        return _html;
    }

    myajax({
        url:'/api/admin_list/subject',
        data:'',
        async:true,
        success:function(data){
            if (data.c == 0){
                vm.subject_list=data.d;
            }
        }
    })

});

//添加章节
function add_chapter(textbookId){
    if (textbookId){
        window.location.href = '/root/index?cuspath=page/root/textbook/chapter.html&textbookId='+textbookId;
    }else{
        layer.msg('未选择教材');
    }
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
                    url: '/api/admin_delete/textbook',
                    data: {
                        textbook_id: id
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

function edit(id){
    var rowObject = $("#grid").getLocalRow(id);
    if(!rowObject) {
        rowObject = $("#grid").getRowData(id);
    }
    if (!rowObject){
        rowObject = $("#grid").getGridRowById(id);
    }
     $('#bookNameSec').val(rowObject.textbook_name);
     $('#bookGrad').val(rowObject.grade_num);
    layer.open({
        type: 1,
        title: '编辑教材',
        area: ['550px', '330px'],
        content : $('#editBook'),
        btn:['确定','取消'],
        btn1: function(index){

            var data = {
                textbook_id: id,
                textbook_name: $("#bookNameSec").val(),
                grade_num: $("#bookGrad").val()
            };
            myajax({
                aysnc: false,
                url: '/api/admin_edit/textbook',
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

function freeze(id){
    var rowObject = $("#grid").getLocalRow(id);
    if(!rowObject) {
        rowObject = $("#grid").getRowData(id);
    }
    if (!rowObject){
        rowObject = $("#grid").getGridRowById(id);
    }
    var textbook_id=rowObject.id;
    vm.freezeBookName=rowObject.textbook_name;
    layer.open({
        type: 1,
        title: '冻结确认',
        area: ['550px', '330px'],
        content : $('#freezeSub'),
        btn:['确定','取消'],
        btn1: function(index){
            var data = {
                textbook_id:textbook_id
            };
            myajax({
                aysnc: false,
                url: '/api/admin_freeze/textbook',
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

function unfreeze(id){
    if(!id){
        layer.msg('未选择记录');
    }
    myajax({
        aysnc: false,
        url: '/api/admin_unfreeze/textbook',
        data:  {
            textbook_id: id
        }
    },function(data){
        if(data.c == 0){
            reloadGrid();
            layer.msg('解冻成功');
        }
    })
}

function reloadGrid(elementGrade, elementSubject){
    var isActive;
        if(vm.frozen_flag){
            isActive=0;
        }else{
            isActive=1;
        }
    if (elementGrade){
        vm.grade_num = $(elementGrade).attr('grade');;
    }
    if (elementSubject){
        vm.subject_id = $(elementSubject).attr('subject');
    }

    var grade_num_list = [];
    var subject_id_list = [];
    if (vm.grade_num){
        grade_num_list[0] = parseInt(vm.grade_num);
    }
    if (vm.subject_id){
        subject_id_list[0] = parseInt(vm.subject_id) ;
    }
    var data={
        is_active:isActive,
        grade_num_list: JSON.stringify(grade_num_list),
        subject_id_list: JSON.stringify(subject_id_list)
    };
    $("#grid").jqGrid('setGridParam', {
        url: '/api/admin_list/textbook',
        dataType: "json",
        mType: "POST",
        postData:data,
        page: 1
    }).trigger("reloadGrid");
}

function add(){
    layer.open({
        type: 1,
        title: '添加教材',
        area: ['550px', '330px'],
        content : $('#addBook'),
        btn:['确定','取消'],
        btn1: function(index){
            var data = {
                subject_id: $('#selSubject').val(),
                textbook_name: $("#bookName").val(),
                grade_num:$('#selGradeNum').val()
            };
            myajax({
                aysnc: false,
                url: '/api/admin_add/textbook',
                data:data
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
