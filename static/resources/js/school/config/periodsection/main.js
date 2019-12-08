/**
 * Created by jie on 2017/3/27.
 */

$(document).ready(function(){
    myajax({
        url:'/api/detail/school',
        data:'',
        async:false,
        success:function(data){
            var primary=data.d[0].primary_years;
            if(primary!=0){
                $('#priCheck').attr('checked', true);
                $('#priCh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-upper-checked.png">');
                if(primary==5){
                    $('#pri').val('五年制');
                    $('#priFive').attr('checked', true);
                    $('#priFi').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down-checked.png">');
                    $('#priSi').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down.png">');
                }
                if(primary==6){
                    $('#pri').val('六年制');
                    $('#priSix').attr('checked', true);
                    $('#priFi').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down.png">');
                    $('#priSi').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down-checked.png">');
                }
                $('#priDiv').show();
            }else if(primary==0){
                $('#priCheck').attr('checked',false);
                $('#priCh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-upper.png">');
                $('#priFi').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down.png">');
                $('#priSi').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down.png">');
            }
            var junior=data.d[0].junior_years;
            if(junior!=0){
                $('#junCheck').attr('checked', true);
                $('#junCh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-upper-checked.png">');
                if(junior==3){
                    $('#jun').val('三年制');
                    $('#junThree').attr('checked', true);
                    $('#junTh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down-checked.png">');
                    $('#junFo').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down.png">');
                }
                if(junior==4){
                    $('#jun').val('四年制');
                    $('#junFour').attr('checked', true);
                    $('#junTh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down.png">');
                    $('#junFo').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down-checked.png">');
                }
                $('#junDiv').show();
            }else if(junior==0){
                $('#junCheck').attr('checked',false);
                $('#junCh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-upper.png">');
                $('#junTh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down.png">');
                $('#junFo').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down.png">');
            }
            var senior=data.d[0].senior_years;
            if(senior!=0){
                $('#senCheck').attr('checked', true);
                $('#senCh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-upper-checked.png">');
                $('#sen').val('三年制');
                $('#senDiv').show();
            }else if(senior==0){
                $('#senCh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-upper.png">');
            }
        }
    });

    //点击事件
    $('#priCheck').click(function(){
        if($('#priCheck').is(':checked')){
            $('#priCh').children().remove();
            $('#priCh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-upper-checked.png">');
        }else{
            $('#priCh').children().remove();
            $('#priCh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-upper.png">');
        }
    });
    $('#junCheck').click(function(){
        if($('#junCheck').is(':checked')){
            $('#junCh').children().remove();
            $('#junCh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-upper-checked.png">');
        }else{
            $('#junCh').children().remove();
            $('#junCh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-upper.png">');
        }
    });
    $('#senCheck').click(function(){
        if($('#senCheck').is(':checked')){
            $('#senCh').children().remove();
            $('#senCh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-upper-checked.png">');
        }else{
            $('#senCh').children().remove();
            $('#senCh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-upper.png">');
        }
    });

    //学制互斥
    $('#priFive').click(function(){
        if($('#priFive').is(':checked')) {
            $('#priFi').children().remove();
            $('#priFi').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down-checked.png">');
            $('#priSix').attr('checked', false);
            $('#priSi').children().remove();
            $('#priSi').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down.png">');
        }else{
            $('#priFi').children().remove();
            $('#priFi').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down.png">');
        }
    });
    $('#priSix').click(function(){
        if($('#priSix').is(':checked')) {
            $('#priSi').children().remove();
            $('#priSi').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down-checked.png">');
            $('#priFive').attr('checked', false);
            $('#priFi').children().remove();
            $('#priFi').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down.png">');
        }else{
            $('#priSi').children().remove();
            $('#priSi').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down.png">');
        }
    });
    $('#junThree').click(function(){
        if($('#junThree').is(':checked')) {
            $('#junTh').children().remove();
            $('#junTh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down-checked.png">');
            $('#junFour').attr('checked', false);
            $('#junFo').children().remove();
            $('#junFo').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down.png">');
        }else{
            $('#junTh').children().remove();
            $('#junTh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down.png">');
        }
    });
    $('#junFour').click(function(){
        if($('#junFour').is(':checked')) {
            $('#junFo').children().remove();
            $('#junFo').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down-checked.png">');
            $('#junThree').attr('checked', false);
            $('#junTh').children().remove();
            $('#junTh').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down.png">');
        }else{
            $('#junFo').children().remove();
            $('#junFo').append('<img class="imgClass" src="/static/resources/images/icon/checkbox-down.png">');
        }
    });
});

function test(){
    $('#norm').hide();
    $('#choos').show();
}

function keepIt(){
    var primary=0,junior=0,senior=0;

    //小学被勾选
    if($('#priCheck').is(':checked') && $('#priFive').is(':checked')){
        primary=5;
    }
    else if($('#priCheck').is(':checked') && $('#priSix').is(':checked')){
        primary=6;
    }
    else{
        layer.msg('已勾选信息不足')
    }
    //初中被勾选
    if($('#junCheck').is(':checked') && $('#junThree').is(':checked')){
        junior=3;
    }
    else if($('#junCheck').is(':checked') && $('#junFour').is(':checked')){
        junior=4;
    }
    else{
        layer.msg('已勾选信息不足')
    }
    //高中被勾选
    if($('#senCheck').is(':checked')){
        senior=3;
    }
    var data={
        primary_years:primary,
        junior_years:junior,
        senior_years:senior
    };
    myajax({
        url:'/api/update/learning_period',
        data:data,
        async:false,
        success:function(data){
            if(data.c!=0) {
                layer.msg(data.m);
            }else{
                location.reload();
            }
        }
    })
}

function cancelIt(){
    $('#norm').show();
    $('#choos').hide();
}