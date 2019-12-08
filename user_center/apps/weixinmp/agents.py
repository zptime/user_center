# coding=utf-8
import json
import logging

import cStringIO

import datetime

import copy
import urllib

import qrcode
import base64

import requests
import time
from django.conf import settings
from django.db import transaction

from user_center.apps.account.agents import __check_mobile_valid
from user_center.apps.account.models import Account
from user_center.apps.common.agents import verify_messagecode, send_message
from user_center.apps.common.models import VerifyCode
from user_center.apps.parent.agents import add_parent
from user_center.apps.parent.models import Parent, ParentStudent
from user_center.apps.school.models import Class
from user_center.apps.service.models import SchoolService, Service, Role, UserRole
from user_center.apps.student.models import Student
from user_center.apps.teacher.models import Teacher
from user_center.apps.weixinmp.models import WeixinAccount, WeixinSchool, WeixinService
from user_center.apps.weixinmp.sign import Sign
from user_center.utils.constant import FLAG_YES, FLAG_NO, USER_TYPE_STUDENT, USER_TYPE_TEACHER, USER_TYPE_PARENT, APPLICATION_STATUS_APPROVED
from user_center.utils.err_code import *
from user_center.utils.file_fun import get_timestr
from user_center.utils.public_fun import convert_id_to_code, get_timestamp, get_randstr, send_http_request
from user_center.utils.utils_except import BusinessException

logger = logging.getLogger(__name__)


def get_weixin_school(school_id, appid=None):
    # 返回weixin_school对象
    if not school_id and not appid:
        return None
    weixinschool = WeixinSchool.objects.filter(del_flag=FLAG_NO)
    if school_id:
        weixinschool = weixinschool.filter(school_id=school_id)

    if appid:
        weixinschool = weixinschool.filter(app_id=appid)

    weixinschool = weixinschool.first()

    # 检查必配字段
    if not weixinschool or not weixinschool.app_id or not weixinschool.app_secret or weixinschool.only_request_openid is None:
        raise Exception(u'微信学校缺少必配字段。')

    return weixinschool


def get_weixin_global_access_token(weixinschool):
    if not weixinschool:
        raise BusinessException(ERR_GET_APPID)
    now_time = datetime.datetime.now()
    # 如果accesstoken过期了则重新获取
    if not weixinschool.access_token or not weixinschool.access_token_update_time or \
            get_timestr(weixinschool.access_token_update_time) <= get_timestr(now_time):
        logger.info('weixin_global_access_token need update')
        update_weixin_global_access_token(weixinschool)
        weixinschool = get_weixin_school(weixinschool.school_id)
    cur_access_token = weixinschool.access_token
    return cur_access_token


def update_weixin_global_access_token(weixinschool):
    if not weixinschool:
        raise BusinessException(ERR_GET_APPID)
    global_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + weixinschool.app_id + '&secret=' + weixinschool.app_secret
    # globalaccesstokeninfo = requests.get(global_access_token_url).text
    globalaccesstokeninfo = send_http_request(url=global_access_token_url, method="GET")
    globalaccesstokeninfo = json.loads(globalaccesstokeninfo)
    now_time = datetime.datetime.now()

    if globalaccesstokeninfo.get('access_token'):
        weixinschool.access_token = globalaccesstokeninfo.get('access_token')
        weixinschool.access_token_update_time = now_time + datetime.timedelta(seconds=int(globalaccesstokeninfo.get('expires_in'))/2)
        weixinschool.save()
        # print settings.weixin_access_token_updatetime.strftime("%Y-%m-%d %H:%M:%S")
    else:
        # 获取accesstoken失败
        raise Exception(globalaccesstokeninfo)
    return globalaccesstokeninfo


def get_account_byopenid(openid, school_id):
    # 通过openid获取帐户信息
    weixinaccount = WeixinAccount.objects.filter(school_id=school_id, openid=openid, del_flag=FLAG_NO).first()
    if not weixinaccount:
        return None

    account = weixinaccount.account
    return account


