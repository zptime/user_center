/**
 * Created by jie on 2016/11/22.
 */
    $(function (){
        var image_url = '/static/resources/images/icon/photo-default.png';
        if(parent.window.image_url){
            image_url = parent.window.image_url;
        }
        $('#full_name').html( parent.window.full_name );
        $('#mobile').html( parent.window.mobile );
        $('#account_id').html( parent.window.account_id );
        $('#username').html( parent.window.username );
        $('#image_photo').attr('src',image_url);
    });
    function cancel(){
        parent.closeStep2();
    }
    function submit_application(){
         $.ajax({
            url: '/api/add/parent_by_student',
            type: 'POST',
            data: {
                mobile: parent.window.mobile,
                relation: parent.window.relation
            },
            success: function (data) {
                if (data.c== 0){
                    parent.openStep3()
                }else{
                    $('#err-msg-tip').html(data.m);
                }
            }
        })
    }