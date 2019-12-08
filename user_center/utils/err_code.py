#!/usr/bin/python
# -*- coding=utf-8 -*-

ERR_SUCCESS = [0, u'完成']
ERR_FAIL = [40001, u'操作失败']
ERR_LOGIN_FAIL = [40003, u'用户名或密码错误']
ERR_USER_NOTLOGGED = [40004, u'用户未登录']
ERR_USER_AUTH = [40005, u'用户权限不够']
ERR_REQUESTWAY = [40006, u'请求方式错误']
ERR_USER_INFO_INCOMPLETE = [40007, u'用户信息不完整']
ERR_FILE_FORMAT_NOT_SUPPORTED = [40008, u'文件格式不支持']
ERR_INTERNAL_ERROR = [40009, u'服务器内部错误']
ERR_USER_ALREADY_EXIST = [40010, u'用户已经存在']
ERR_CLASS_NOT_EXIST = [40011, u'班级不存在']
ERR_USER_NOT_EXIST = [40012, u'用户不存在']
ERR_FILE_TEMPLATE_ERROR = [40013, u'导入模板不正确']
ERR_IMPORT_DATA_ERROR = [40014, u'部分数据导入失败']
ERR_IMPORT_NUM_ERROR = [40015, u'数据导入数量过多']

ERR_USER_NAME_CONFLICT_ERROR = [40017, u'用户名冲突']
ERR_USER_MOBILE_CONFLICT_ERROR = [40018, u'用户手机号冲突']
ERR_USER_CODE_CONFLICT_ERROR = [40019, u'用户学籍号冲突']
ERR_USER_TMP_CODE_CONFLICT_ERROR = [40020, u'用户临时学籍号冲突']
ERR_USER_ID_CARD_CONFLICT_ERROR = [40021, u'用户身份证号冲突']
ERR_USER_EMAIL_CONFLICT_ERROR = [40022, u'用户email冲突']
ERR_USER_PASSWORD_NOT_EXIST_ERROR = [40024, u'用户没有设置密码']
ERR_PARENT_CHILDREN_INFO_INCOMPLETE = [40025, u'家长信息中的学生信息不正确']
ERR_USER_INFO_IMAGE_NOT_EXIST = [40026, u'用户信息中的图片不存在']
ERR_OLD_PASSWORD_ERROR = [40027, u'原始密码不正确']
ERR_REQUEST_PARAMETER_ERROR = [40027, u'请求参数不正确']

ERR_USER_INFO_MULTI_LOGIN_NAME_ERROR = [40023, u'用户信息对应多个登录名']

ERR_USER_ID_CARD_ERROR = [40015, u'身份证格式不正确']
ERR_USER_STUDENT_CODE_ERROR = [40016, u'学籍号格式不正确']
ERR_USER_MOBILE_ERROR = [40023, u'用户手机号格式不正确']
ERR_USER_EMAIL_ERROR = [40023, u'用户邮箱格式不正确']
ERR_USER_USERNAME_ERROR = [40023, u'用户名格式不正确']
ERR_USER_ID_ERROR = [40023, u'用户ID格式不正确']

ERR_SCHOOL_ID_ERR = [40024, u"学校ID不正确"]
ERR_USER_TYPE_ERR = [40024, u"用户类型不正确"]
ERR_USER_TYPE_NOT_EXIST_ERROR = [40024, u"用户类型不存在"]

ERR_SYSTEM_ADMIN_NOT_DELETE_SELF_ERROR = [40024, u"系统管理员不能删除自己"]

ERR_STUDENT_KIND_NOT_MATCH_ERROR = [40024, u"学生类型和在读状态不匹配"]
ERR_PARENT_HAVE_EXIST_ERROR = [40070, u'家长关系已经建立或已发送过邀请']

ERR_DELETE_ERROR = [40039, u"删除失败"]
ERR_DELETE_PART = [40040, u"部分删除失败"]
ERR_OP_ERROR = [40039, u"操作失败"]
ERR_OP_PART_ERROR = [40040, u"部分操作失败"]
ERR_TIME_CONF = [40041, u"时间设置错误"]

ERR_MODEL_NAME_ERR = [40025, u"模块名称不存在"]
ERR_INTERFACE_NAME_ERR = [40025, u"接口不存在"]

ERR_TITLE_HAVE_EXIST_ERROR = [40050, u'职务已经存在']
ERR_TITLE_NOT_EXIST_ERROR = [40051, u'职务不存在']
ERR_TITLE_HAVE_TEACHER_ERROR = [40052, u'有教师属于该职务']
ERR_SCHOOL_LEARNING_PERIOD_ERROR = [40053, u'学段学制设置错误']
ERR_SCHOOL_LEARNING_PERIOD_CLASS_ERROR = [40054, u'已经创建班级无法修改']
ERR_SCHOOL_LEARNING_LOW_ERROR = [40055, u'学段学制不能调低']
ERR_SCHOOL_NOT_INIT_ERROR = [40056, u'学校数据没有初始化']
ERR_TITLE_INTERNAL_ERROR = [40052, u'内部职务不允许操作']

