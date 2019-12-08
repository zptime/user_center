/**
 * Created by jie on 2017/4/19.
 */


var vm= new Vue({
    el: '#content',
    data: {
        form: {
            //class_id: null,
            //class_name: "",
            //class_manager: "",
            //status: 1
        }
    }
});

$(document).ready(function(){
    get_myclass();
});

//获取我申请（加入）的班级
function get_myclass(){
    myajax({
        url: '/api/detail/student_class_application',
        async: false
    }, function (data) {
        if(data.c == 0){
            vm.form = data.d[0];
        }
    });
}

//申请加入班级
function applyClass(){
    if (!mycheck({ element: '#modal-join'})) {
        return;
    }
    myajax({
        url: '/api/add/student_class_application',
        data: {
            class_code: $.trim( $('#class_code').val() ),
            comments: $.trim( $('#comments').val() ),
        }
    }, function (data) {
        if(data.c == 0){
            window.location.reload();
        }
    })
}

//重新申请加入班级
function rejoinClass(){
    vm.form.class_id = null;
}