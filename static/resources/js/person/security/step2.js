/**
 * Created by jie on 2016/11/22.
 */
    $(function (){
        $('#input-mobile').val(parent.window.mobile);
        $('#mobile_value').html(encrypt());
        $(".pass-input-container").each(function(index, item){
            $(item).children('input').on('onmouseover', function () {
                $(item).children('input').addClass('pass-input-hover');
                $(item).children('label').addClass('pass-input-label-hover');
            });
            $(item).children('input').on('onmouseout', function () {
                $(item).children('input').removeClass('pass-input-hover');
                $(item).children('label').removeClass('pass-input-label-hover');
            });
            $(item).children('input').on('focus',function(){
                if ($(item).children('input').val()==''){
                    $(item).children('input').removeClass('pass-input-error')
                    $(item).children('input').addClass('pass-input-focus');
                    $(item).children('label').addClass('pass-input-label-focus');
                    $(item).children('label').attr('style','display: block;');
                } else{
                    $(item).children('input').addClass('pass-input-focus');
                    $(item).children('label').removeClass('pass-input-label-focus');
                    $(item).children('label').attr('style','display: none;');
                }
            });
            $(item).children('input').on('blur',function(){
                if ($(item).children('input').val()==''){
                    $(item).children('input').addClass('pass-input-error');
                    $(item).children('label').attr('style','display: block;');
                    if($(item).children('input').attr('id') == 'mobileVcode'){
                        $(item).children('.pass-input-msg').html('请填写验证码');
                    }
                }else{
                    $(item).children('input').removeClass('pass-input-error');
                    $(item).children('label').attr('style','display: none;');
                    $(item).children('.pass-input-msg').html('');
                }
            });
            $(item).children('input').on('keydown',function(){
                $(item).children('label').attr('style','display: none;');
                $(item).children('.pass-input-msg').html('');
            });
        });
        function test(){
            alert('123123');
        }
        $('#pass-button-new1').on('click', function () {
            if ($(this).html() == '发送验证码'){
                $(this).html('');
                $.ajax({
                    url: '/api/send/messagecode',
                    type: 'GET',
                    data: {
                        mobile: $('#input-mobile').val(),
                    },
                    complete: function () {
                        intervalProcess = setInterval("count_time()" , 1000);

                    },
                    success: function (data) {
                        if (data.c == 0){
                            $('#forgot-mobileVcode-success').html('验证码已发送');
                        }
                    }
                })
            }
        });
        $('#mobileVcode').focus();
        $("#submit").on('click',function(event){
            if ($.trim($('#mobileVcode').val())){
                $.ajax({
                    url: '/api/verify/messagecode',
                    type: 'POST',
                    data: {
                        mobile: $('#input-mobile').val(),
                        code: $('#mobileVcode').val()
                    },
                    success: function (data) {
                        if (data.c == 0){
                            reset_mobile($('#input-mobile').val(), $('#mobileVcode').val())
                        }else{
                            $('#forgot-mobileVcode-tip').html(data.m);
                        }
                    }
                })
            }
        });
    });
    var count = 120;
    var intervalProcess = null;
    function count_time(){
        count -= 1;
        if(count){
            $('#pass-button-new1').addClass('pass-button-timer-timing');
            //$('#forgot-mobileVcode-success').html('验证码已发送');
            $('#pass-button-new1').html('重新发送('+ count +')');
        }else{
            clearInterval(intervalProcess);
            count = 120;
            $('#pass-button-new1').removeClass('pass-button-timer-timing');
            $('#pass-button-new1').html('发送验证码');
        };
    };
    function encrypt(){
        var str = parent.window.mobile  ,arr = str.split(''),res='';
        if (arr.length == 11){
            res= arr[0]+arr[1]+arr[2]+'******'+arr[9]+arr[10];
        }
        return '手机 '+res;
    }

    function reset_mobile(new_mobile, messagecode){
        $.ajax({
            url: '/api/reset/mobile',
            type: 'POST',
            data: {
                new_mobile: new_mobile,
                messagecode:messagecode
            },
            success: function (data) {
                if (data.c == 0){
                    parent.openStep3( $('#account').val() )
                }else{
                    $('#forgot-mobileVcode-tip').html(data.m);
                }
            }
        })
    }