def get_account_byfhopenid(fhopenid):
    # 通过fhopenid获取帐户信息
    weixinaccount = WeixinAccount.objects.filter(openid_fh=fhopenid, del_flag=FLAG_NO).first()
    if not weixinaccount:
        return None

    account = weixinaccount.account
    return account


def get_str_qrcode_base64(src_str):
    img = qrcode.make(src_str, border=1)
    fbuffer = cStringIO.StringIO()
    img.save(fbuffer)
    qrcode_base64 = base64.b64encode(fbuffer.getvalue())
    return qrcode_base64


def api_class_qrcode(class_id):
    # result = dict()
    if not class_id:
        raise BusinessException(ERR_REQUEST_PARAMETER_ERROR)

    cls = Class.objects.filter(id=class_id, del_flag=FLAG_NO).first()
    if not cls:
        raise BusinessException(ERR_CLASS_NOT_EXIST)

    classcode = convert_id_to_code(cls.id)
    classcode_base64 = get_str_qrcode_base64(classcode)

    result = {
        "base64_image": classcode_base64,
        "base64_html": r'<img src="data:image/gif;base64,' + classcode_base64 + '">',
    }
    return result


def get_weixin_jsapi_ticket(weixinschool):
    if not weixinschool:
        raise BusinessException(ERR_GET_APPID)
    now_time = datetime.datetime.now()
    # 如果accesstoken过期了则重新获取
    if not weixinschool.jsapi_ticket or not weixinschool.jsapi_ticket_update_time or \
            get_timestr(weixinschool.jsapi_ticket_update_time) <= get_timestr(now_time):
        logger.info('weixin_jsapi_ticket need update')
        update_weixin_jsapi_ticket(weixinschool)
        weixinschool = get_weixin_school(weixinschool.school_id)
    cur_jsapi_ticket = weixinschool.jsapi_ticket
    return cur_jsapi_ticket


def update_weixin_jsapi_ticket(weixinschool):
    if not weixinschool:
        raise BusinessException(ERR_GET_APPID)

    wx_access_token = get_weixin_global_access_token(weixinschool)

    jsapi_ticket_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=' + wx_access_token + '&type=jsapi'
    # jsapi_ticket_info = requests.get(jsapi_ticket_url).text
    jsapi_ticket_info = send_http_request(url=jsapi_ticket_url, method="GET")

    jsapi_ticket_info = json.loads(jsapi_ticket_info)
    now_time = datetime.datetime.now()

    if jsapi_ticket_info.get('ticket'):
        weixinschool.jsapi_ticket = jsapi_ticket_info.get('ticket')
        weixinschool.jsapi_ticket_update_time = now_time + datetime.timedelta(seconds=int(jsapi_ticket_info.get('expires_in'))/2)
        weixinschool.save()
        # print settings.weixin_access_token_updatetime.strftime("%Y-%m-%d %H:%M:%S")
    else:
        # 获取accesstoken失败
        raise Exception(jsapi_ticket_info)
    return jsapi_ticket_info


def wx_get_jsconfig(weixinschool, url):
    if not weixinschool:
        raise BusinessException(ERR_GET_APPID)

    if not url:
        raise BusinessException(ERR_GET_PARAM_URL)

    result = dict()

    ticket = get_weixin_jsapi_ticket(weixinschool)

    sign = Sign(ticket, url).sign()
    result['appid'] = weixinschool.app_id
    result['timestamp'] = sign['timestamp']
    result['noncestr'] = sign['nonceStr']
    result['signature'] = sign['signature']
    result['url'] = url
    result['debug_mod'] = settings.WEB_DEBUG_MOD  # 前端使用，用于动态开关前端调试信息。

    return result


def api_get_accountopenid(account_id_list, school_id):
    if not account_id_list or not school_id:
        raise BusinessException(ERR_REQUEST_PARAMETER_ERROR)

    result = list()
    account_id_list = account_id_list.strip(',').split(',')
    weixin_accounts = WeixinAccount.objects.filter(account_id__in=account_id_list, school_id=school_id, del_flag=FLAG_NO)
    for each_weixinaccount in weixin_accounts:
        rowdata = {
            'account_id': each_weixinaccount.account_id,
            'openid': each_weixinaccount.openid,
        }
        result.append(rowdata)
    return result


