var formObj = {};
$.extend(formObj, window.userObj);

var vm= new Vue({
    el: '#content',
    data: {
        form: formObj,
        parent_student_list: [
            //{
            //    "id": "1",
            //    "student_id": "1",
            //    "student_full_name": "student_full_name",
            //    "student_code": "student_code",
            //    "student_class_name": "student_class_name",
            //    "parent_id": "parent_id",
            //    "parent_full_name": "parent_full_name",
            //    "parent_mobile": "parent_mobile",
            //    "relation": "relation",
            //    "comments": "comments",
            //    "status": "status"  //申请状态(1, u"未处理")(2, u"已同意")(3, u"已拒绝")，空为全部
            //},
        ]
    },
    computed: {

    },
    methods: {
        get_img_url: function (index) {
            var res = '/static/resources/images/icon/photo-default.png';
            if (index>=0){
                if (this.form.user_type == 1){ //当前用户为学生
                    if (this.parent_student_list[index].parent_img_url)
                        res =  this.parent_student_list[index].parent_img_url
                }else{
                    if (this.parent_student_list[index].student_img_url)
                        res =  this.parent_student_list[index].student_img_url
                }
            }
            return res;
        },
        get_tips: function (index) {
            var res = '';
            if (index>=0){
                var status = parseInt(this.parent_student_list[index].status);
                switch ( status ){
                    case 1:
                        if (this.form.user_type == 1){
                            res = '邀请已发出';
                        }else{
                            res = '邀请您加入家庭组';
                        };
                        break;
                    case 2:
                        if (this.form.user_type == 1){
                            res = this.parent_student_list[index].relation;
                        }else{
                            res =  this.parent_student_list[index].student_class_name;
                        };
                        break;
                    case 3:
                        if (this.form.user_type == 1){
                            res = '邀请已拒绝';
                        }else{
                            res = '您已拒绝加入家庭组';
                        };
                        break;
                }
            }
            return res;
        }
    }
});

$(document).ready(function () {
    //获取学生-家长管理列表
    get_parent_student();
});

//获取学生-家长管理列表
function get_parent_student(){
    myajax({
        url: '/api/list/parent_student',
    }, function (data) {
        if ( data.c==0 ){
            vm.parent_student_list = data.d;
        }
    });
}

function openStep1() {
    var m_step1 = layer.open({
        type: 2,
        title: '邀请家长',
        area: ['880px', '480px'],
        content: '/static/resources/js/person/family/step1.html',
    });
    window.m_step1 = m_step1;
}

function openStep2( mobile ){
    window.mobile = mobile;
    layer.close(m_step1);
    var m_step2 = layer.open({
        type:2,
        title:  '邀请家长',
        area: ['880px', '480px'],
        content: '/static/resources/js/person/family/step2.html'
    });
    window.m_step2 = m_step2;
}

function openStep2_2( mobile, account_id, username, full_name, image_url){
    window.mobile = mobile;
    window.account_id = account_id;
    window.username = username;
    window.image_url = image_url;
    window.full_name = full_name;

    layer.close(m_step1);
    var m_step2_2 = layer.open({
        type:2,
        title:  '邀请家长',
        area: ['880px', '480px'],
        content: '/static/resources/js/person/family/step2_2.html'
    });
    window.m_step2 = m_step2_2;
}

function openStep3(){
    layer.close(m_step2);
    var m_step3 = layer.open({
        type:2,
        title:  '邀请家长',
        area: ['880px', '480px'],
        content: '/static/resources/js/person/family/step3.html'
    });
    window.m_step3 = m_step3;
};

function closeStep3() {
    layer.close(m_step3);
}

function closeStep2() {
    layer.close(m_step2);
}


//处理邀请 同意or拒绝
function dealApply(element, flag){
    var status = 3;
    if (flag){
        status = 2;
    }
    if(element){
        var index = $(element).attr('index');
        var obj = vm.parent_student_list[index];
        myajax({
            url: '/api/update/parent_student',
            data: {
                parent_student_id: obj.id,
                status: status
            }
        }, function (data) {
            if (data.c == 0){
                //刷新列表
                get_parent_student();
            }
        });
    }else{
        layer.alert('未选择'+ (vm.form.user_type == 1?'家长':'学生'));
    }
}

//修改昵称
function editRelation(element){
    if(element){
        var index = $(element).attr('index');
        var obj = vm.parent_student_list[index];
        layer.open({
            type: 1,
            title: '修改昵称',
            area: ['550px', '330px'],
            content: $('#modal-edit-relation'),
            btn: ['确定','取消'],
            yes: function(index){
                myajax({
                    url: '/api/update/parent_student',
                    data: {
                        parent_student_id: obj.id,
                        relation: $(".relation-name").val()
                    }
                }, function (data) {
                    if (data.c == 0){
                        layer.close(index);
                        //刷新列表
                        get_parent_student();
                    }
                });
            }
        });
    }else{
        layer.alert('未选择'+ (vm.form.user_type == 1?'家长':'学生'));
    }
    $('#modal-edit-relation input[name="relation"]').val( obj.relation );
}

//删除家长-学生对应关系
function del(element){
    if(element){
        var index = $(element).attr('index');
        var obj = vm.parent_student_list[index];
        var tips='';
        if (vm.form.user_type == 1){
            tips = '家长[ '+ obj.parent_full_name + ' ]';
        }else{
            tips = '学生[ '+ obj.student_full_name + ' ]';
        }
        layer.confirm('确认删除' + tips + '吗?', function (index) {
            myajax({
                url: '/api/delete/parent_student',
                data: {
                    parent_student_id: obj.id,
                }
            }, function (data) {
                if (data.c == 0){
                    layer.close(index);
                    //刷新列表
                    get_parent_student();
                }
            });
        });
    }else{
        layer.alert('未选择'+ (vm.form.user_type == 1?'家长':'学生'));
    }
}