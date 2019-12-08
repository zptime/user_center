#!/usr/bin/python
# -*- coding=utf-8 -*-

import json
import traceback

from django.http import HttpResponse
from user_center.utils.ipaddr_fun import ip_in_subnet_list
from agents import *

from user_center.utils.request_auth import *

logger = logging.getLogger(__name__)


def api_list_admin_user(request):
    dictResp = auth_check(request, "POST", MODULE_SYSTEM)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        service_name = request.POST.get("service_name", "")
        user_name = request.POST.get("user_name", "")

        dictResp = list_admin_user(request.user, service_name, user_name)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_list_admin_role(request):
    dictResp = auth_check(request, "POST", MODULE_SYSTEM)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        teacher_id = request.POST.get("teacher_id", "")

        dictResp = list_admin_role(request.user, teacher_id)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_update_admin_user(request):
    dictResp = auth_check(request, "POST", MODULE_SYSTEM)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        teacher_id = request.POST.get("teacher_id", "")
        role_id_list = request.POST.get("role_id_list", "")
        dictResp = update_admin_user(request.user, role_id_list, teacher_id)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_delete_admin_user(request):
    dictResp = auth_check(request, "POST", MODULE_SYSTEM)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        user_role_id_list = request.POST.get("user_role_id_list", "")
        dictResp = delete_admin_user(request.user, user_role_id_list)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_list_role_user(request):
    dictResp = auth_check(request, "POST", MODULE_SYSTEM)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        service_name = request.POST.get("service_name", "")

        dictResp = list_role_user(request.user, service_name)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_update_role_user(request):
    dictResp = auth_check(request, "POST", MODULE_SYSTEM)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        role_id = request.POST.get("role_id", "")
        user_list = request.POST.get("user_list", "")
        user_list = json.loads(user_list)
        dictResp = update_role_user(request.user, role_id, user_list)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_list_service_apps(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:

        dictResp = list_service_apps(request.user)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_export_admin_user(request):
    dictResp = auth_check(request, "POST", MODULE_SYSTEM)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        dictResp = export_admin_user(user=request.user)
        if dictResp["c"] != ERR_SUCCESS[0]:
            return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")
        file_path = dictResp["d"][0]
        response = gen_file_reponse(file_path)
        return response

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")