def bind_openid_schoolaccount(openid, account, school_id, check_user_bind):
    # 检查用户是否已经绑定
    weixin_account = WeixinAccount.objects.filter(account=account, school_id=school_id, del_flag=FLAG_NO)
    if check_user_bind and weixin_account:
        raise BusinessException(ERR_USER_IS_BIND)
    else:
        weixin_account.update(del_flag=FLAG_YES)

    # 检查openid是否已经绑定
    weixin_account = WeixinAccount.objects.filter(openid=openid, del_flag=FLAG_NO)
    if weixin_account:
        raise BusinessException(ERR_OPENID_IS_BIND)

    # 绑
    weixin_account_new = WeixinAccount()
    weixin_account_new.openid = openid
    weixin_account_new.account = account
    weixin_account_new.school_id = school_id
    weixin_account_new.save()
    return True


@transaction.atomic
def api_bind_teacher(openid, school_id, mobile, address, student_list_json, messagecode, check_user_bind=False, only_check=False):
    result = dict()
    if not openid or not school_id:
        raise BusinessException(ERR_REQUEST_PARAMETER_ERROR)

    # 检查手机验证码
    if not only_check:
        if not mobile:
            raise BusinessException(ERR_REQUEST_PARAMETER_ERROR)

        ret = verify_messagecode(mobile, code=messagecode, expire_time=600)
        if ret["c"] != ERR_SUCCESS[0]:
            raise BusinessException(ERR_MESSAGECODE)

    # 检查老师是否存在
    teacher_account = Account.objects.filter(mobile=mobile, del_flag=FLAG_NO).first()
    if not teacher_account:
        raise BusinessException(ERR_GET_ACCOUNT_BYMOB)

    teacher = Teacher.objects.filter(account=teacher_account, school_id=school_id, del_flag=FLAG_NO).first()
    if not teacher:
        raise BusinessException(ERR_GET_TEACHER_BYMOB)

    # 更新老师的地址
    if address:
        teacher.address = address
        teacher.save()

    # 检查用户是否已经绑定
    weixin_account = WeixinAccount.objects.filter(account=teacher_account, school_id=school_id, del_flag=FLAG_NO)
    if check_user_bind and weixin_account:
        raise BusinessException(ERR_USER_IS_BIND)
    else:
        weixin_account.update(del_flag=FLAG_YES)

    # 检查openid是否已经绑定
    weixin_account = WeixinAccount.objects.filter(openid=openid, del_flag=FLAG_NO)
    if weixin_account:
        raise BusinessException(ERR_OPENID_IS_BIND)

    # 检查学生信息，注意:按徐峻要求，性别当前未处理
    # student_list_json格式 [{"full_name":"张三", "code":"G20160145", "sex":"男", "relation":"父亲", }, {}]
    if student_list_json:
        student_list_json = json.loads(student_list_json)
        children = list()
        for each_student in student_list_json:
            full_name = each_student.get('full_name', "")
            code = each_student.get('code', "")
            sex = each_student.get('sex', "")
            relation = each_student.get('relation', "")
            cur_student = Student.objects.filter(full_name=full_name, account__code=code, is_in=FLAG_YES, is_available=FLAG_YES, del_flag=FLAG_NO).first()
            if not cur_student:
                logger.info(u"当前处理孩子 姓名：%s   学号：%s" % (full_name, code))
                raise BusinessException(ERR_GET_STUDENT)

            student_dict = {
                "student_id": cur_student.id,
                "relation": relation,
                "status": APPLICATION_STATUS_APPROVED[0]
            }
            children.append(student_dict)

        parent_info = {
            "mobile": mobile,
            "full_name": teacher.full_name,
            "children": children
        }
        ret = add_parent(teacher_account, parent_info)
        if ret["c"] != ERR_SUCCESS[0]:
            # raise BusinessException(ERR_MESSAGECODE)
            raise Exception(ret['m'])

    # 绑定用户及微信openid和account
    bind_openid_schoolaccount(openid, teacher_account, school_id, check_user_bind)

    # 如果只是检查，则此处直接抛出异常，使事务回退
    if only_check:
        raise BusinessException(ERR_ONLYCHECK_OK)
    return result


