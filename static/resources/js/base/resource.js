/**
 * Created by jie on 2016/10/27.
 */


/*
在此添加或组织全局变量
*/
Vue.config.delimiters = ["{$", "$}"];
var CONST = {
    'K12': [
        {"grade_num": 1, "grade_name":"一年级"},
        {"grade_num": 2, "grade_name":"二年级"},
        {"grade_num": 3, "grade_name":"三年级"},
        {"grade_num": 4, "grade_name":"四年级"},
        {"grade_num": 5, "grade_name":"五年级"},
        {"grade_num": 6, "grade_name":"六年级"},
        {"grade_num": 7, "grade_name":"七年级"},
        {"grade_num": 8, "grade_name":"八年级"},
        {"grade_num": 9, "grade_name":"九年级"},
        {"grade_num": 10, "grade_name":"高一"},
        {"grade_num": 11, "grade_name":"高二"},
        {"grade_num": 12, "grade_name":"高三"}
    ]
},
CONST_ARR = {
    KIND_LIST: ['正常','借读','保籍',/*'毕业',*/'转校','休学','退学'],
    TEACHER_KIND_LIST: ['正式','非正式']
};

/*
在此图片添加路径常量
*/
var ICON = {
    VIEW : "/static/resources/images/icon/icon-view-dis.png",  //查看
    SETMANAGER: "/static/resources/images/icon/icon-setmanager-dis.png", //配置管理员
    SETPWD:"/static/resources/images/icon/icon-setpwd-dis.png",//修改密码
    PHOTO_DEFAULT: "/static/resources/images/icon/photo-default.png", //默认头像
}
/*
操作提示
*/
var TIPS = {
    VIEW: "查看",
    SETMANAGER: "设置管理员",
    SETPWD:"修改密码",
    REMOVE : "删除"
}

function getclassById(class_id){
    var class_list = HX_CACHE.CLASS_LIST;
    for (var i in class_list){
        if(class_list[i].id == class_id){
            return class_list[i];
        }
    }
    return {};
}

function getgradeById(grade_id){
    var grade_list = HX_CACHE.GRADE_LIST;
    for (var i in grade_list){
        if(grade_list[i].id == grade_id){
            return grade_list[i];
        }
    }
    return {};
}
