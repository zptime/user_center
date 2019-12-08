/**
 * Created by jie on 2017/4/19.
 */
//清理缓存
if ($('#recache').val()){
    HX_CACHE.refresh();
}

const USER_TYPE = {
    USER_TYPE_NOT_SET : 0,
    USER_TYPE_STUDENT : 1,
    USER_TYPE_TEACHER : 2,
    USER_TYPE_PARENT : 4
};

(function () {
    //首焦
    $('.person-firstcoke-box .person-photo').attr('src',HX_COM_ACCOUNT.getAccount().image_url ? HX_COM_ACCOUNT.getAccount().image_url : ICON.PHOTO_DEFAULT);
    $('.person-firstcoke-box .person-box .person-photo-box').on('mouseenter', function () {
        $('.person-firstcoke-box .person-box .up-person-photo-box').css('display','inherit');
    }).on('mouseleave', function () {
        $('.person-firstcoke-box .person-box .up-person-photo-box').css('display','none');
    });
    $('.up-person-photo-box').on('click',function(){
        upload_photo()
    });
    $('.person-firstcoke-box .person-name').html(HX_COM_ACCOUNT.getAccount().full_name);
    $('.person-firstcoke-box .person-school').html(HX_COM_ACCOUNT.getAccount().school_name);
    //用户
    var user_type = parseInt($('#user_type').val());
    var key_str = '';
    switch (user_type){
        case USER_TYPE.USER_TYPE_STUDENT:
            key_str = 'student';
            break;
        case USER_TYPE.USER_TYPE_TEACHER:
            key_str = 'teacher';
            break;
        case USER_TYPE.USER_TYPE_PARENT:
            key_str = 'parent';
            break;
    };
    window.user_type_key_str = key_str;
    window.userObj = {
        user_type: user_type
    };
    function getDetail(){
        var data={
            account_id: $('#account_id').val()
        };
        data[ user_type_key_str+'_id' ] = $('#id').val();
        myajax({
            url: '/api/detail/'+user_type_key_str,
            data: data,
            async: false
        },function(data){
            if (data.c == 0){
                $.extend(window.userObj, data.d[0]);
            }
        });
    }
    getDetail();
})();

$(document).ready(function(){
    //切换导航栏
    $('.main-nav li').on('click',function(){
        var a = this;
        url_go( '/person/index?nav='+ a.id );
    })
});

function upload_photo(){
    layer.open({
        type: 2,
        title: '更改头像',
        area: ['780px','480px'],
        content :"/static/resources/js/person/share/upload_photo.html",
        btn:['保存','取消'],
        yes: function(index){
            $("iframe").contents().find("#submit_photo").click()
        },
        cancel: function(index){
            layer.close(index);
        }
    });
}

function upload_photo_success(image_url){
    data = {"image_url": image_url, "id": window.userObj.id};
    postData = {
        account_id: $('#account_id').val(),
    };
    postData [user_type_key_str+'_info'] = JSON.stringify(data);
    var ret_val = false;
    myajax({
        url: '/api/update/'+user_type_key_str,
        data: postData,
        async: false
    },function(data){
        if(data.c == 0){
            layer.msg('操作成功', {time:1000}, function () {
                window.location.reload();
            });
            ret_val = true
        } else {
            ret_val = data.m
        }
    });
    return ret_val;
}