@transaction.atomic
def api_bind_parent(openid, school_id, class_id, mobile, address, fullname, parent_sex, student_list_json, messagecode, check_user_bind=False, only_check=False):
    result = dict()
    if not openid or not school_id or not student_list_json:
        raise BusinessException(ERR_REQUEST_PARAMETER_ERROR)

    # 检查手机验证码
    if not only_check:
        if not mobile:
            raise BusinessException(ERR_REQUEST_PARAMETER_ERROR)

        ret = verify_messagecode(mobile, code=messagecode, expire_time=600)
        if ret["c"] != ERR_SUCCESS[0]:
            raise BusinessException(ERR_MESSAGECODE)

    # 检查家长是否存在, 如果存在，则检查用户是否已经绑定微信
    parent_account = Account.objects.filter(mobile=mobile, del_flag=FLAG_NO).first()
    if parent_account:
        weixin_account = WeixinAccount.objects.filter(account=parent_account, school_id=school_id, del_flag=FLAG_NO)
        if check_user_bind and weixin_account:
            raise BusinessException(ERR_USER_IS_BIND)
        else:
            weixin_account.update(del_flag=FLAG_YES)

    # 检查学生信息，注意:按徐峻要求，性别当前未处理
    # student_list_json格式 [{"full_name":"张三", "code":"G20160145", "sex":"男", "relation":"父亲", }, {}]
    children_account = None

    student_list_json = json.loads(student_list_json)
    children = list()
    for each_student in student_list_json:
        full_name = each_student.get('full_name', "")
        code = each_student.get('code', "")
        sex = each_student.get('sex', "")
        relation = each_student.get('relation', "")
        cur_student = Student.objects.filter(full_name=full_name, account__code=code, is_in=FLAG_YES, is_available=FLAG_YES, del_flag=FLAG_NO).first()
        if not cur_student:
            logger.info(u"当前处理孩子 姓名：%s   学号：%s" % (full_name, code))
            raise BusinessException(ERR_GET_STUDENT)

        # 任选一个孩子作为add_parent的用户，add_parent必须要传，实际作用不大。
        children_account = cur_student.account

        student_dict = {
            "student_id": cur_student.id,
            "relation": relation,
            "status": APPLICATION_STATUS_APPROVED[0]
        }
        children.append(student_dict)

    parent_info = {
        "mobile": mobile,
        "full_name": fullname,
        "sex": parent_sex,
        "children": children,
        "address": address,
    }
    ret = add_parent(children_account, parent_info)
    if ret["c"] != ERR_SUCCESS[0]:
        # raise BusinessException(ERR_MESSAGECODE)
        raise Exception(ret['m'])

    # 获取刚添加的家长帐号
    parent_account = Account.objects.filter(mobile=mobile, del_flag=FLAG_NO).first()
    if not parent_account:
        raise BusinessException(ERR_WX_ADD_PARENT)

    # 绑定用户account和微信openid
    bind_openid_schoolaccount(openid, parent_account, school_id, check_user_bind)

    # 如果只是检查，则此处直接抛出异常，使事务回退
    if only_check:
        raise BusinessException(ERR_ONLYCHECK_OK)
    return result


