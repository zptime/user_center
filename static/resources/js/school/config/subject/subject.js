/**
 * Created by Xi Chen on 3/30/2017.
 */

var subList=[];

$(document).ready(function () {
//当前存在的课程

        myajax({
            url: '/api/school_list/subject',
            data: {}
        }, function (data) {
            var temp = data.d;
            for (var i = 0; i < temp.length; i++) {
                $('#subContainer').append('<li><div class="blueDiv" id="class' + i + '">' + temp[i].name + '</div></li>');
                subList.push(temp[i].id)
            }
        });

});


function setModal(){
    //所有课程
    $('#subAll').children().remove();
        myajax({
            url: '/api/admin_list/subject',
            data: '',
            async: false
            },function(data){
                var temp=data.d;
                var flag=1;
                for(var j=0;j<temp.length;j++) {
                    for(var i=0;i<subList.length;i++){
                        if(temp[j].id==subList[i]){
                            flag=0;
                            break;
                        }
                    }
                    if(flag==1){
                        $('#subAll').append('<div subId="'+temp[j].id+'" onclick="switchFun(this)" class="grayDiv" id="blue'+j+'">'+temp[j].name+'</div>');
                    }else{
                        $('#subAll').append('<div subId="'+temp[j].id+'" onclick="switchFun(this)" class="blueDiv" id="blue'+j+'">'+temp[j].name+'</div>');
                        flag=1;
                    }
                }
            });
    $('#norm').hide();
    $('#setSub').show();
    }

function switchFun(element){
    var subId;
    var temp=$(element).attr('class');

    if(temp=='grayDiv'){
        $(element).removeClass();
        $(element).addClass('blueDiv');
    }
    if(temp=='blueDiv'){
        subId=$(element).attr('subId');
        var data={
            subject_id:subId
        };
         myajax({
            aysnc: false,
            url: '/api/school_check/subject',
            data:data
            },function(data) {
                 if (data.d[0] == "False") {
                     $(element).removeClass();
                     $(element).addClass('grayDiv');
                     //layer.msg('操作成功');
                 } else if (data.d[0] == "True") {
                     layer.confirm('当前科目下存在有效教材，确认删除？', {
                         title: '提示',
                         btn: ['确定', '取消'],
                         btn1: function (index) {
                             $(element).removeClass();
                             $(element).addClass('grayDiv');
                             layer.close(index);
                         },
                         cancel: function (index) {
                             layer.close(index);
                         }
                     });
                 }
            }
         )
    }
}

function cancelIt(){
    location.reload();
}

function keepIt(){
    var tempList=[];
    $('#subAll').find('div').each(function(){
       if($(this).attr('class')=="blueDiv"){
            tempList.push($(this).attr('subId'));
       }
    });
    myajax({
            aysnc: false,
            url: '/api/school_update/subject',
            data: {
                subject_id_list:JSON.stringify(tempList)
            }
        },function(data){
            if(data.c == 0){
                layer.msg('添加科目成功');
                location.reload();
            }
    })
}
