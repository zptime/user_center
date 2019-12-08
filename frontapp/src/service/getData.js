import fetch from '../config/fetch'
import {uploadBlobImageInner,uploadFileInner,} from './utils.js'

/**
 *测试登录
**/
export const testLogin = (username,password) => fetch('/api/login',{
  username: username,
  password: password,
},'POST');



//POST /api/detail/account
//获取用户信息
export const accountDetail = (username) => fetch('/api/detail/account',{
  username: username ? username:'',
},'POST');


//获取用户应用列表（微信）
//GET /api/wx/service/list
export const wxServiceList = () => fetch('/api/wx/service/list',{

},'GET');


/**
 *发送老师绑定短信(微信)
 * */
export const wxSendTeacherCode = (mobile) => fetch('/api/wx/send/teacherbind/messagecode',{
  mobile:mobile,
},'GET');


/**
 *发送老师绑定短信(微信)
 * */
export const wxSendParentCode = (mobile) => fetch('/api/wx/send/parentbind/messagecode',{
  mobile:mobile,
},'GET');


/**
 *家长绑定微信，同时可添加绑定孩子(微信)
 * */
export const wxBindParent = (mobile,fullname,sex,address,student_list_json,messagecode,openid,sid,only_check) => fetch('/api/wx/bind/parent',{
  mobile:mobile,
  fullname:fullname,
  sex:sex,
  address:address,
  student_list_json:student_list_json,
  messagecode:messagecode,
  openid:openid,
  sid:sid,
  only_check:only_check,//当传入1时，只做业务校验，不真正办理提交业务，同时不验证验证码
},'POST');


/**
 *老师绑定微信，同时可添加家长绑定孩子(微信)
 * */
export const wxBindTeacher = (mobile,address,student_list_json,messagecode,openid,sid,only_check) => fetch('/api/wx/bind/teacher',{
  mobile:mobile,
  address:address,
  student_list_json:student_list_json,
  messagecode:messagecode,
  openid:openid,
  sid:sid,
  only_check:only_check,//当传入1时，只做业务校验，不真正办理提交业务，同时不验证验证码
},'POST');

/*
* 获取学校的所有年级
*
 POST /api/list/grade
* */
export const getSchoolGrades = () => fetch('/api/list/grade',{

},'POST');

/*
* 获取教师的班级信息（包含授课和不授课的）
* */
export const getSchoolClasses = (grade_num,teach_class) => fetch('/api/list/class',{
  grade_num:grade_num,
  teach_class:teach_class
},'POST');

/*
* POST /api/add/teacher_class
* 添加老师和教授班级
* */
export const addTeacherClass = (class_id_list) => fetch('/api/add/teacher_class',{
  class_id_list:class_id_list
},'POST');


/*
 POST /api/delete/teacher_class
* 删除老师和教授班级
* */
export const deleteTeacherClass = (class_id_list) => fetch('/api/delete/teacher_class',{
  class_id_list:class_id_list
},'POST');
/*
* 用户角色列表
* */
export const getUserTypeList = () => fetch('/api/list/user_type',{

},'POST');

/*
* 个人中心
 */


/*
* 添加用户
* */
export const addUserType = () => fetch('/api/list/user_type',{

},'POST');

/*
* 切换身份
* */
export const switchPerson = (school_id,type_id) => fetch('/api/change/user_type',{
  school_id:school_id,
  type_id:type_id
},'POST');

/*
* 查询教师信息
* */
export const getDetaiInfor = (teacher_id,account_id) => fetch('/api/detail/teacher',{
  teacher_id:teacher_id,
  account_id:account_id
},'POST');

/*
* 查询家长信息
* */
export const getParentDetaiInfor = (parent_id,account_id) => fetch('/api/detail/parent',{
  parent_id:parent_id,
  account_id:account_id
},'POST');

/*
* 修改家长信息/api/wx/add/child_by_parent
* */
export const updateParentInfo = (account_id,parent_info) => fetch('/api/update/parent',{
  account_id:account_id,
  parent_info:parent_info,
},'POST');

/*
* 家长添加孩子
* */
export const addChildByParent = (student_list_json) => fetch('/api/wx/add/child_by_parent',{
  student_list_json:student_list_json,
},'POST');

/*
* 家长获取家庭成员
* */
export const familyMember = () => fetch('/api/list/parent_student',{

},'POST');


/*
* 修改教师信息
* */
export const updateTeacherInfo = ( account_id,teacher_info ) => fetch('/api/update/teacher',{
  account_id:account_id,
  teacher_info:teacher_info,
},'POST');


/*
* 获取家庭邀请二维码
* */
export const getQrcode = ( account_id,teacher_info ) => fetch('/api/update/teacher',{
  account_id:account_id,
  teacher_info:teacher_info,
},'POST');



/*
* 间接获取所授科目
* */
export const getTeachSub = () => fetch('/api/list/teacher_textbook',{

},'POST');

/*
* 获取我的空间链接主域名
* */
export const getDomain = () => fetch('/api/wx/service/domain',{
  app_code:'interact',
},'GET');




/*
* 获取家长邀请二维码
* */
export const parentQrcode = (parent_id) => fetch('/api/wx/parent/qrcode',{
  parent_id:parent_id,
},'GET');


/*
* 邀请家长注册
* POST /api/list/teacher_class
* */
export const InviteParent = (parent_id,mobile,fullname,sex,address,messagecode,openid,relation) => fetch('/api/wx/invite/parent',{
  parent_id:parent_id,
  mobile:mobile,
  fullname:fullname,
  sex:sex,
  address:address,
  messagecode:messagecode,
  openid:openid,
  relation:relation,
},'POST');


/*
* 获取教师的班级信息（包含授课的）
* POST /api/list/teacher_class
* */
export const getMyClasses = (teacher_id) => fetch('/api/list/teacher_class',{
  teacher_id:teacher_id
},'POST');



/*
* 获取学校详情
* POST /api/detail/school
* */
export const getSchoolDetail = () => fetch('/api/detail/school',{
},'POST');

///api/wx/class/qrcode
//获取班级二维码
export const getClassQrcode = (class_id) => fetch('/api/wx/class/qrcode',{
  class_id:class_id
},'get');


/**
 *获取微信元数据
 **/
export const query_WeiXin_metaData = (sid,url) => fetch('/wx/get/jsconfig',{
  sid:sid,
  url:url,
},'POST');


//获取学校二维码
export const getSchoolQrcode = (sid) => fetch('/api/wx/school/qrcode',{
  sid:sid
},'get');

/**
 * 上传二进制文件
 */
export const uploadBlobImage = (base64Str) => uploadBlobImageInner('/api/common/upload/image','image',base64Str,'POST');

/**
 * 上传文件流
 */
export const uploadFile = (fileObj) => uploadFileInner('/api/common/upload/file','file',fileObj,'POST');

/*
* 上传音频
* */

export const uploadVoice = (media_id,duration) => fetch('/api/common/wx/voice/fetch', {
  media_id:media_id,
  duration:duration,
},'POST');

/*
* 上传视频
* */
export const uploadVideo = (videoObj) => uploadFileInner('/api/common/upload/video','video',videoObj,'POST');
