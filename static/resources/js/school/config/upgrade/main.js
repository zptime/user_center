/**
 * Created by jie on 2017/3/27.
 */

var vm= new Vue({
    el: '#content',
    data: {
        current_term: '',
        month: '01',
        day: '01',
        month_list: ['01','02','03','04','05','06','07','08','09','10','11','12'],
        day_list_28: ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28'],
        day_list_30: ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30'],
        day_list_31: ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'],
    },
    computed: {
        c_day_list: function(){
            var str_31 = ',01,03,05,07,08,10,12,',str_30 = ',04,06,09,11,',str_28 = ',02,';
            if (str_31.indexOf(','+this.month+',')>=0){
                return this.day_list_31;
            }else if (str_30.indexOf(','+this.month+',')>=0){
                return this.day_list_30;
            }else if (str_28.indexOf(','+this.month+',')>=0){
                return this.day_list_28;
            }else{
                return [];
            }
        }
    },
    methods: {

    }
});

$(document).ready(function(){
    get_current_term(); //获取当前年度
    get_update_time(); //获取默认升级日期
});

//获取当前年度
function get_current_term(){
    myajax({
        url: '/api/display/current_term'
    }, function (data) {
        if(data.c == 0){
            vm.current_term = data.d;
        }
    });
}

//获取默认升级日期
function get_update_time(){
    myajax({
        url: '/api/display/update_time'
    }, function (data) {
        if(data.c == 0){
            if (data.d.month){
                vm.month = formatnumber(data.d.month);
            }
            if (data.d.day){
                vm.day = formatnumber(data.d.day);
            }
        }
    });
}

//升年级
function upgrade(){
    layer.confirm('确认升年级吗?', {
           icon: 3,
           title: '提示',
           btn:['确定','取消'],
           btn1: function (index) {
                layer.close(index);
                $('body').showLoading();
                myajax({
                    url: '/api/annually_update/grade'
                }, function (data) {
                    $('body').hideLoading();
                    if (data.c==0){
                        HX_CACHE.refresh();
                        //获取当前年度
                        myajax({
                            url: '/api/display/current_term'
                        }, function (data) {
                            if(data.c == 0){
                                vm.current_term = data.d;
                            }
                        });
                        layer.msg('操作成功');
                    }
                })
           },
           cancel: function(index){
               layer.close(index);
           }
    });

}

//回退
function upgrade_back(){
    layer.confirm('确认回退升年级吗?', {
           icon: 3,
           title: '提示',
           btn:['确定','取消'],
           btn1: function (index) {
                layer.close(index);
                $('body').showLoading();
                myajax({
                    url: '/api/undo_update/grade'
                }, function (data) {
                    $('body').hideLoading();
                    if (data.c==0){
                        HX_CACHE.refresh();
                        //获取当前年度
                        myajax({
                            url: '/api/display/current_term'
                        }, function (data) {
                            if(data.c == 0){
                                vm.current_term = data.d;
                            }
                        });
                        layer.msg('操作成功');
                    }
                });
           },
           cancel: function(index){
               layer.close(index);
           }
    });
}

//保存
function save(){
    $('body').showLoading();
    myajax({
        url: '/api/config/update_time',
        data: {
            "month": $('#month').val(),
            "day": $('#day').val()
        },
    },function(data){
        $('body').hideLoading();
        if (data.c == 0){
            layer.msg('操作成功',{
                time: 3000,
            },function(){
                window.location.reload();
            })
        }
    });
}

