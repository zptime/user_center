/**
 * Created by jie on 2016/11/22.
 */
    $(function (){
        $(".pass-input-container").each(function(index, item){
            $(item).children('input').on('onmouseover', function () {
                $(item).children('input').addClass('pass-input-hover');
            });
            $(item).children('input').on('onmouseout', function () {
                $(item).children('input').removeClass('pass-input-hover');
            });
            $(item).children('input').on('focus',function(){
                if ($(item).children('input').val()==''){
                    $(item).children('input').removeClass('pass-input-error')
                    $(item).children('input').addClass('pass-input-focus');
                } else{
                    $(item).children('input').addClass('pass-input-focus');
                }
            });
            $(item).children('input').on('blur',function(){
                if ($(item).children('input').val()==''){
                    $(item).children('input').addClass('pass-input-error');
                    if($(item).children('input').attr('id') == 'newpassword'){
                        $(item).children('.pass-input-msg').html('请您填写密码');
                    }else{
                        $(item).children('.pass-input-msg').html('请您确认密码');
                    }
                }else{
                    $(item).children('input').removeClass('pass-input-error');
                    $(item).children('.pass-input-msg').html('');
                }
            });
            $(item).children('input').on('keydown',function(){
                $(item).children('.pass-input-msg').html('');
            });
        });
        $('#newpassword').focus();
        $("#submit").on('click',function(event){
            if ($('#verifypwd').val() != $('#newpassword').val()) {
                $('#error-tip').html('两次输入密码不一致');
                $('#pwd_flag').val('false');
                return;
            }else{
                $('#error-tip').html('');
                $('#pwd_flag').val('true');
            }
            if ($.trim($('#newpassword').val()) && $('#verifypwd').val() && $('#pwd_flag').val()=='true'){
                $.ajax({
                    url: '/api/unset/password',
                    type: 'POST',
                    data: {
                        mobile: $('#mobile').val(),
                        newpassword: $('#newpassword').val(),
                        newcopy: $('#verifypwd').val()
                    },
                    success: function (data) {
                        if (data.c == 0){
                            window.location.href = '/findpassword4';
                        }else{
                            $('#error-tip').html(data.m);
                        }
                    }
                })
            }
        });
    });
