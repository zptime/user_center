/**
 * Created by jie on 2017/3/27.
 */

var vm= new Vue({
    el: '#content',
    data: {
        section: {
            primary: '小学',
            junior: '初中',
            senior: '高中'
        },
        class_style: {
            primary: [
                /*{id: 1, style_example: '', school_period: 1},
                {id: 2, style_example: '', school_period: 1},
                {id: 3, style_example: '', school_period: 1}*/
            ],
            junior: [

            ],
            senior: [

            ]
        },
        current_style: {
            primary: {/*id: 1, style_example: '', school_period: 1*/},
            junior: { },
            senior: { }
        },
        form: {
            styleID: {
                primary: '',
                junior: '',
                senior: ''
            }
        }
    },
    computed: {

    },
    methods: {
        get_section_name: function (section) {
            var res = '';
            if (section){
                switch (section){
                    case 'primary':
                        res = this.section.primary;
                        break;
                    case 'junior':
                        res = this.section.junior;
                        break;
                    case 'senior':
                        res = this.section.senior;
                        break;
                }
            }
            return res;
        },
    }
});

$(document).ready(function(){
    get_class_style();  //获取后台定义的班级样式模板
    get_current_style();  //获取当前班级样式值
});

//获取班级样式
function get_class_style(){
    myajax({
        url: '/api/list/class_style'
    }, function (data) {
        if(data.c == 0){
            extend(vm.class_style, data.d[0]);
        }
    });
}

//获取当前班级样式值
function get_current_style(){
    myajax({
        url: '/api/detail/class_style'
    }, function (data) {
        if(data.c == 0){
            extend(vm.current_style, data.d[0]);
            var obj = {}
            if (data.d[0].primary.id){
                obj['primary'] = data.d[0].primary.id;
            }
            if (data.d[0].junior.id){
                obj['junior'] = data.d[0].junior.id;
            }
            if (data.d[0].senior.id){
                obj['senior'] = data.d[0].senior.id;
            }
            extend(vm.form.styleID, obj);
        }
    });
}

//保存
function save(){
    myajax({
        url: '/api/update/class_style',
        data: {
            "primary_class_style_id": vm.form.styleID.primary,
            "junior_class_style_id": vm.form.styleID.junior,
            "senior_class_style_id": vm.form.styleID.senior
        }
    },function(data){
        if (data.c == 0){
            layer.msg('操作成功',{
                time: 3000,
            },function(){
                window.location.reload();
            })
        }
    });
}
