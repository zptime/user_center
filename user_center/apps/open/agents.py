# -*- coding=utf-8 -*-
import datetime
import traceback
import sys
import importlib
from user_center.utils.err_code import *
from user_center.apps.account.models import *
from user_center.apps.school.models import *
from user_center.apps.student.models import *
from user_center.apps.teacher.models import *
from user_center.apps.parent.models import *
from user_center.apps.common.models import *
from user_center.apps.subject.models import *
from user_center.apps.service.models import *
from user_center.apps.service import agents as service_agents
from user_center.utils.public_fun import *
from django.conf import settings
from django.db.models import ManyToOneRel
import importlib
import logging

logger = logging.getLogger(__name__)

MODEL_CLS_LIST = ["Subject", "Textbook", "Chapter", "SchoolSubject", "SchoolTextbook", "Subnet", "School", "Grade",
                  "Class", "Account", "Teacher", "Student", "Parent", "Service", "Role", "UserRole",
                  "TeacherClass", "TeacherSubject", "TeacherTextbook"]

FUNCTION_DICT = {'user_center.apps.service.views': ["api_list_service_apps"],
                 'user_center.apps.school.views': ["api_list_grade", "api_list_class"],
                 'user_center.apps.student.views': ["api_list_student", "api_update_student"],
                 'user_center.apps.parent.views': ["api_update_parent"],
                 'user_center.apps.teacher.views': ["api_list_teacher", "api_update_teacher", "api_list_teacher_textbook",
                                                    "api_update_teacher_textbook",
                                                    "api_add_teacher_textbook", "api_delete_teacher_textbook",
                                                    "api_list_teacher_class", "api_delete_teacher_class", "api_add_teacher_class"],
                 'user_center.apps.account.views': ['api_detail_account', 'api_reset_password', 'api_list_user_type', 'api_change_user_type'],
                 'user_center.apps.subject.views': ['api_school_list_subject', 'api_admin_list_chapter', 'api_school_list_textbook'],
                 'user_center.apps.common.views': ['api_upload_image']}

ITEM_NUM_PER_QUERY = 500


def class_name_to_class(model_cls_name):
    model_cls = getattr(sys.modules[__name__], model_cls_name)
    return model_cls


def get_user_center_url():
    user_center_obj = Service.objects.get(code=settings.SERVICE_USER_CENTER, del_flag=FLAG_NO)
    internet_url = get_domain_name(user_center_obj.internet_url)
    return internet_url


def get_user_center_image_url(path):
    if not path:
        return ""
    image_url = get_user_center_url() + path
    return image_url


def call_function(request, function_name):
    resp = None
    for model_name, func_name_list in FUNCTION_DICT.items():
        if function_name in func_name_list:
            model = importlib.import_module(model_name)
            func = getattr(model, function_name)
            resp = func(request)
    if not resp:
        raise Exception(u"没有找到对应的函数名称")
    # 将url相对地址替换为绝对地址
    try:
        if resp.content:
            resp_content = json.loads(resp.content)
            resp_data = resp_content["d"]
            have_change = False
            if resp_data:
                for item in resp_data:
                    for key, value in item.items():
                        if key.endswith("url") and not key.startswith("http"):
                            logger.info(value)
                            item[key] = get_user_center_image_url(value)
                            have_change = True
                            logger.info(item[key])
            if have_change:
                resp.content = json.dumps(resp_content)
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo) 
    return resp


def detail_update_time(model_cls_name):
    model_cls = class_name_to_class(model_cls_name)
    if not model_cls:
        return {"c": ERR_MODEL_NAME_ERR[0], "m": ERR_MODEL_NAME_ERR[1], "d": []}
    update_time = datetime.datetime.now() - datetime.timedelta(hours=24)
    obj = model_cls.objects.filter()
    if not obj:
        return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": [update_time]}
    account = obj.latest("update_time")
    if account:
        update_time = account.update_time
    # update_time = datetime_to_str(update_time, DATE_FORMAT_TIME)
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": [update_time]}

EXCLUDE_FIELD = []
REPLACE_FIELD = {"image_id": "image__url", "logo_id": "logo__url", "banner_id": "banner__url"}
OUTPUT_REPLACE_FIELD = {"image__url": "image_url", "logo__url": "logo_url", "banner__url": "banner_url"}


def list_items(model_cls_name, update_time, item_id):
    update_time = datetime.datetime.strptime(update_time, '%Y-%m-%d %H:%M:%S')
    item_id = int(item_id)
    model_cls = class_name_to_class(model_cls_name)
    ret_obj_list = []

    # 获取model的所有field_name
    all_fields_column = []
    all_fields = model_cls._meta.get_fields()
    for field in all_fields:
        if field in EXCLUDE_FIELD or isinstance(field, ManyToOneRel):
            continue
        column = field.column
        if column in REPLACE_FIELD.keys():
            column = REPLACE_FIELD[column]
        all_fields_column.append(column)

    # 查询更新时间相同 id大于的项目
    obj_list = model_cls.objects.filter(update_time=update_time, id__gt=item_id).order_by('id')[:ITEM_NUM_PER_QUERY].values(*all_fields_column)
    ret_obj_list.extend(obj_list)
    result_len = ITEM_NUM_PER_QUERY - len(obj_list)

    # 查询更新时间大于指定时间的所有项目
    if result_len > 0:
        obj_list = model_cls.objects.filter(update_time__gt=update_time).order_by('update_time', 'id')[:result_len].\
            values(*all_fields_column)
        ret_obj_list.extend(obj_list)

    # 设置输出格式
    for ret_obj in ret_obj_list:
        for key, value in ret_obj.items():
            if key in OUTPUT_REPLACE_FIELD.keys():
                new_key = OUTPUT_REPLACE_FIELD[key]
                ret_obj[new_key] = ""
                ret_obj[new_key] = ret_obj.pop(key)
                if not ret_obj[new_key]:
                    ret_obj[new_key] = ""
    logger.info("[list_items] %s %s item_id(%s) len(%s)" % (model_cls_name, update_time, item_id, len(ret_obj_list)))
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": ret_obj_list}