ERR_GRADE_NOT_EXIST_ERROR = [40056, u'年级不存在']
ERR_CLASS_HAVE_EXIST_ERROR = [40056, u'班级已经存在']
ERR_CLASS_NO_STYLE_ERROR = [40056, u'班级名称样式没有设置']
ERR_TEAM_NOT_EXIST_ERROR = [40056, u'学校学期不存在']
ERR_HAVE_UPGRADE_TERM_ERROR = [40056, u'已升级学年，无法升级']
ERR_CANNOT_DEGRADE_TERM_ERROR = [40056, u'没有升学年，无法回退']
ERR_HAVE_FIRST_GRADE_CLASS_TERM_ERROR = [40056, u'有一年级/初一/高一班级，无法回退']
ERR_CLASS_GRADE_NUM_TOO_LARGE_ERROR = [40056, u'班级数据超过了年制限制']
ERR_CANNOT_OP_TERM_ERROR = [40056, u'无法操作学年']
ERR_TEACHER_CLASS_MASTER_DELETE_ERROR = [40057, u"您为该班级班主任，请联系学校管理中心管理员删除"]

ERR_CLASS_CODE_ERROR = [40057, u'班级码不正确']
ERR_VERIFY_CODE_ERROR = [40057, u'校验码不正确']
ERR_SUBJECT_HAVE_EXIST_ERROR = [40060, u'科目已经存在']
ERR_SUBJECT_ID_ERROR = [40061, u'科目ID不正确']
ERR_SUBJECT_GRADE_NUM_ERROR = [40062, u'科目的年级设置不正确']
ERR_TEXTBOOK_HAVE_EXIST_ERROR = [40063, u'教材已经存在']
ERR_TEXTBOOK_ID_ERROR = [40064, u'教材ID不正确']
ERR_CHAPTER_ID_ERROR = [40065, u'章节ID不正确']

# 验证码
ERR_VERIFY_CODE_NOT_NULL = [40081, u"手机号/验证码不能为空"]
ERR_VERIFY_CODE_USER_NOT_EXIST = [40082, u"用户不存在，请输入正确手机号"]
ERR_VERIFY_CODE_USER_EXIST = [40083, u"该手机号已经注册，请更换其它手机号"]

# 第三方应用
ERR_SP_SCHOOL_NOT_EXIST = [40091, u"用户所在学校没有开通该应用"]
ERR_SP_USER_NOT_EXIST = [40091, u"用户没有权限访问该应用"]
ERR_SP_USER_NOT_COMPLETE_INFO = [40093, u"用户信息不完整，没有权限访问该应用"]
ERR_SP_AUTH_UC_ERROR = [40093, u"用户认证失败"]

# 微信相关
ERR_GET_ACCESS_TOKEN = [40101, u"获取微信accesstoken失败！"]
ERR_GET_APPID = [40102, u"获取微信APPID失败！请检查是否post传入学校信息！"]
ERR_GET_PARAM_URL = [40103, u"获取URL参数失败！"]
ERR_GET_ACCOUNT_BYMOB = [40104, u"您所填写的信息与向学校提供的已有信息不一致，请核对后重新填写！"]
ERR_GET_TEACHER_BYMOB = [40105, u"您所填写的信息与向学校提供的已有信息不一致，请核对后重新填写！"]
ERR_USER_IS_BIND = [40106, u"该用户已经绑定了微信，不能再次绑定！"]
ERR_GET_STUDENT = [40107, u"孩子姓名与孩子的学号不匹配，请核实后再进行填写！"]
ERR_MESSAGECODE = [40108, u"验证码校验失败！"]
ERR_OPENID_IS_BIND = [40109, u"该微信已经绑定了用户，不能再次绑定！"]
ERR_VERIFY_CODE_TELISBIND = [40110, u"该手机号已经绑定了微信，请核对资料是否正确"]
ERR_VERIFY_CODE_SEND_MAX = [40111, u"验证码发送次数过多，请稍后再试"]
ERR_GET_PARENT_BYMOB = [40112, u"您所填写的信息与向学校提供的已有信息不一致，请核对后重新填写！"]
ERR_WX_ADD_PARENT = [40113, u"添加家长失败！"]
ERR_WX_USE_PARENT_ADD_STUDENT = [40114, u"请使用家长身份添加孩子！"]
ERR_WX_USE_PARENT = [40115, u"仅家长身份允许操作！"]
ERR_PARENT_NULL = [40116, u"没对查询到家长信息！"]
ERR_ONLYCHECK_OK = [0, u"业务检查成功！"]  # 此处用于做业务检查


def getDictResp(err_array):
    dictResp = {'c': err_array[0], 'e': err_array[1]}
    return dictResp
