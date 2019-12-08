/**
 * Created by jie on 2016/11/22.
 */
    $(function (){
        $('#mobile').val( parent.window.mobile);
        $('#mobile_show').html( parent.window.mobile );
        $("#mobile-suc-bind").on('click',function(event){
            parent.closeStep3();
        });
    });
