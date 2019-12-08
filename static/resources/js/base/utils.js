/**
 * Created by jie on 2016/10/20.
 */

function getURLString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null)
        return unescape(r[2]);
    return '';
}
function getYNname(val) {
    var res = '';
    if (val == '1') {
        res = '是'
    } else if (val == '0') {
        res = '否'
    }
    return res
}
function Serializetojson(str) {
    "use strict";
    str = str.replace(/\+/g," ");
    var res = {},
    arr = decodeURIComponent(str, true).split('&');
    for (var i in arr) {
        var item = arr[i].split('='),
        key = item[0],
        value = item[1];
        res[key] = value
    }
    return res
}
function formatnumber(data, leng){
    var res='',data_str=data.toString(),v_length=leng?leng:2;
    if (data_str.length < v_length){
        for (var i=0; i< v_length - data_str.length; i++ ){
            res += '0';
        }
    }
    res += data_str;
    return res;
}
function url_go(url) {
    window.location.href = encodeURI(url)
}
function url_back() {
    window.history.go( - 1)
}
function mycheck(opt){
    var res = true;
    defaults = {
        element: '#content',
    }
    var settings = extend(defaults, opt);
    //校验
    $(settings.element+' label.required').each(function(index,element){
        var el_check = $(element).attr('for');
        if (el_check){
            var el =  $('[check="'+el_check+'"]') ;
            var loop2 = true;
            el.each(function (index2, element2) {
                if ( !$(element2).val() ){
                    layer.msg($(element).text()+'不允许为空');
                    element2.focus();
                    loop2 = false;
                    res = false;
                    return false;
                }
            });
            return loop2;
        }
    });
    return res;
}
function submit_with_parameters(action, method, values) {
    var form = $('<form/>', {
        action: action,
        method: method
    });
    $.each(values, function() {
        form.append($('<input/>', {
            type: 'hidden',
            name: this.name,
            value: this.value
        }));
    });
    form.appendTo('body').submit();
}

function myajax(opt, callback) {
    if (!opt.url) return '未配置url';
    defaults = {
        url: '',
        type: 'POST',
        dataType: 'json',
        complete: function(data) {
            if (typeof callback == 'function') {
                callback(JSON.parse(data.responseText))
            }
        },
        error: function(data) {
            console.log('请求超时');
            layer.msg("请求超时");
        },
        success: function(data) {
            if (data.c != 0) {
                console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                layer.msg('操作失败：' + data.m)
            }
        }
    };
    var settings = extend(defaults, opt);
    $.ajax(settings)
}