def get_wx_service_list(user):
    result = list()
    wx_services_all = WeixinService.objects.filter(del_flag=FLAG_NO).order_by('sort')

    wx_services_group_dict = dict()
    for each_dict in wx_services_all:
        wx_services_group_dict[each_dict.group] = list()

    cur_type_user = get_type_current_user(user)
    for each_wxservice in wx_services_all:
        # 检查学校是否开通此应用
        school_service = SchoolService.objects.filter(school_id=user.school.id, service=each_wxservice.service, del_flag=FLAG_NO)
        if not school_service:
            continue

        # 非管理员看不到仅管理员可用的应用
        if each_wxservice.support_user_type == 0:
            if not is_sys_admin(cur_type_user, each_wxservice.service.code):
                continue
        else:
            # 教师、家长、学生只能看到自己角色可见的应用
            if int(each_wxservice.support_user_type) & user.type == 0:
                continue

        wx_service_dict = {
            'app_code': each_wxservice.service.code,
            'app_name': each_wxservice.entrance,
            'app_url': each_wxservice.url + 'sid=' + str(user.school.id),
            'app_icon': each_wxservice.icon,
        }

        wx_services_group_dict[each_wxservice.group].append(wx_service_dict)

    # 检查删除结果中为分组中没有app的记录
    for each_group in wx_services_group_dict:
        if not wx_services_group_dict[each_group]:
            continue
            # wx_services_group_dict.pop(each_group)

        # 重新组装返回结果
        new_dict = dict()
        new_dict[each_group] = copy.deepcopy(wx_services_group_dict[each_group])
        result.append(new_dict)

    return result


def get_wx_service_domain(app_code):
    wx_service = WeixinService.objects.filter(service__code=app_code, del_flag=FLAG_NO).first()
    url = wx_service.url
    proto, rest = urllib.splittype(url)
    res, rest = urllib.splithost(rest)
    result = {
        "domain": res,
    }
    return result


def is_sys_admin(teacher, service_code):
    # 检查老师是不是该系统的管理员
    if not isinstance(teacher, Teacher):
        return False
    current_service = Service.objects.filter(code=service_code, del_flag=FLAG_NO).first()
    super_role = Role.objects.filter(service=current_service, code='1', del_flag=FLAG_NO).first()
    is_sysadmin = UserRole.objects.filter(user=teacher, school=teacher.school, role=super_role, del_flag=FLAG_NO).exists()
    if is_sysadmin:
        return


def get_type_current_user(user):
    return get_type_user(user.id, user.type, user.school.id)


def get_type_user(account_id, user_type, school_id):
    """
    查询ID当前对应的用户类型资料（学生、老师、家长）
    :param:用户ID，当前用户类型，学校ID
    :return:类型对应的对象
    """
    if user_type == USER_TYPE_STUDENT:
        result = Student.objects.filter(account_id=account_id, school_id=school_id, del_flag=FLAG_NO)
    elif user_type == USER_TYPE_TEACHER:
        result = Teacher.objects.filter(account_id=account_id, school_id=school_id, del_flag=FLAG_NO)
    elif user_type == USER_TYPE_PARENT:
        result = Parent.objects.filter(account_id=account_id, school_id=school_id, del_flag=FLAG_NO)
    else:
        result = None
    if result:
        result = result.first()
    return result


def check_sms_flow(mobile, times=3, seconds=600):
    # 检查短信验证码发送数量。默认600秒即10分钟3次
    pre_timestamp = int(time.time())-seconds
    verifycode_cnt = VerifyCode.objects.filter(mobile=mobile, timestamp__gte=pre_timestamp).count()
    return True if verifycode_cnt < times else False


def api_send_bind_messagecode(mobile, check_account_exist=True, check_user_bind=False):
    # 发送验证码，check_user_bind为是否检查用户是否已经绑定过。为True时检查，为False时不检查， 同时绑定时，会自动删除原来的绑定。默认为False
    # mobile = mobile.strip()
    if not mobile or __check_mobile_valid(mobile) == ERR_USER_MOBILE_ERROR:
        raise BusinessException(ERR_USER_MOBILE_ERROR)

    # 短信流量控制
    if not check_sms_flow(mobile, times=3, seconds=600):
        raise BusinessException(ERR_VERIFY_CODE_SEND_MAX)

    # 检查用户是否存在
    account = Account.objects.filter(mobile=mobile, del_flag=FLAG_NO).first()
    if check_account_exist and not account:
        raise BusinessException(ERR_VERIFY_CODE_USER_NOT_EXIST)

    # 检查用户是否已经绑定
    if check_user_bind:
        weixin_account = WeixinAccount.objects.filter(account=account, del_flag=FLAG_NO).first()
        if weixin_account:
            raise BusinessException(ERR_VERIFY_CODE_TELISBIND)

    # 先将原来的验证码失效，再生成新的验证码。
    VerifyCode.objects.filter(mobile=mobile, del_flag=FLAG_NO).update(del_flag=FLAG_YES)
    VerifyCode.objects.create(mobile=mobile, IMCode_status=FLAG_YES)
    send_message(mobile)
    return ''


