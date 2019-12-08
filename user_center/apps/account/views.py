#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django_cas_ng import views as cas_views
from user_center.utils.request_auth import *
from user_center.utils.gen_response import *
from user_center.utils.constant import *
from user_center.utils.err_code import *
from django.dispatch import receiver
from django_cas_ng import signals as cas_signals
import agents
import json
import traceback
import logging

logger = logging.getLogger(__name__)


# @receiver(cas_signals.cas_user_authenticated)
# def login_callback(sender, **kwargs):
#     # print sender
#     attr = kwargs["attributes"]
#     username = attr["username"]
#     account_id = attr["account_id"]


def api_login(request):
    dictResp = auth_check(request, "POST", check_login=False)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if agents.login(request, login_name=username, password=password):

            dictResp = {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1]}
        else:
            dictResp = {"c": ERR_LOGIN_FAIL[0], "m": ERR_LOGIN_FAIL[1]}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_logout(request):
    dictResp = auth_check(request, "POST", check_login=False)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        cas_views.callback(request)
        dictResp = {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1]}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_reset_password(request):
    dictResp = auth_check(request, "POST", check_login=False)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        account_id = request.POST.get('account_id', '')
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        dictResp = agents.reset_password(request.user, account_id, new_password, old_password)

        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_batch_reset_password(request):
    dictResp = auth_check(request, "POST", check_login=False)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        account_id_list = request.POST.get('account_id_list', "")
        account_id_list = json.loads(account_id_list)
        new_password = request.POST.get('new_password', '')
        dictResp = agents.batch_reset_password(request.user, account_id_list, new_password)

        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_check_username(request):
    dictResp = auth_check(request, "POST", check_login=False)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        username = request.POST['username']
        dictResp = agents.check_username(username)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_detail_account(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        username = request.POST.get('username', "")
        dictResp = agents.api_detail_account(request.user)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_list_user_type(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        account_id = request.POST.get('account_id', "")
        dictResp = agents.api_list_user_type(request.user)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_change_user_type(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        school_id = request.POST.get('school_id', "")
        type_id = request.POST.get('type_id', "")
        dictResp = agents.api_change_user_type(request.user, school_id, type_id)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_reset_mobile(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        new_mobile = request.POST['new_mobile']
        messagecode = request.POST['messagecode']
        dictResp = agents.reset_mobile(request.user, new_mobile, messagecode)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_detail_account_by_mobile(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        mobile = request.POST['mobile']
        dictResp = agents.detail_account_by_mobile(mobile)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")