function myajaxForm(el, opt) {
    if (!opt.url) return '未配置url';
    var defaults = {
        target: '_self',
        success: function(data) {
            if (data.c == 0) {
                if (opt.successed && typeof opt.successed == 'function'){
                    opt.successed(data);
                };
                layer.alert('操作成功', function(index){
                  //do something
                    if (opt.next_path){
                        if (opt.next_path == '_self'){
                            layer.close(index);
                        }else{
                            url_go(opt.next_path);
                        }
                    }else{
                        url_back();
                    }
                });
            } else if (data.c != 0) {
                console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                layer.msg('操作失败：' + data.m)
            }
        },
        url: '',
        type: 'POST',
        dataType: 'json',
        //resetForm: true,
    }
    var settings = extend(defaults, opt);
    el.ajaxForm(settings)
}
function extend(target, source) {
    "use strict";
    var property;
    for (property in source) {
        if (source.hasOwnProperty(property)) {
            target[property] = source[property]
        }
    }
    return target
};
function myjqGrid(el, opt, callback) {
    if (!opt.url) return '未配置url';
    if (!opt.colNames.length || !opt.colModel.length) return 'colNames或colModel配置不正确';
    if (opt.colNames.length != opt.colModel.length) return '列colNames和colModel长度不匹配';
    var el_id = el.attr('id');
    /**未分页**/
    defaults = {
        url: '',
        datatype: "json",
        mtype: "POST",
        postData: {},
        height: 'auto',
        autowidth: true,
        colNames: [],
        colModel: [],
        rowNum: 50,
        rowList:[50,100],
        pager: '#pager',
        viewrecords: true,
        multiselect: true,
        multiselectWidth:24,//多选框宽度
        gridview: true, //加速显示
        loadonce: false,
        altRows: true,
        altclass: 'zebra',
        pagerpos: "center", //指定分页栏的位置
        //sortname : 'id',
        //sortorder : "desc",
        //cellEdit:true,//与editable属性对应
        //multiboxonly: true, //是否只有点击多选框时
        jsonReader: {
            root: "d"
        },
        /*beforeSelectRow: function(rowid, e) {
            var $myGrid = $(this),
            i = $.jgrid.getCellIndex($(e.target).closest('td')[0]),
            cm = $myGrid.jqGrid('getGridParam', 'colModel');
            return (cm[i].name === 'cb')
        },*/ //仅点击checkebox才可选择行
        loadComplete: function() {
            var re_records = $("#grid").getGridParam('records');
            if (re_records == 0 || re_records == null) {
                if ($(".norecords").html() == null) {
                    $("#grid").parent().append("<div class=\"norecords\">没有符合条件的数据</div>")
                }
                $(".norecords").show()
            } else {
                if ($(".norecords").html()) {
                    $(".norecords").hide()
                }
                var height = re_records < 5? "210":"auto";
                $('#grid').jqGrid('setGridHeight', height).trigger('reloadGrid');
            }
            if (typeof callback == 'function') {
                callback()
            }
        },
        gridComplete: function() {//当表格所有数据都加载完成，处理统计行数据
            //表格多选框，多控监听
            if (opt.multipleBtn){
                $(opt.multipleBtn).prop('checked',false).unbind('click').on('click', function () {
                    $('#cb_'+el_id).click();
                })
            };
            //分页信息
            var pager_id = 'pager';
            if (opt.pager){
                pager_id = opt.pager;
            }
            var rowNum = $(this).jqGrid('getGridParam','records');
            $('#'+el_id+'_toppager_record').text(rowNum);
            $('#'+pager_id+' .ui-icon.ui-icon-seek-first').text('首页');
            $('#'+pager_id+' .ui-icon.ui-icon-seek-end').text('尾页');
            var head_cb_box = $('#jqgh_'+el_id+'_cb'),head_input_box = head_cb_box.children('input').eq(0);
            if ( head_cb_box.children('label.cb_label').length <= 0){
                head_input_box.after( '<label class="cb_label" for="'+ head_input_box.attr("id")+'"></label>');
            };
            $('td[aria-describedby="'+el_id+'_cb"]').append('<label class="cb_label"></label>');
            /**bottom page backgroundurl**/
            var page= $('#'+el_id).getGridParam('page'),lastpage = $('#'+el_id).getGridParam('lastpage'),
                prev_img='icon-seek-prev-dis170301',next_img='icon-seek-next-dis170301',first_color = 'first-dis',end_color = 'end-dis';
            if (page>1){
                prev_img = 'icon-seek-prev-active170301';
                first_color = 'first-active';
            };
            if (page<lastpage){
                next_img = 'icon-seek-next-active170301';
                end_color = 'end-active';
            };
            $('.ui-icon-seek-prev').attr('style','background-image:url("/static/resources/images/grid/'+prev_img+'.png")');
            $('.ui-icon-seek-next').attr('style','background-image:url("/static/resources/images/grid/'+next_img+'.png")');
            $('.ui-icon-seek-first').removeClass('first-dis').removeClass('first-active').addClass(first_color);
            $('.ui-icon-seek-end').removeClass('end-dis').removeClass('end-active').addClass(end_color);
        },
        onSelectRow:function(rowid,status){
          var idList=el.jqGrid('getGridParam','selarrrow');
          $('#'+el_id+'_toppager_choose').text(idList.length);
          if (opt.choosed && typeof opt.choosed == 'function'){
            opt.choosed(idList.length>0);
          }
        },
        onSelectAll:function(aRowids, status) {
          var idList=el.jqGrid('getGridParam','selarrrow');
          $('#'+el_id+'_toppager_choose').text(idList.length);
          if (opt.choosed && typeof opt.choosed == 'function'){
            opt.choosed(idList.length>0);
          }
        }
    };
    /**分页**/
    if (opt.ispaged){
        defaults['loadonce'] = false;
        defaults['jsonReader'] = {
            root: "d.items",
            page: "d.page",
            records: "d.records",
            total: "d.total"
        };
    }else{
        defaults['loadonce'] = true;
    }
    var settings = extend(defaults, opt);
    /**create top pager**/
    var element = document.createElement('div');
    var totalTitle = opt.totalTitle ? opt.totalTitle: '共计记录';
    var selectedTitle = opt.selectedTitle ? opt.selectedTitle: '已选记录';
    $(element).attr('id',el_id+'_toppager').html(
        '<p style="display:none;">'
            +'<span id="'+el_id+'_toppager_record_container">'+totalTitle+' <font id="'+el_id+'_toppager_record"></font></span>&nbsp;&nbsp;&nbsp;&nbsp;'
            +'<span id="'+el_id+'_toppager_choose_container" hidden="hidden">'+selectedTitle+' <font id="'+el_id+'_toppager_choose">0</font></span>'
        +'</p>'
    );
    el.before(element);
    el.jqGrid(settings)
}

