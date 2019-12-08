/**
 * Created by jie on 2017/7/7.
 */

///////////////////////////////////

(function ($) {
    $.extend({
        chooseUser : function (options) {
            // default plugin settings
            var defaults = {
                title: '选择人员',
                url: '/api/list/teacher',
                multiselect: true, //默认多选
                confirm: null,
                origin_user_list: []
            };
            var opts = $.extend(defaults, options);
            /**初始化数据**/
            function initUser(){
                var init_user_list = function(){/**获取用户列表数据**/
                    myajax({
                        url: opts.url,
                        data: {
                            full_name : $.trim($('#modal-chooseUser input[name="full_name"]').val()),
                        },
                        async:false,
                        success:function(data){
                            var temp=data.d;
                            var html='';
                            for(var i=0;i<temp.length;i++) {
                                html +=
                                    '<div class="userDiv" userId="'+temp[i].id+'">' +
                                        '<img class="photo" alt="text" src="'+(temp[i].image_url?temp[i].image_url:'/static/resources/images/icon/photo-default.png')+'">' +
                                        '<span class="name">'+temp[i].full_name+'</span>' +
                                    '</div>';
                            }
                            $('#user-box').html(html).mCustomScrollbar();
                        }
                    });
                    $('.userDiv').on('click', function() {//选择人员
                        var user_id = $(this).attr('userId');
                        var full_name = $(this).children('span.name').html();
                        var image_url = $(this).children('img').attr('src');
                        //多选
                        if(opts.multiselect){
                            $(this).toggleClass('blue');
                            if ( $(this).hasClass('blue') ){
                                opts.origin_user_list.push({
                                    full_name: full_name,
                                    id: user_id,
                                    image_url: image_url
                                });
                                $('#modal-chooseUser .head-left-box').append(
                                    '<span class="choosed-user-box" userId="'+user_id+'">' +
                                        full_name +
                                        '<el class="remove-btn">×</el>' +
                                    '</span>'
                                );
                                bindUnchooseUser(user_id);
                            }else{
                                for(var i=0; i<opts.origin_user_list.length; i++){
                                    if ( opts.origin_user_list[i].id == user_id ){
                                        opts.origin_user_list.splice(i,1);
                                    }
                                };
                                $('#modal-chooseUser .head-left-box .choosed-user-box[userId="'+user_id+'"]').remove();
                            }
                        }else{ //单选
                            opts.origin_user_list.splice(0, opts.origin_user_list.length);
                            $('#modal-chooseUser .userDiv').removeClass('blue');
                            $('#modal-chooseUser .head-left-box').html('').append(
                                '<span class="choosed-lab">已选：</span>' +
                                '<span class="choosed-user-box" userId="'+user_id+'">' +
                                    full_name +
                                '</span>'
                            );
                            $(this).addClass('blue');
                            opts.origin_user_list.push({
                                full_name: full_name,
                                id: user_id,
                                image_url: image_url
                            });
                        }
                    });
                    defaultChoose();
                };
                layer.open({
                    type: 1,
                    area: ['880px', '480px'], //宽高
                    title: opts.title,
                    content: '<div id="modal-chooseUser" style="height:340px">'+
                            '<div id="ulForAdd">'+
                                '<div style="overflow:hidden;line-height:30px;">' +
                                    '<div class="head-left-box">' +
                                        '<span class="choosed-lab">已选：</span>' +
                                    '</div>' +
                                    '<div style="float:right;text-align: right;">'+
                                        '<input name="full_name" placeholder="请输入姓名">'+
                                        '<button id="init-user-btn" type="button" class="hx-margin20-l">查询</button>'+
                                    '</div>'+
                                '</div>' +
                                '<div id="user-box" style="height:330px"></div>'+
                            '</div>'+
                        '</div>',
                    btn:['确定','取消'],
                    yes: function (index) {
                        if ( $('#modal-chooseUser .userDiv.blue').length > 0 ){
                            //var user_ids = [];
                            //$('#modal-chooseUser .userDiv.blue').each(function (index,element) {
                            //    user_ids.push( $(element).attr('userId') );
                            //})
                            layer.close(index);
                            setuser_callback();
                        }else{
                            layer.msg('未选择');
                            return;
                        }
                    },
                    cancel: function(index){
                       layer.close(index);
                    }
                });
                init_user_list();
                $('#init-user-btn').on('click',function(){
                    init_user_list();
                });
            };

             //默认选中和已选择
            function defaultChoose(){
                for(var i=0; i<opts.origin_user_list.length; i++){
                    var user_id = opts.origin_user_list[i].id;
                    if (user_id){
                        $('#modal-chooseUser .userDiv[userId='+user_id+']').addClass('blue');
                    }
                    var _html = '<span class="choosed-user-box" userId="'+user_id+'">' +
                        opts.origin_user_list[i].full_name +
                        '<el class="remove-btn">×</el>' +
                    '</span>';
                    if ( $('#modal-chooseUser .head-left-box .choosed-user-box[userId="'+user_id+'"]').length <= 0 ){
                        $('#modal-chooseUser .head-left-box').append( _html );
                    }
                    bindUnchooseUser(user_id);
                };
            }

            //取消选中
            function bindUnchooseUser(user_id){
                $('#modal-chooseUser .choosed-user-box[userId="'+user_id+'"] .remove-btn').unbind().on('click', function () {
                    $(this).parent().remove();
                    $('#modal-chooseUser .userDiv[userId="'+user_id+'"]').removeClass('blue');
                    for(var i=0; i<opts.origin_user_list.length; i++){
                        if ( opts.origin_user_list[i].id == user_id ){
                            opts.origin_user_list.splice(i,1);
                        }
                    }
                });
            }

            //确认并返回
            function setuser_callback(){//回调
                if ( typeof (opts.confirm) == 'function'){
                    opts.confirm.apply(this,[opts.origin_user_list]);
                }
            }

            $(function () {
                initUser();
            });
        }
    });
})(jQuery);