def refresh_one_item_of_all_service(model_name, item_data):
    service_url_list = Service.objects.filter(type=SERVICE_TYPE_INTERNAL, del_flag=FLAG_NO).exclude(code="user_center")\
        .values_list('intranet_url', flat=True)
    service_domain_list = []
    for service_url in service_url_list:
        service_domain = decode_domain_list(service_url)
        if service_domain in service_domain_list:
            continue
        else:
            service_domain_list.append(service_domain)
        # url = service_domain + "/user_center/api/refresh/item"
        try:
            form_data_dict = {"model_name": model_name, "item_id": item_data["id"], "item_data": json.dumps(item_data)}
            response = try_send_http_request(domain_list=service_domain, path=settings.API_USER_CENTER_APP_REFRESH_ITEM,
                                             method="POST", form_data_dict=form_data_dict)
        except Exception as e:
            logger.error("refresh_one_item error %s [%s] %s" % (str(service_domain), model_name, str(item_data)))


def list_subnet():
    subnet_list = Subnet.objects.filter(del_flag=NO).values_list("cidr", flat=True)
    return list(subnet_list)


def decode_domain_list(domain_str):
    if "[" in domain_str:
        ret_domain_list = []
        domain_list = json.loads(domain_str)
        for domain in domain_list:
            ret_domain_list.append(get_domain_name(domain))
        return ret_domain_list
    else:
        intranet_url = get_domain_name(domain_str)
        return [intranet_url]


# 第三应用的service code的定义为
# app_提供商编码_应用编码
def redirect_service_url(user, service_code):
    service_obj = Service.objects.filter(code=service_code, del_flag=FLAG_NO).first()
    if not service_obj:
        raise Exception(u"没有找到对应服务")

    if service_obj.type == SERVICE_TYPE_VENDER:
        # 获取提供商编码和应用编码
        code_list = service_code.split("_")
        if service_code.startswith("app_") and len(code_list) != 3:
            raise Exception(u"服务代码不正确")
        vender_code = code_list[1]
        app_code = code_list[2]
        logger.debug("in open agent:func<redirect_service_url>, to import vender module <user_center.apps.open.\
        vender.{}>...".format(vender_code))
        vender_module = importlib.import_module("user_center.apps.open.vender." + vender_code)
        logger.info("module imported<{}>".format(vender_module))
        url = vender_module.get_redirect_url(user, app_code)
        logger.info("get url-{}".format(url))
        return url

    raise Exception(u"没有找到该应用对应处理模块")

from urllib import quote
from vender import tsb
from django.contrib.auth import login


def app_auth(request, user_id, service_code=""):
    try:
        # 获取用户对象
        err_code, user = tsb.get_user(user_id)
        if err_code[0] != ERR_SUCCESS[0] or not user:
            return err_code, None

        # 检查用户是否有该服务使用权限
        if not service_code:
            service_code = "home_page"
        service_auth = False
        ret_val = service_agents.list_service_apps(user)
        if ret_val["c"] != ERR_SUCCESS[0]:
            raise Exception(u'获取服务列表失败')
        category_service_list = ret_val["d"]
        for category_service in category_service_list:
            service_list = category_service["data"]
            if service_list and not service_auth:
                for service in service_list:
                    if service["code"] == service_code:
                        service_auth = True
                        break
        if not service_auth:
            raise Exception(u"没有权限访问该应用，您所在学校没有开通该应用")
        # 模拟用户本地登录
        user.backend = settings.AUTHENTICATION_BACKENDS[0]
        login(request, user)
        token = request.session.session_key
        if not token:
            return ERR_SP_AUTH_UC_ERROR, None

        # 重定向至CAS认证，并跳转对应子系统
        service_obj = Service.objects.filter(code=service_code).first()
        url = login_cas(user.username, token, service_obj.internet_url)
        return ERR_SUCCESS, url
    except Exception as ex:
        return [-1, ex.message], None


def login_cas(username, token, service=""):
    url = settings.CAS_SERVER_URL + "login?"
    url += "username=" + username
    url += "&token=" + token
    if service:
        url += "&service=" + quote(service)
    return url


def reset_password(account_id, new_password):
    account = Account.objects.filter(id=int(account_id), del_flag=FLAG_NO).first()
    account.set_password(new_password)
    account.encoded_pwd = xor_crypt_string(data=new_password, encode=True)
    account.save()
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}


def get_username_passwd_by_wxtoken(wxtoken):
    WXTOKEN_EXPIRE = 60 * 60 * 12
    try:
        account_id, timestamp, timestamp_str = wxtoken_decompose(wxtoken)
        current_time = int(time.time())
        logger.info('wxtoken de-compose, token time: [%s], current time: [%s]' % (timestamp_str, current_time))
        if current_time - timestamp > WXTOKEN_EXPIRE:
            raise Exception(u'微信登录token已过期')
        account = Account.objects.filter(id=account_id).first()
        if not account:
            raise Exception(u'微信登录用户不存在')
        pwd = xor_crypt_string(data=account.encoded_pwd, decode=True)
        return account.username or '', account.mobile or '', pwd
    except Exception as e:
        logger.error(e.message)
        raise e