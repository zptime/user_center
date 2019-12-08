#!/usr/bin/python
# -*- coding=utf-8 -*-

import json
import traceback

from django.http import HttpResponse
from agents import *

from user_center.utils.request_auth import *

logger = logging.getLogger(__name__)


def api_list_parent(request):
    dictResp = auth_check(request, "POST", MODULE_PARENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        full_name = request.POST.get("full_name", "")
        student_name = request.POST.get("student_name", "")
        student_id = request.POST.get("student_id", "")
        verbose = request.POST.get("verbose", "")
        class_id = request.POST.get("class_id", "")
        grade_name = request.POST.get("grade_name", "")
        is_active = request.POST.get("is_active", "")

        dictResp = list_parent(user=request.user, full_name=full_name, student_name=student_name, student_id=student_id,
                               verbose=verbose, class_id=class_id, grade_name=grade_name, is_active=is_active)
        dictResp = paging_with_request(request, dictResp)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


# 学生个人设置界面，获取该学生的家长信息，认证流程不同
def api_list_student_parent(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        dictResp = list_student_parent(user=request.user)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_detail_parent(request):
    dictResp = auth_check(request, "POST", MODULE_PARENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        parent_id = request.POST.get("parent_id", "")
        account_id = request.POST.get("account_id", "")

        dictResp = detail_parent(request.user, parent_id, account_id)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_update_parent(request):
    dictResp = auth_check(request, "POST", MODULE_PARENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        account_id = request.POST.get("account_id", "")
        parent_info = request.POST.get("parent_info", {})
        parent_info = json.loads(parent_info)
        dictResp = update_parent(request.user, parent_info, account_id)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_add_parent(request):
    dictResp = auth_check(request, "POST", MODULE_PARENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        parent_info = request.POST.get("parent_info", {})
        parent_info = json.loads(parent_info)
        dictResp = add_parent(request.user, parent_info)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_delete_parent(request):
    dictResp = auth_check(request, "POST", MODULE_PARENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        parent_id_list = request.POST.get("parent_id_list", [])
        parent_id_list = json.loads(parent_id_list)
        dictResp = delete_parent(request.user, parent_id_list)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_active_parent(request):
    dictResp = auth_check(request, "POST", MODULE_PARENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        parent_id_list = request.POST.get("parent_id_list", "[]")
        parent_id_list = json.loads(parent_id_list)
        is_active = request.POST.get("is_active", "")
        dictResp = active_parent(request.user, parent_id_list, is_active)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_import_parent(request):
    dictResp = auth_check(request, "POST", MODULE_PARENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        file_obj = request.FILES['file']
        is_override = request.POST.get("is_override", "")

        dictResp = import_parent(request.user, file_obj, is_override)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_export_parent(request):
    dictResp = auth_check(request, "POST", MODULE_PARENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        full_name = request.POST.get("full_name", "")
        student_name = request.POST.get("student_name", "")
        student_id = request.POST.get("student_id", "")
        verbose = request.POST.get("verbose", "")
        is_active = request.POST.get("is_active", "")

        dictResp = export_parent(request.user, full_name, student_name, student_id, verbose, is_active)
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


def api_list_parent_student(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        dictResp = list_parent_student(request.user)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_delete_parent_student(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        parent_student_id = request.POST.get("parent_student_id", "")
        dictResp = delete_parent_student(request.user, parent_student_id)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_update_parent_student(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        parent_student_id = request.POST.get("parent_student_id", "")
        relation = request.POST.get("relation", "")
        status = request.POST.get("status", "")
        dictResp = update_parent_student(request.user, parent_student_id, relation, status)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_add_parent_by_student(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        mobile = request.POST.get("mobile", "")
        relation = request.POST.get("relation", "")
        messagecode = request.POST.get("messagecode", "")
        dictResp = add_parent_by_student(request.user, mobile, relation, messagecode)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")
