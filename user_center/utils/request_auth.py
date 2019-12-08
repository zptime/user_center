#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import traceback
from err_code import *
from django.conf import settings
import functools
from django import http
from django.utils.decorators import method_decorator
from ipaddr_fun import get_subnet_list, ip_in_subnet_list
from user_center.apps.service import agents as service_agents
from user_center.apps.teacher.models import *
from constant import *

logger = logging.getLogger(__name__)

# 是否检查登录
IS_CHECK_LOGIN = True

special_dict = {"/api/detail/student": "account_id", "/api/update/student": "account_id",
                "/api/detail/parent": "account_id", "/api/update/parent": "account_id",
                "/api/detail/teacher": "account_id", "/api/update/teacher": "account_id",
                "/open/call/api": "account_id"}


def auth_check(request, method="POST", module=None, check_login=True, is_admin=False):
    dictResp = {}

    log_request(request)
    if not IS_CHECK_LOGIN:
        return dictResp

    if check_login:
        try:
            if not request.user.is_authenticated():
                dictResp = {'c': ERR_USER_NOTLOGGED[0], 'm': ERR_USER_NOTLOGGED[1]}
                return dictResp
            # 检查是否是管理员
            if is_admin and request.user.is_admin != 1:
                dictResp = {'c': ERR_USER_AUTH[0], 'm': ERR_USER_AUTH[1]}
                return dictResp
            # 检查是否是用户使用自己的信息
            is_self = False
            if str(request.path) in special_dict.keys():
                form_name = special_dict[request.path]
                account_id = request.POST.get(form_name)
                if account_id and int(account_id) == request.user.id:
                    is_self = True
            request.user.role = []
            if not is_self and module is not None:
                module_list, user_role_list = get_user_permission(request.user)
                request.user.role = user_role_list
                if module not in module_list:
                    dictResp = {"c": ERR_USER_AUTH[0], "m": ERR_USER_AUTH[1], "d": []}
                    return dictResp
        except Exception as ex:
            sErrInfo = traceback.format_exc()
            logger.error(sErrInfo)
            dictResp = {"c": -1, "m": ex.message}
            return dictResp

        # if not request.user.num or not request.user.school_id:
        #     dictResp = {'c': ERR_USER_INFO_INCOMPLETE[0], 'e':ERR_USER_INFO_INCOMPLETE[1]}
        #     return dictResp

    if request.method != method.upper():
        dictResp = {'c': ERR_REQUESTWAY[0], 'e': ERR_REQUESTWAY[1]}
        return dictResp

    return dictResp


def internal_or_403(view_func):
    """
    A view decorator which returns the provided view function,
    modified to return a 403 when the remote address is not in
    the list of internal IPs defined in settings.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            subnet_list = get_subnet_list()
            if not ip_in_subnet_list(request.META['REMOTE_ADDR'], subnet_list):
                return http.HttpResponseForbidden('<h1>Forbidden</h1>')
            return view_func(request, *args, **kwargs)
        except Exception as ex:
            sErrInfo = traceback.format_exc()
            logger.error(sErrInfo)
            return http.HttpResponseForbidden('<h1>Forbidden</h1>')
    return wrapper


class Internal(object):
    """
    A mix-in for class based views, which disallows requests from
    non-internal IPs.
    """
    @method_decorator(internal_or_403)
    def dispatch(self, *args, **kwargs):
        return super(Internal, self).dispatch(*args, **kwargs)


def log_request(request):
    # self.start_time = time.time()
    if "/open/list/items" == request.get_full_path():
        return
    remote_addr = request.META.get('REMOTE_ADDR')
    if remote_addr in getattr(settings, 'INTERNAL_IPS', []):
        remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or remote_addr
    if hasattr(request, 'user'):
        user_account = getattr(request.user, 'username', '-')
    else:
        user_account = 'nobody-user'
    if 'POST' == str(request.method):
        logger.info('[POST] %s %s %s :' % (remote_addr, user_account, request.get_full_path()))
        # info(request.POST)
    if 'GET' == str(request.method):
        logger.info('[GET] %s %s %s :' % (remote_addr, user_account, request.get_full_path()))
        # info(request.GET)


def get_user_permission(user):
    school_id = user.school_id
    permission_modules = []
    user_role_list = []
    teacher = Teacher.objects.filter(school_id=school_id, account_id=user.id, is_in=YES, del_flag=NO).first()
    if not teacher or user.type != USER_TYPE_TEACHER:
        return permission_modules, user_role_list
    user_role_list = service_agents.get_service_user_role(service_code=SERVICE_CODE_USER_CENTER, user_id=teacher.id, school_id=school_id)
    if user_role_list:
        if ADMIN_USER_TYPE_SYSTEM_ADMIN in user_role_list:
            permission_modules = MODULE_LIST
        if ADMIN_USER_TYPE_STUDENT_ADMIN in user_role_list:
            permission_modules.append(MODULE_STUDENT)
            permission_modules.append(MODULE_PARENT)
        if ADMIN_USER_TYPE_TEACHER_ADMIN in user_role_list:
            permission_modules.append(MODULE_TEACHER)

    teacher_obj = Teacher.objects.filter(school_id=school_id, account_id=user.id, del_flag=NO).first()
    if teacher_obj and teacher_obj.cls and MODULE_STUDENT not in permission_modules \
            and MODULE_STUDENT not in permission_modules:
        user_role_list.append(ADMIN_USER_TYPE_CLASS_ADMIN)
        permission_modules.append(MODULE_STUDENT)
        permission_modules.append(MODULE_PARENT)
    permission_modules = list(set(permission_modules))
    return permission_modules, user_role_list


def convert_user_role_list_to_mask(user_role_list):
    mask = 0x0
    for user_role in user_role_list:
        mask |= int(user_role)
    return mask


def check_cls_permission(user, class_id=-1):
    teacher_obj = Teacher.objects.filter(school_id=user.school_id, account_id=user.id, del_flag=NO).first()
    if teacher_obj and teacher_obj.cls:
        teacher_class_id = teacher_obj.cls_id
        if class_id < 0:
            return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": [teacher_class_id]}
        if teacher_class_id != class_id:
            return {"c": ERR_USER_AUTH[0], "m": ERR_USER_AUTH[1], "d": []}
        else:
            return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": [teacher_class_id]}
    else:
        return {"c": ERR_USER_AUTH[0], "m": ERR_USER_AUTH[1], "d": []}