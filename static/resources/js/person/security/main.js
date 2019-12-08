/**
 * Created by jie on 2017/4/19.
 */

var formObj = {};
$.extend(formObj, window.userObj);

var vm= new Vue({
    el: '#content',
    data: {
        form: formObj
    },
    computed: {

    },
    methods: {
        encrypt: function(){
            var str = this.form.mobile  ,arr = str.split(''), res='';
            if (arr.length == 11){
                res= arr[0]+arr[1]+arr[2]+'*****'+arr[8]+arr[9]+arr[10];
            }
            return res;
        },
        get_user_name: function(){
            return this.form.username
        }
    }
});

$(document).ready(function(){
    //bind
    $('.security button.upmobile').on('click', function () {
        openStep1();
    });
    $('.security button.uppwd').on('click', function () {
        upPwd();
    });
})

//更换手机号码
function openStep1() {
    var m_step1 = layer.open({
        type: 2,
        title: vm.form.mobile ? '更换手机':'绑定手机',
        area: ['880px', '480px'],
        content: '/static/resources/js/person/security/step1.html',
    });
    window.m_step1 = m_step1;
}

function openStep2( mobile ){
    window.mobile = mobile;
    layer.close(m_step1);
    var m_step2 = layer.open({
        type:2,
        title: vm.form.mobile ? '更换手机':'绑定手机',
        area: ['880px', '480px'],
        content: '/static/resources/js/person/security/step2.html'
    });
    window.m_step2 = m_step2;
}

function openStep3( mobile ){
    layer.close(m_step2);
    var m_step3 = layer.open({
        type:2,
        title: vm.form.mobile ? '更换手机':'绑定手机',
        area: ['880px', '480px'],
        content: '/static/resources/js/person/security/step3.html'
    });
    window.m_step3 = m_step3;
};

function closeStep3() {
    layer.close(m_step3);
}

//修改密码弹框
function upPwd(){
    layer.open({
          type: 1,
          area: ['550px', '330px'], //宽高
          title:'修改密码',
          content: $('#modal-setpwd'),
          btn:['确定','取消'],
          btn1: function(index, layero){
             //按钮【确定】的回调
             if($.trim($('#oldpwd').val()) && $.trim($('#newpwd').val()) && $('#newpwd').val()==$('#newpwd2').val()){
                resetPwd(index);
             }else{
                layer.msg('密码为空或两次密码不相同');
             }
             return false;
          },
          cancel: function (index) {
              $('#oldpwd').val('');
              $('#newpwd').val('');
              $('#newpwd2').val('');
              $("#tishi").css('display','none');
              layer.close(index);
              return false;
          }
        });
}

/**重置密码**/
function resetPwd(index){
    var data = {
        "new_password": $("#newpwd").val(),
        "old_password": $("#oldpwd").val()
    };
    $.ajax({
        url: '/api/reset/password',
        type: 'POST',
        dataType: 'json',
        data: data,
        aysnc: false,
        error: function(data) {
            console.log('请求超时');
            layer.msg("请求超时");
        },
        success: function(data) {
            if(data.c == 0){
                layer.close(index);
                layer.msg('操作成功,请重新登录！', {
                    anim:6,
                    time:3000,
                    skin:'layui-layer-hui'
                },function(){
                    window.location.href = '/logout';
                });
            }else{
                console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                layer.msg('操作失败：' + data.m)
            }
        }
    })
}

/**判断两次密码是否相同**/
function pwdConfirm(){
    var pwd=$('#newpwd').val();
    var pwd2=$('#newpwd2').val();
    if(pwd!=pwd2){
         document.getElementById("tishi").style.display='block';
    }else{
         document.getElementById("tishi").style.display='none';
    }
}


