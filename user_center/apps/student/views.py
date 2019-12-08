#!/usr/bin/python
# -*- coding=utf-8 -*-

import json
import traceback

from django.http import HttpResponse
from agents import *

from user_center.utils.request_auth import *

logger = logging.getLogger(__name__)


def api_list_student(request):
    dictResp = auth_check(request, "POST", MODULE_STUDENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")
    try:
        full_name = request.POST.get("full_name", "")
        code = request.POST.get("code", "")
        name_or_code = request.POST.get("name_or_code", "")
        is_in = request.POST.get("is_in", "")
        kind = request.POST.get("kind", "")
        is_available = request.POST.get("is_available", "")
        grade_name = request.POST.get("grade_name", "")
        class_id = request.POST.get("class_id", "")
        enrollment_year = request.POST.get("enrollment_year", "")
        graduated_year = request.POST.get("graduated_year", "")
        verbose = request.POST.get("verbose", "")

        dictResp = list_student(user=request.user, full_name=full_name, code=code, name_or_code=name_or_code,
                                is_in=is_in, kind=kind, is_available=is_available, grade_name=grade_name,
                                class_id=class_id, enrollment_year=enrollment_year, graduated_year=graduated_year,
                                verbose=verbose)
        dictResp = paging_with_request(request, dictResp)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_detail_student(request):
    dictResp = auth_check(request, "POST", MODULE_STUDENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        student_id = request.POST.get("student_id", "")
        account_id = request.POST.get("account_id", "")
        dictResp = detail_student(request.user, student_id, account_id)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_update_student(request):
    dictResp = auth_check(request, "POST", MODULE_STUDENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        student_info = request.POST.get("student_info", {})
        account_id = request.POST.get("account_id", "")
        student_info = json.loads(student_info)
        dictResp = update_student(request.user, student_info, account_id)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_add_student(request):
    dictResp = auth_check(request, "POST", MODULE_STUDENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        student_info = request.POST.get("student_info", {})
        student_info = json.loads(student_info)
        dictResp = add_student(request.user, student_info)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_delete_student(request):
    dictResp = auth_check(request, "POST", MODULE_STUDENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        student_id_list = request.POST.get("student_id_list", [])
        student_id_list = json.loads(student_id_list)
        dictResp = delete_student(request.user, student_id_list)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_update_student_class(request):
    dictResp = auth_check(request, "POST", MODULE_STUDENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        student_id_list = request.POST.get("student_id_list", "")
        student_id_list = json.loads(student_id_list)
        class_id = request.POST.get("class_id", "")
        dictResp = update_student_class(request.user, student_id_list, class_id)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_import_student(request):
    dictResp = auth_check(request, "POST", MODULE_STUDENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        file_obj = request.FILES['file']
        is_override = request.POST.get("is_override", "")

        dictResp = import_student(request.user, file_obj, is_override)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_export_student(request):
    dictResp = auth_check(request, "POST", MODULE_STUDENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
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

        dictResp = export_student(user=request.user, full_name=full_name, code=code, name_or_code=name_or_code,
                                  is_in=is_in, kind=kind, is_available=is_available, grade_name=grade_name,
                                  class_id=class_id, enrollment_year=enrollment_year, verbose=verbose)
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


def api_add_student_class_application(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        class_code = request.POST.get("class_code", "")
        comments = request.POST.get("comments", "")

        dictResp = add_student_class_application(request.user, class_code, comments)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_list_student_class_application(request):
    dictResp = auth_check(request, "POST", MODULE_STUDENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        status = request.POST.get("status", "")
        student_name = request.POST.get("student_name", "")

        dictResp = list_student_class_application(request.user, status, student_name)
        dictResp = paging_with_request(request, dictResp)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_delete_student_class_application(request):
    dictResp = auth_check(request, "POST", MODULE_STUDENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        id_list = request.POST.get("id_list", "")
        id_list = json.loads(id_list)

        dictResp = delete_student_class_application(request.user, id_list)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_update_student_class_application(request):
    dictResp = auth_check(request, "POST", MODULE_STUDENT)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        status = request.POST.get("status", "")
        id_list = request.POST.get("id_list", "")
        id_list = json.loads(id_list)

        dictResp = update_student_class_application(request.user, status, id_list)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_detail_student_class_application(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        dictResp = detail_student_class_application(request.user)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")