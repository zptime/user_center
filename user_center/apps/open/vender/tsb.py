# -*- coding=utf-8 -*-

from user_center.apps.account.agents import get_user_info
from user_center.apps.school.models import *
from user_center.apps.student.models import *
from user_center.apps.teacher.models import *
from user_center.apps.parent.models import *
from user_center.apps.account.agents import api_change_user_type
from user_center.utils.public_fun import *
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


TSB_APP_KEY = "zhxy01"
TSB_APP_SECRET = "xkjozhxydswsfdg1"
# TSB_URL = "http://www.hbeducloud.com:8888/"
# TSB_URL = "http://10.1.11.35:8888/"
TSB_URL = "http://10.0.99.8:8888/"
TSB_USER_TYPE_TEACHER = 0b1000
TSB_USER_TYPE_STUDENT = 0b0100
TSB_USER_TYPE_PARENT = 0b0010


def get_token(app_key=TSB_APP_KEY, app_secret=TSB_APP_SECRET, go_to=True):
    url = TSB_URL + "TSB_ISCHOOL_DOCKING_SERVER/oauth/getToken"
    if go_to == False:
        url = TSB_URL + "auth/oauth/getToken"
    form_data_dict = {"appKey": app_key, "appSecret": app_secret}
    form_data_dict = json.dumps(form_data_dict)
    logger.debug('in get token func: redirecr to url-{} to get response'.format(url))
    response = send_http_request(url=url, method="POST", form_data_dict=form_data_dict, centent_type="json")
    logger.debug("[tsb: get_token] response: %s" % response)
    response = json.loads(response)
    if response["code"] == 1:
        return response["data"]["token"]
    else:
        logger.error(u"tsb add_user_info errorCode[%d] errorMessage[%s] "
                     % (response["errorCode"], response["errorMessage"]))
        raise Exception(u"从应用获取用户Token失败，可能没有权限访问")


def add_user_info(user, token):
    user_info = get_user_info(user)
    if not user_info.get("id_card", ""):
        raise AttributeError(u"请联系学校管理员，设置身份证号才能使用该应用")
    user_info_param = {
        "appKey": TSB_APP_KEY,
        "token": token,
        "userRealName": user_info.get("full_name", ""),
        "lgname": user_info.get("username", ""),
        "sex": 1 if user_info.get("sex", "") == u"男" else 2,
        "mobile": user_info.get("mobile", ""),
        "idcard": user_info.get("id_card", ""),
        "userType": user_info.get("user_type", ""),
        "userSchool": user_info.get("school_name_full", ""),
        "schoolType": user_info.get("school_type", "") if user_info.get("school_type", "") else 1,
        "provinceId": "",
        "provinceName": user_info.get("school_province", u"湖北"),
        "dsId": "420101",
        "dsName": user_info.get("school_city", u"武汉"),
        "qxId": "230106",
        "qxName": user_info.get("school__district", u"武昌"),
        "userGrade": user_info.get("grade_num", ""),
        "userClass": user_info.get("class_name", ""),
        "learnyear": user_info.get("enrollment_year", ""),
    }
    url = TSB_URL + "TSB_ISCHOOL_DOCKING_SERVER/oauth/addUserinfo"
    form_data_dict = user_info_param
    form_data_dict = json.dumps(form_data_dict)
    logger.debug("[ts: add_user_info] %s" % form_data_dict)
    response = send_http_request(url=url, method="POST", form_data_dict=form_data_dict, centent_type="json")
    logger.debug("[tsb: add_user_info] response: %s" % response)
    response = json.loads(response)
    if response["code"] == 1:
        return response["data"]["ut"]
    else:
        logger.error(u"tsb add_user_info errorCode[%d] errorMessage[%s] " % (response["errorCode"], response["errorMessage"]))
        raise Exception(u"与应用系统对接用户信息失败，可能没有权限访问")


def get_redirect_url(user, app_code):
    logger.debug("to get token...")
    token = get_token()
    logger.debug('to get ut...')
    ut = add_user_info(user, token)
    url = "http://passport.hbeducloud.com:8080/hblogin/redirect?authentication="+ut
    return url


def get_user_by_id(user_id, token):
    user_info_param = {
        "appKey": TSB_APP_KEY,
        "token": token,
        "userId": user_id,
    }
    url = TSB_URL + "auth/oauth/getUserbyId"
    form_data_dict = user_info_param
    form_data_dict = json.dumps(form_data_dict)
    logger.debug("[tsb: get_user_by_id] form_data: %s" % form_data_dict)
    response = send_http_request(url=url, method="POST", form_data_dict=form_data_dict, centent_type="json")
    logger.debug("[tsb: get_user_by_id] response: %s" % response)
    response = json.loads(response)
    if response["code"] == 1:
        return response["data"]
    else:
        raise Exception(u"tsb get_user_by_id errorCode[%d] errorMessage[%s] " % (response["errorCode"], response["errorMessage"]))


def get_user(user_id):
    token = get_token(go_to=False)
    user_info = get_user_by_id(user_id, token)
    if not user_info["organizationName"] or not user_info["idcard"] or not user_info["occupations"]:
        return ERR_SP_USER_NOT_COMPLETE_INFO, None

    # 获取所在学校
    school_name = user_info["organizationName"]
    school_obj = School.objects.filter(Q(name_full=school_name) | Q(name_simple=school_name)).first()
    if not school_obj:
        return ERR_SP_SCHOOL_NOT_EXIST, None

    # 获取用户对象
    id_card = user_info["idcard"]
    tsb_user_type = user_info["occupations"]
    tsb_user_type = int(tsb_user_type, 2)
    user_type = USER_TYPE_NOT_SET
    user_obj = None
    if tsb_user_type & TSB_USER_TYPE_TEACHER:
        user_type = USER_TYPE_TEACHER
        user_obj = Teacher.objects.filter(school=school_obj, id_card=id_card, del_flag=FLAG_NO).first()
    elif tsb_user_type & TSB_USER_TYPE_STUDENT:
        user_type = USER_TYPE_STUDENT
        user_obj = Student.objects.filter(school=school_obj, id_card=id_card, del_flag=FLAG_NO).first()
    elif tsb_user_type & TSB_USER_TYPE_PARENT:
        user_type = USER_TYPE_PARENT
        user_obj = Parent.objects.filter(school=school_obj, id_card=id_card, del_flag=FLAG_NO).first()
    if not user_obj:
        return ERR_SP_USER_NOT_EXIST, None

    # 切换用户身份
    account_obj = user_obj.account
    if account_obj and school_obj and user_type:
        api_change_user_type(account_obj, school_obj.id, user_type)
        return ERR_SUCCESS, account_obj
    else:
        return ERR_SP_USER_NOT_EXIST, None




