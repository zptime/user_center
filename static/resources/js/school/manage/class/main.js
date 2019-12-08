/**
 * Created by jie on 2016/10/21.
 */


var vm= new Vue({
    el: '#content',
    data: {
        periodsection: '',
        classstyle: '',
        grade_list: HX_CACHE.get_grade_list(),
        class_list: HX_CACHE.get_class_list(),
        graduate_list: [],
        class_graduate_switch : 'CLASS',
        grade_num: '',
        class_id: '',
        manager_list: [],
        year_list: HX_CACHE.YEAR_LIST ,
        school: {

        }
    },
    computed: {

    },
    methods: {
        cancel_choose: function(index){
            if (index>=0 && index<vm.manager_list.length){
                this.manager_list.splice(index,1);
            }
        },
    }
});

$(document).ready(function(){
    get_periodsection();  //初始化学段学制
    get_classstyle();  //初始当前班级样式

    //批量新增班级modal
    $('#modal-add-bt-class .class-num').on('focus', function () {
        $(this).css('border-bottom','1px solid #308ce3');
    });
    $('#modal-add-bt-class .class-num').on('blur', function () {
        if (!$(this).val()){
            $(this).css('border-bottom','1px solid #ccc');
        }
    });

});

/**获取学段学制**/
function get_periodsection(){
    myajax({
        url: '/api/detail/school',
        data:{

        }
    }, function (data) {
        if (data.c==0){
            vm.school = data.d[0];
            if (data.d){//设置学段学制
                var school_detail = data.d[0];
                var primary_years = school_detail.primary_years;
                var junior_years = school_detail.junior_years;
                var senior_years = school_detail.senior_years;
                var period_str = "";
                if (primary_years > 0)
                    period_str += "小学" + convert_num_to_ch(primary_years) + "年制、";
                if (junior_years > 0)
                    period_str += "初中" + convert_num_to_ch(junior_years) + "年制、";
                if (senior_years > 0)
                    period_str += "高中"+ convert_num_to_ch(senior_years) + "年制、";
                period_str = period_str.substring(0, period_str.length-1);
                vm.periodsection = period_str;
            }
        }
    });
}

/**获取班级样式**/
function get_classstyle(){
    myajax({
        url: '/api/detail/class_style',
        data:{

        }
    }, function (data) {
        if (data.c==0){
            if (data.d){//设置班级样式
                var primary = data.d[0].primary;
                var junior = data.d[0].junior;
                var senior = data.d[0].senior;
                var style_str = "";
                if (!$.isEmptyObject(primary))
                    style_str += "小学（" + primary.style_example + "）、";
                if (!$.isEmptyObject(junior))
                    style_str += "初中（" + junior.style_example + "）、";
                if (!$.isEmptyObject(senior))
                    style_str += "高中（"+ senior.style_example + "）、";
                style_str = style_str.substring(0,style_str.length-1);
                vm.classstyle = style_str;
            }
        }
    });
}

/**获取班级列表**/
function get_classList(gradeNum){
    if (gradeNum >= 0){
        vm.grade_num = gradeNum;
    } else if (gradeNum == -1) {
        vm.grade_num = "";
    }
    vm.class_list = HX_CACHE.get_class_list()
}

/**刷新班级列表**/
function reloadclass(element) {
    vm.class_graduate_switch = 'CLASS';
    if (element){
        var grade_num = $(element).attr('grade');
        vm.grade_num = grade_num;
    }
    get_classList(grade_num);
}

/**获取毕业班列表**/
function get_graduateList(){
    vm.grade_num = 'GRADUATE';
    vm.class_graduate_switch = 'GRADUATE';
    myajax({
        url:'/api/list/graduated_class',
    }, function (data) {
        if (data.c==0){
            if (data.d.length > 0){//设置毕业班列表
                vm.graduate_list = _.groupBy(data.d, function(item){
                    return item.graduate_year;
                });
                $('.flik-timeline').css('display','block');
            }else{
                $('.flik-timeline').css('display','none');
            }
            init_timeline();
        }
    })
}

/**初始化时间轴插件**/
function init_timeline(){
    var flik_timeline_html = '';
    for (var year in vm.graduate_list){
        var data = vm.graduate_list[year];
        var li_html = '';
        li_html += '' +
            '<li class="event" data-date="'+year+'届">' +
                '<div class="card-box">';
                    var section_graduate_list = _.groupBy(data, function (item) {
                        return item.school_period;
                    });
                    for(var section in section_graduate_list){
                        var local_class_list = section_graduate_list[section];
                        li_html += '' +
                            '<div class="one-card">' +
                                    '<div class="card-title">' +
                                        (section==1?'小学·'+convert_num_to_ch(vm.school.primary_years)+'年制':
                                            (section==2?'初中·'+convert_num_to_ch(vm.school.junior_years)+'年制':
                                                (section==4?'高中·'+convert_num_to_ch(vm.school.senior_years)+'年制':'undefined'))) +
                                    '</div>'+
                                    '<div class="card-core">' +
                                        '<ul>';
                                            for (var num in local_class_list){
                                                var local_class = local_class_list[num];
                        li_html += ''+
                                                    '<li style="cursor:pointer;" onclick="view_student('+year+','+local_class.id+')">' +
                                                        '<div class="one-little-box">' +
                                                            '<div class="div-box">' +
                                                                '<img class="middle-img" src="/static/resources/images/icon/class-default.png">' +
                                                                '<div class="middle-context">' +
                                                                    '<div class="class-name">'+ local_class.class_name +'</div>' +
                                                                    '<div class="class-num">'+ local_class.student_amount +'人</div>' +
                                                                '</div>' +
                                                            '</div>' +
                                                        '</div>' +
                                                    '</li>';
                                            }
                        li_html += ''+
                                        '</ul>' +
                                    '</div>' +
                            '</div>';
                    }
        li_html += '' +
                '</div>' +
            '</li>';
        flik_timeline_html += li_html;
    };
    $('.flik-timeline').html(flik_timeline_html);
    $('.flik-timeline').flikScrollEffect();
}
//查看毕业班学生名单
function view_student(graduate_year, class_id){
    url_go('/index?nav=manage&view=student&graduate_year='+graduate_year+'&class_id='+class_id)
}

