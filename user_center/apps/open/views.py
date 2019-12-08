#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotAllowed

from django.contrib.auth import logout
from user_center.utils.request_auth import *
from user_center.utils.gen_response import *
from user_center.utils.constant import *
from user_center.utils.err_code import *
from user_center.apps.student import agents as student_agents
from user_center.apps.teacher import agents as teacher_agents
from user_center.apps.school import school_agents, class_agents
from agents import *
import json
import traceback
import logging

logger = logging.getLogger(__name__)


@internal_or_403
def open_list_student(request):
    dictResp = auth_check(request, "POST", check_login=False)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        school_id = request.POST.get('school_id')
        full_name = request.POST.get("full_name", "")
        code = request.POST.get("code", "")
        name_or_code = request.POST.get("name_or_code", "")
        is_in = request.POST.get("is_in", "")
        kind = request.POST.get("kind", "")
        is_available = request.POST.get("is_available", "")
        grade_name = request.POST.get("grade_name", "")
        class_id = request.POST.get("class_id", "")
        enrollment_year = request.POST.get("enrollment_year", "")
        verbose = request.POST.get("verbose", "")
        if not school_id:
            dictResp = {"c": ERR_SCHOOL_ID_ERR[0], "m": ERR_SCHOOL_ID_ERR[1], "d":[]}
            return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")
        dictResp = student_agents.list_student(full_name=full_name, code=code, name_or_code=name_or_code,
                                is_in=is_in, kind=kind, is_available=is_available, grade_name=grade_name,
                                class_id=class_id, enrollment_year=enrollment_year, verbose=verbose, school_id=school_id)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


@internal_or_403
def open_list_teacher(request):
    dict_resp = auth_check(request, "POST", check_login=False)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        school_id = request.POST.get('school_id')
        full_name = request.POST.get("full_name", "")
        code = request.POST.get("code", "")
        name_or_code = request.POST.get("name_or_code", "")
        is_in = request.POST.get("is_in", "")
        in_date_year = request.POST.get('in_date_year', '')
        kind = request.POST.get("kind", "")
        is_available = request.POST.get("is_available", "")
        verbose = request.POST.get("verbose", "")
        dict_resp = teacher_agents.list_teacher(full_name=full_name, code=code, name_or_code=name_or_code, is_in=is_in,
                                                in_date_year=in_date_year, kind=kind, is_available=is_available,
                                                verbose=verbose, school_id=school_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


@internal_or_403
def open_list_school(request):
    dictResp = auth_check(request, "POST", check_login=False)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        dictResp = school_agents.list_school()
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

@internal_or_403
def open_list_class(request):
    dictResp = auth_check(request, "POST", check_login=False)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        school_id = request.POST.get('school_id')
        grade_num = request.POST.get('grade_num')
        dictResp = class_agents.list_class(grade_num=grade_num, school_id=school_id)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

@internal_or_403
def open_detail_update_time(request):
    dictResp = auth_check(request, "POST", check_login=False)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        model_name = request.POST.get("model_name")
        dictResp = detail_update_time(model_name)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False, cls=RoundTripEncoder), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


@internal_or_403
def open_list_items(request):
    dictResp = auth_check(request, "POST", check_login=False)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        model_name = request.POST["model_name"]
        update_time = request.POST["update_time"]
        item_id = request.POST["item_id"]
        dictResp = list_items(model_name, update_time, item_id)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False, cls=RoundTripEncoder), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def open_list_subnet(request):
    try:
        subnet_list = list_subnet()
        if not ip_in_subnet_list(request.META['REMOTE_ADDR'], subnet_list):
            return http.HttpResponseForbidden('<h1>Forbidden</h1>')
        return HttpResponse(json.dumps(subnet_list, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def open_call_api(request):
    dictResp = auth_check(request, "POST", check_login=False)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        function_name = request.POST.get("api_name", "")

        # 获取请求用户
        user_id = request.POST.get("user_id", "")
        user_obj = Account.objects.get(id=user_id)
        request.user = user_obj

        # 获取POST参数
        parameters = request.POST.get("parameters", "")
        logger.info("[open_call_api] %s %s %s" % (function_name, user_obj.username, parameters))
        if parameters:
            new_post = request.POST.copy()
            parameters = json.loads(parameters)
            for key, value in parameters.items():
                new_post[key] = value
            request.POST = new_post

        resp = call_function(request, function_name)
        return resp

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

from user_center.apps.page.views import page_login
from django.contrib.auth.models import AnonymousUser


def open_redirect_service_url(request):
    if isinstance(request.user, AnonymousUser):
        if request.GET.get("next"):
            next_page = None
        else:
            next_page = request.path
            service = request.GET.get("srv", "")
            if service:
                next_page += "?"
                next_page += "srv=" + service

        return page_login(request, next_page=next_page)
    dictResp = auth_check(request, "GET")
    if dictResp != {}:
        return HttpResponseNotAllowed(permitted_methods="GET")
    try:
        service = request.GET["srv"]
        logger.debug("running in open redirect service url func: to get url...")
        url = redirect_service_url(request.user, service_code=service)
        logger.debug("running in open redirect service url func:get url - {}".format(url))
        return HttpResponseRedirect(url)
    except Exception as ex:
        return HttpResponseForbidden(ex.message)


def open_app_auth(request):
    dictResp = auth_check(request, "GET", check_login=False)
    if dictResp != {}:
        return HttpResponseNotAllowed(permitted_methods="GET")
    try:
        user_id = request.GET.get("userId", "")
        service_code = request.GET.get("service", "")
        err_code, url = app_auth(request=request, user_id=user_id, service_code=service_code)
        if err_code[0] != ERR_SUCCESS[0]:
            return HttpResponseForbidden(err_code[1])
        # url = login_cas("fenghuo", '827cmksgizavxknse6m6mwlrkv64ehvt', "http://127.0.0.1:8000")
        return HttpResponseRedirect(url)
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")
        # return HttpResponseForbidden()


@internal_or_403
def open_check_token(request):
    try:
        if request.user.is_authenticated():
            encoded_pwd = request.user.encoded_pwd
            pwd = xor_crypt_string(data=encoded_pwd, decode=True)
            dictResp = {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": [request.user.username, pwd]}
        else:
            dictResp = {"c": ERR_USER_AUTH[0], "m": ERR_USER_AUTH[1], "d": []}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False, cls=RoundTripEncoder), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


@internal_or_403
def open_check_wxtoken(request):
    try:
        wxtoken = request.POST.get('wxtoken', '')
        logger.info('check wxtoken %s' % wxtoken)
        username, mobile, pwd = get_username_passwd_by_wxtoken(wxtoken)
        logger.info('tell cas_server username, mobile, password: [%s], [%s], [%s]' % (username, mobile, pwd))
        dictResp = {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": [username, mobile, pwd]}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False, cls=RoundTripEncoder), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        logger.info('"open_check_wxtoken" response: %s' % dictResp)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


@internal_or_403
def open_reset_password(request):
    dictResp = auth_check(request, "POST", check_login=False)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        account_id = request.POST["account_id"]
        new_password = request.POST.get("new_password", "")
        dictResp = reset_password(account_id, new_password)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False, cls=RoundTripEncoder), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")