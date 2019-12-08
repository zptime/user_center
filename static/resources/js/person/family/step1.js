/**
 * Created by jie on 2016/11/22.
 */
    $(function (){
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
                    if($(item).children('input').attr('id') == 'relation'){
                        $(item).children('.pass-input-msg').html('请您输入称谓');
                    }else if($(item).children('input').attr('id') == 'account'){
                        $(item).children('.pass-input-msg').html('请您输入手机');
                    }else{
                        $(item).children('.pass-input-msg').html('请输入验证码');
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
        $('.mod-step-detail input:eq(0)').get(0).focus();
        $('#veritycode').on('keyup', function () {
            if ($('#veritycode').val().length >= 4) {
                $.ajax({
                    url: '/api/check/imagecode',
                    type: 'POST',
                    data: {
                        code: $('#veritycode').val()
                    },
                    success: function (data) {
                        if (data.c == 0){
                            $('#veritycode_flag').val('true');
                            $('#error-tip').html('');
                        }else{
                            $('#veritycode_flag').val('false');
                            $('#error-tip').html('验证码错误');
                        }
                    }
                })
            }
        });
        $('#changecode').on('click', function () {
            document.getElementById('imgcode').src += '?';
        });
        $("#submit").on('click',function(event){
            parent.window.relation = $('#relation').val()
            if ($.trim($('#account').val())){
                if ($('#veritycode_flag').val()=='false'){
                    $('#error-tip').html('验证码错误');
                }else{
                    $.ajax({
                        url: '/api/verify/imagecode',
                        type: 'POST',
                        data: {
                            mobile: $('#account').val(),
                            code: $('#veritycode').val(),
                            check_mobile_account: 2
                        },
                        success: function (data) {
                            if (data.c== 0){
                                find_account($('#account').val());
                            }else{
                                $('#error-tip').html(data.m);
                            }
                        }
                    })
                }
            }
        });
    });


    function find_account(mobile){
        $.ajax({
            url: '/api/detail/account_by_mobile',
            type: 'POST',
            data: {
                mobile: $('#account').val(),
            },
            success: function (data) {
                if (data.c== 0){
                    account_info = data.d[0];
                    parent.window.parent_isnew = false;
                    parent.openStep2_2( $('#account').val(), account_info["id"], account_info["username"], account_info["full_name"], account_info["image_url"])
                }else{
                    parent.window.parent_isnew = true;
                    parent.openStep2( $('#account').val() )
                }
            }
        })
    }
