/**
 * Created by jie on 2017/3/27.
 */

var vm= new Vue({
    el: '#content',
    data: {
        grade_list: HX_CACHE.get_grade_list(),
        class_list: HX_CACHE.get_class_list(),
        class_graduate_switch : 'CLASS',
        grade_num: '',
        grade_name: '',
        subject_list: [],
        textbook_list:[],
        subjectName: '',
        textbook_id: '',
        subject_id:'',
        selSubList:[],
        selBookList:[],
        subject_list_disp:[],
        gradNumList:[],
        subIdList:[],
        gradBookList:[]
    },
    computed: {

    },
    methods: {
        cancel_choose: function(index){
            if (index>=0 && index<vm.manager_list.length){
                this.manager_list.splice(index,1);
            }
        }
    }
});

$(document).ready(function(){

    myajax({
        url:'/api/school_list/subject',
        data:'',
        async:false,
        success:function(data) {
            if (data.c == 0){
                vm.subject_list_disp=data.d;
            }
        }
    });

    myajax({
        url:'/api/school_list/subject',
        data:'',
        async:false,
        success:function(data) {
            if (data.c == 0){
                vm.subject_list=data.d;
            }
        }
    });


    myajax({
        url: '/api/school_list/textbook',
        data: '',
        async: false,
        success: function (data) {
            if (data.c == 0) {
                vm.textbook_list = data.d;
            }
        }
    })

});

function add(element){
    $('#tbGrade').val($(element).attr('grade_num'));
    var data={
        not_belong_flag:1
    };
    myajax({
        url:'/api/school_list/textbook',
        data:data,
        async:false,
        success:function(data) {
            var selList=[];
            var temp=data.d;
            for (var i =0;i<temp.length;i++) {
                if (temp[i].grade_num == $('#tbGrade').val()) {
                    selList.push(temp[i]);
                }
            }
            vm.selBookList=selList;
            vm.gradBookList=selList;
        }
    });
    layer.open({
        type: 1,
        title: '添加教材',
        area: ['580px', '370px'],
        content : $('#addBook'),
        btn:['确定','取消'],
        yes: function(index){
            if(!mycheck({element:"#tableAdd"})){
                return;
            }
                var data = {
                    subject_id: $('#selSubject').val(),
                    textbook_id: $('#selTextbook').val()
                };
                myajax({
                    aysnc: false,
                    url: '/api/school_add/textbook',
                    data: data
                }, function (data) {
                    if (data.c == 0) {
                        reloadGrid();
                        layer.close(index);
                        layer.msg('操作成功');
                    }
                });
            $('#selSubject').val('');
        },
        cancel: function(index){
            $('#selSubject').val('');
            layer.close(index);
        }
    });
}

function freeze(){
    layer.open({
        type: 1,
        title: '冻结确认',
        area: ['705px', '440px'],
        content : $('#freeze'),
        btn:['确定','取消'],
        btn1: function(index){
            var data = {
                "grade_num": '',
                "class_num": $("#class_num").val()
            };
            myajax({
                aysnc: false,
                url: '/api/school_freeze/textbook',
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

function del(element){
    var id=$(element).attr('textbook-id');
    layer.confirm('确认删除选中记录吗?', {
        title: '提示',
        btn:['确定','取消'],
        btn1: function (index) {
            layer.close(index);
            myajax({
                aysnc: false,
                url: '/api/school_delete/textbook',
                data: {
                    textbook_id: id
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

function reloadGrid(elementGrade, elementSubject){
    if (elementGrade){
        vm.grade_num = $(elementGrade).attr('grade');
    };
    if (elementSubject){
        vm.subject_id = $(elementSubject).attr('subId');
    }

    var data={};
    var grade_numARR = [];
    var subject_idARR = [];
    if (vm.grade_num){
        grade_numARR.push( parseInt(vm.grade_num));
    }
    if (vm.subject_id){
        subject_idARR.push( parseInt(vm.subject_id));
    }
    data['grade_num_list'] = JSON.stringify(grade_numARR);
    data['subject_id_list'] = JSON.stringify(subject_idARR);

    myajax({
        url: '/api/school_list/textbook',
        data: data,
        async: false,
        success: function (data) {
            if (data.c == 0) {
                vm.textbook_list = data.d;
            }
        }
    })
}



function locateDetail(){
    var data={
        not_belong_flag:1
    };
    myajax({
        url:'/api/school_list/textbook',
        data:data,
        async:false,
        success:function(data) {
            var selList=[];
            var temp=data.d;
            if($('#selSubject').val()!="") {
                for (var i =0;i<temp.length;i++) {
                    if (temp[i].grade_num==$('#tbGrade').val() && temp[i].subject_name==$('#selSubject').find("option:selected").text()) {
                        selList.push(temp[i]);
                    }
                }
                vm.selBookList=selList;
            }else{
                vm.selBookList=vm.gradBookList;
            }
        }
    });
}