function hascheckedrows(callback) {
    var rowIds = $("#grid").getGridParam("selarrrow");
    if (rowIds.length == 0) {
        layer.msg('未选择记录');
        return false
    }
    callback(rowIds);
    return true
}
function hascheckedonerow(callback) {
    var rowIds = $("#grid").getGridParam("selarrrow");
    if (rowIds.length != 1) {
        layer.msg('请选择一条记录');
        return false
    }
    callback(rowIds[0]);
    return true
}

/**管理员-修改密码**/
function setpwd(id){
    var rowObject = $('#grid').getLocalRow(id);
    if (!rowObject){
        rowObject =  $("#grid").getRowData(id);
    };
    name = rowObject.full_name;
    account_id=rowObject.account_id;
    layer.open({
        type: 1,
        area: ['380px', '240px'], //宽高
        title:'修改密码',
        content:
                '<div>'
                    +'<table class="table">'
                        +'<tr>'
                            +'<td>姓名</td>'
                            +'<td><input disabled="disabled" value="'+name+'"></td>'
                        +'</tr>'
                        +'<tr>'
                            +'<td>新密码</td>'
                            +'<td><input id="pwd" type="password"></td>'
                        +'</tr>'
                        +'<tr>'
                            +'<td>重复新密码</td>'
                            +'<td><input id="pwd2" type="password" onkeyup="pwdConfirm2()"></td>'
                        +'</tr>'
                    +'</table>'
                    +'<div id="tishi2" style="display:none;color:#ff0000;text-align: center;">两次密码不相同</div>'
                +'</div>',
        btn:['确定','取消'],
        btn1: function(index){
            if($.trim($('#pwd').val()) && $('#pwd').val()==$('#pwd2').val()){
                var data = {
                    "account_id": account_id,
                    "new_password": $("#pwd").val()
                };
                myajax({
                    aysnc: false,
                    url: '/api/reset/password',
                    data: data
                },function(data){
                    layer.close(index);
                    if(data.c == 0){
                        reloadGrid();
                        layer.msg('操作成功');
                    }
                })
            }else{
                layer.msg('密码为空或两次密码不相同');
            }
            return false;
        },
        cancel: function(index){
            layer.close(index);
            return false;
        }
    });
}
/**判断两次密码是否相同**/
function pwdConfirm2(){
    var pwd=$('#pwd').val();
    var pwd2=$('#pwd2').val();
    if(pwd!=pwd2){
         document.getElementById("tishi2").style.display='block';
         $('.layui-layer-btn1').attr('disabled', 'true');
    }else{
         document.getElementById("tishi2").style.display='none';
         $('.layui-layer-btn1').removeAttr('disabled');
    }
}
/**切换应用**/
function switchgApp(){
    url_go('/');
}

//上传头像
function importImg(){
    $("#upload").click(); //隐藏了input:file样式后，点击头像就可以本地上传
    $("#upload").on("change",function(){
       var objUrl = getObjectURL(this.files[0]) ;  //获取图片的路径，该路径不是图片在本地的路径
       if (objUrl) {
         $("#pic").attr("src", objUrl) ;      //将图片路径存入src中，显示出图片
         $('.add-img').css('display','none');
         $('#pic').css('display','block');
         var data = new FormData();
         //为FormData对象添加数据
         $.each($('#upload')[0].files, function(i, file) {
             data.append('image', file);
         });
           $("body").showLoading();
           //图片上传接口
           myajax({
                aysnc: true,
                url: '/api/upload/image',
                data: data,
                cache: false,
                contentType: false,//  不设置Content-type请求头
                processData: false //  不处理发送的数据，因为data值是Formdata对象，不需要对数据做处理
            },function(data){
                if(data.c == 0){
                    $('#image_url').attr('value',data.d[0].url);
                };
               $("body").hideLoading();
            });
       }
    });
}

//建立一个可存取到该file的url
function getObjectURL(file) {
  var url = null ;
  if (window.createObjectURL!=undefined) { // basic
    url = window.createObjectURL(file) ;
  } else if (window.URL!=undefined) { // mozilla(firefox)
    url = window.URL.createObjectURL(file) ;
  } else if (window.webkitURL!=undefined) { // webkit or chrome
    url = window.webkitURL.createObjectURL(file) ;
  }
  return url ;
}

//修改头像
function changeImg(){
    layer.open({
        title: false,
        content : '<button class="hx-margin20-r" style="width:100px;" onclick="layer.closeAll()">取消</button>' +
                    '<button style="width:100px;" onclick="javascript:importImg();layer.closeAll()">更换头像</button>',
        btn: false
    });

}

//阿拉伯数字转中文数字
function convert_num_to_ch(num){
    ch_num_list = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
    if (num >=0 && num <=9){
        return ch_num_list[num];
    } else {
        return num;
    }
}