def api_school_qrcode(domain, school_id):
    school_url = 'http://%s/wx/page/scan/schoolcode?sid=%s' % (domain, school_id)
    school_qrcode = get_str_qrcode_base64(school_url)
    result = {
        "parentbind_base64_image": school_qrcode,
        "parentbind_base64_html": r'<img src="data:image/gif;base64,' + school_qrcode + '">',
    }

    # 查询学校公众号二维码图片
    weixinschool = WeixinSchool.objects.filter(school_id=school_id, del_flag=FLAG_NO).first()
    school_mp_qrcode_url = weixinschool.mp_image_url
    result['school_mp_qrcode_url'] = school_mp_qrcode_url
    return result


def api_parent_qrcode(domain, school_id, parent_id):
    parent_url = 'http://%s/wx/page/scan/parentcode?sid=%s&parent_id=%s' % (domain, school_id, parent_id)
    parent_qrcode = get_str_qrcode_base64(parent_url)
    result = {
        "invite_base64_image": parent_qrcode,
        "invite_base64_html": r'<img src="data:image/gif;base64,' + parent_qrcode + '">',
    }

    return result


def api_fh_qrcode(domain):
    parent_url = 'http://%s/wx/page/scan/fhcode' % (domain, )
    parent_qrcode = get_str_qrcode_base64(parent_url)
    result = {
        "fh_base64_image": parent_qrcode,
        "fh_base64_html": r'<img src="data:image/gif;base64,' + parent_qrcode + '">',
    }

    return result


def wx_mod_debugstatus(debug_status):
    if not debug_status:
        raise BusinessException(ERR_REQUEST_PARAMETER_ERROR)
    settings.WEB_DEBUG_MOD = int(debug_status)
    return 'ok'


def api_add_child_by_parent(user, student_list_json):
    # 家长给本人添加孩子
    cur_type_user = get_type_current_user(user)
    if not isinstance(cur_type_user, Parent):
        raise BusinessException(ERR_WX_USE_PARENT_ADD_STUDENT)

    student_list_json = json.loads(student_list_json)
    children = list()
    for each_student in student_list_json:
        full_name = each_student.get('full_name', "")
        code = each_student.get('code', "")
        sex = each_student.get('sex', "")
        relation = each_student.get('relation', "")
        cur_student = Student.objects.filter(full_name=full_name, account__code=code, is_in=FLAG_YES, is_available=FLAG_YES, del_flag=FLAG_NO).first()
        if not cur_student:
            logger.info(u"当前处理孩子 姓名：%s   学号：%s" % (full_name, code))
            raise BusinessException(ERR_GET_STUDENT)

        student_dict = {
            "student_id": cur_student.id,
            "relation": relation,
            "status": APPLICATION_STATUS_APPROVED[0]
        }
        children.append(student_dict)

    parent_info = {
        "mobile": user.mobile,
        "full_name": cur_type_user.full_name,
        "children": children,
    }
    ret = add_parent(user, parent_info)
    if ret["c"] != ERR_SUCCESS[0]:
        raise Exception(ret['m'])

    return 'ok'


