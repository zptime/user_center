/**
 * Created by jie on 2017/4/19.
 */

var formObj = {};
$.extend(formObj, window.userObj, {school: HX_COM_ACCOUNT.getAccount().school_name});
var vm= new Vue({
    el: '#content',
    data: {
        form: formObj
    },
    computed: {
        c_is_in: function () {
            return getYNname(this.form.is_in);
        }
    },
    methods: {
        edit: function(){
            this.form.editable = true;
        },
        unedit: function(){
            this.form.editable = false;
        },
        check_username: function () {
            var _this = this;
            _this.form.username_tip = false;
            if ($.trim($('#username').val()).length > 0 && $.trim($('#username').val())!= _this.form.username){
                myajax({
                    url: '/api/check/username',
                    data: {
                        username: $.trim($('#username').val()),
                    },
                    complete: function(){

                    },
                    success: function(data){
                        if (data.c !=0 ){
                            _this.form.username_tip = true;
                        }
                    }
                })
            }
        }
    }
});


$(document).ready(function(){
    $(function () {
        //日期控件
        var birthday = {
            clearRestore: false,
            dateCell: '#modal-edit input[name="birthday"]',
            format: 'YYYY-MM-DD',
            isinitVal:false,   //是否初始化时间，默认不初始化时间
            isTime:false,      //是否开启时间选择
        };
        var in_date = {
            clearRestore: false,
            dateCell: '#modal-edit input[name="in_date"]',
            format: 'YYYY-MM-DD',
            isinitVal:false,   //是否初始化时间，默认不初始化时间
            isTime:false,      //是否开启时间选择
        };
        jeDate(birthday);
        jeDate(in_date);
    });
    $('form').on('keydown', function () {
        if(event.keyCode==13)
            return false;
    });
});


function myimportImg(){
    if (vm.form.editable){
        importImg();
    }
}
function mychangeImg(){
    if (vm.form.editable){
        changeImg();
    }
}


/**点击编辑个人信息**/
function editInfo(){
    layer.open({
        type: 1,
        title: '编辑个人信息',
        area: ['880px','480px'],
        content : $('#modal-edit'),
        btn:['确定','取消'],
        yes: function(index){
            if (!mycheck({ element: '#modal-edit'})) {
                return;
            }
            var data = Serializetojson($('#modal-edit form').formSerialize());
            postData = {
                account_id: $('#account_id').val()
            };
            postData [user_type_key_str+'_info'] = JSON.stringify(data);
            myajax({
                url: '/api/update/'+user_type_key_str,
                data: postData
            },function(data){
                if(data.c == 0){
                    layer.close(index);
                    layer.msg('操作成功', {time:1000}, function () {
                        window.location.reload();
                    });
                }
            })
        },
        cancel: function(index){
            layer.close(index);
        }
    });
}


