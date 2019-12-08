/**
 * Created by jie on 2016/11/22.
 */
    $(function (){
        $('#mobile').val( parent.window.mobile);
        $('#mobile_show').html( parent.window.mobile );

        //parent.window.parent_isnew
        if (parent.window.parent_isnew){
            $('.parent-isnew').css('display','block');
            $('#username').html( parent.window.mobile );
            $('#password').html( parent.window.mobile.substr(5,6));
        }else{
            debugger;
            $('.parent-exists').css('display','block');
            var image_url = '/static/resources/images/icon/photo-default.png';
            if(parent.window.image_url){
                image_url = parent.window.image_url;
            }
            $('#image_photo').attr('src',image_url);
            $('#parent_name').html( parent.window.full_name );
            $('#relation').html( parent.window.relation );
        }

        $("#mobile-suc-bind").on('click',function(event){
            parent.closeStep3();
        });
    });