@transaction.atomic
def api_invite_parent1(user, school_id, mobile, address, fullname, parent_sex, relation, messagecode):
    result = dict()
    if not mobile or not address or not school_id or not relation:
        raise BusinessException(ERR_REQUEST_PARAMETER_ERROR)

    # 检查手机验证码
    ret = verify_messagecode(mobile, code=messagecode, expire_time=600)
    if ret["c"] != ERR_SUCCESS[0]:
        raise BusinessException(ERR_MESSAGECODE)

    # 检查当前用户是不是家长身份
    cur_type_user = get_type_current_user(user)
    if not isinstance(cur_type_user, Parent):
        raise BusinessException(ERR_WX_USE_PARENT_ADD_STUDENT)

    # 查询当前登陆用户（家长）的所有孩子，组装待添加的children数组
    children = list()
    parent_students = ParentStudent.objects.filter(parent_id=cur_type_user.id, del_flag=FLAG_NO)
    for each_student in parent_students:
        student_dict = {
            "student_id": each_student.student_id,
            "relation": relation,
            "status": APPLICATION_STATUS_APPROVED[0]
        }
        children.append(student_dict)

    parent_info = {
        "mobile": mobile,
        "full_name": fullname,
        "sex": parent_sex,
        "children": children,
        "address": address,
    }
    ret = add_parent(user, parent_info)
    if ret["c"] != ERR_SUCCESS[0]:
        raise Exception(ret['m'])

    return result


@transaction.atomic
def api_invite_parent(openid, parent_id, school_id, mobile, address, fullname, parent_sex, relation, messagecode, check_user_bind=False, only_check=False):
    result = dict()
    if not openid or not school_id:
        raise BusinessException(ERR_REQUEST_PARAMETER_ERROR)

    src_parent = get_parentbyid(parent_id)

    # 检查手机验证码
    if not only_check:
        if not mobile:
            raise BusinessException(ERR_REQUEST_PARAMETER_ERROR)

        ret = verify_messagecode(mobile, code=messagecode, expire_time=600)
        if ret["c"] != ERR_SUCCESS[0]:
            raise BusinessException(ERR_MESSAGECODE)

    # 检查传入的电话号码对应的家长是否存在, 如果存在，则检查用户是否已经绑定微信
    parent_account = Account.objects.filter(mobile=mobile, del_flag=FLAG_NO).first()
    if parent_account:
        weixin_account = WeixinAccount.objects.filter(account=parent_account, school_id=school_id, del_flag=FLAG_NO)
        if check_user_bind and weixin_account:
            raise BusinessException(ERR_USER_IS_BIND)
        else:
            weixin_account.update(del_flag=FLAG_YES)

    # 查询（来源家长）的所有孩子，组装待添加的children数组
    children = list()
    parent_students = ParentStudent.objects.filter(parent_id=parent_id, del_flag=FLAG_NO)
    for each_student in parent_students:
        student_dict = {
            "student_id": each_student.student_id,
            "relation": relation,
            "status": APPLICATION_STATUS_APPROVED[0]
        }
        children.append(student_dict)

    parent_info = {
        "mobile": mobile,
        "full_name": fullname,
        "sex": parent_sex,
        "children": children,
        "address": address,
    }
    ret = add_parent(src_parent.account, parent_info)
    if ret["c"] != ERR_SUCCESS[0]:
        raise Exception(ret['m'])

    # 获取刚添加的家长帐号
    parent_account = Account.objects.filter(mobile=mobile, del_flag=FLAG_NO).first()
    if not parent_account:
        raise BusinessException(ERR_WX_ADD_PARENT)

    # 绑定用户account和微信openid
    bind_openid_schoolaccount(openid, parent_account, school_id, check_user_bind)

    # 如果只是检查，则此处直接抛出异常，使事务回退
    if only_check:
        raise BusinessException(ERR_ONLYCHECK_OK)
    return result


def get_parentbyid(parent_id):
    # 通过家长id，获取家长对象
    if not parent_id:
        raise BusinessException(ERR_REQUEST_PARAMETER_ERROR)

    parent = Parent.objects.filter(id=parent_id, del_flag=FLAG_NO).first()

    if not parent:
        raise BusinessException(ERR_PARENT_NULL)

    return parent


def get_fh_weixinschool():
    return WeixinSchool.objects.filter(school__code='fhxx', school__del_flag=FLAG_NO, del_flag=FLAG_NO).first()