//批量新增班级
function add_bt(element){
    if (!element){
        layer.msg('请选择年级');
        return;
    }
    var grade_id = $(element).attr('grade-id');
    var gradeObj = getgradeById(grade_id);
    var grade_name = gradeObj.grade_name;
    layer.open({
        type: 1,
        title: '批量添加班级',
        area: ['550px','330px'],
        content : $('#modal-add-bt-class'),
        btn:['确定','取消'],
        btn1: function(index){
            var data = {
                "grade_id": grade_id,
                "class_count": $("#class_count").val()
            };
            myajax({
                aysnc: false,
                url: '/api/add/grade_class',
                data: data
            },function(data){
                set_HX_CACHE();
                reloadclass(); //兼容部分成功
                if(data.c == 0){
                    layer.close(index);
                    layer.msg('操作成功');
                }
            })
        },
        cancel: function(index){
            layer.close(index);
        }
    });
    $('#modal-add-bt-class .grade-name-content').html(grade_name);
}

//新增班级
function add(element){
    if (!element){
        layer.msg('请选择年级');
        return;
    }
    var grade_id = $(element).attr('grade-id');
    var gradeObj = getgradeById(grade_id);
    var grade_name = gradeObj.grade_name;
    var next_seq = gradeObj.class_amount+1;
    layer.open({
        type: 1,
        title: '添加班级',
        area: ['550px','330px'],
        content : $('#modal-add-class'),
        btn:['确定','取消'],
        btn1: function(index){
            var data = {
                "grade_id": grade_id,
                //"class_alias": grade_name+next_seq+'班'
            };
            myajax({
                aysnc: false,
                url: '/api/add/class',
                data:  data
            },function(data){
                if(data.c == 0){
                    set_HX_CACHE();
                    reloadclass();
                    layer.close(index);
                    layer.msg('操作成功');
                }
            })
        },
        cancel: function(index){
            layer.close(index);
        }
    });
    $('#modal-add-class .grade-content').html('确定新增'+grade_name+next_seq+'班吗？')
}

//修改班级
function edit(element){
    if (!element){
        layer.msg('请选择班级');
        return;
    }
    var class_id = $(element).attr('class-id');
    var classObj = getclassById(class_id);
    if (classObj){
        $("#class_alias_edit").val(classObj.class_alias);
    }
    layer.open({
        type: 1,
        title: '编辑班级别名',
        area: ['550px','330px'],
        content : $('#modal-edit-class'),
        btn:['确定','取消'],
        btn1: function(index){
            var data = {
                "class_id": class_id,
                "class_alias": $("#class_alias_edit").val()
            };
            myajax({
                aysnc: false,
                url: '/api/update/class',
                data:  data
            },function(data){
                if(data.c == 0){
                    set_HX_CACHE();
                    reloadclass();
                    layer.close(index);
                    layer.msg('操作成功');
                }
            })
        },
        cancel: function(index){
            layer.close(index);
        }
    });
}

//删除
function del(element){
    if (!element){
        layer.msg('请选择班级');
        return;
    }
    var class_id = $(element).attr('class-id');
    var ids = [class_id];
    layer.confirm('确认删除选中记录吗?', {
           icon: 3,
           title: '提示',
           btn:['确定','取消'],
           btn1: function (index) {
                layer.close(index);
                myajax({
                    aysnc: false,
                    url: '/api/delete/class',
                    data: {
                        id_list: JSON.stringify(ids)
                    }
                },function(data){
                    set_HX_CACHE();
                    reloadclass();
                    if(data.c == 0){
                        layer.msg('删除成功');
                    }
                })
           },
           cancel: function(index){
               layer.close(index);
           }
    });
};

/**设置班主任**/
function setmanager(element){
    if (!element){
        layer.msg('请选择班级');
        return;
    }
    var class_id = $(element).attr('class-id');
    var classObj = getclassById(class_id);
    var prev_teacher_list= [];
    if (classObj){
        prev_teacher_list = classObj.teacher_data;
    }
    $.chooseUser({
        title: '选择班主任',
        origin_user_list: prev_teacher_list,
        confirm: function ( data ) {
            var ids = [];
            for(var i=0;i<data.length; i++){
                ids.push(data[i].id);
            }
            setmanager_callback(class_id, ids);
        }
    });
};

function setmanager_callback(class_id,teacher_ids){//回调
    myajax({
        url: '/api/update/class',
        data: {
            class_id: class_id,
            teacher_ids: JSON.stringify(teacher_ids)
        }
    }, function (data) {
        if(data.c == 0){
            set_HX_CACHE();
            reloadclass();
            layer.msg('操作成功');
        }
    })
}

//获取入学年份options字符串
function get_year_listStr(){
    var res = '';
    var year_list = HX_CACHE.YEAR_LIST;
    for (var i in year_list){
        res += '<option value="'+year_list[i]+'">'+year_list[i]+'级</option>'
    }
    return res;
}

//清除缓存
function set_HX_CACHE(){
    HX_CACHE.refresh();
}
