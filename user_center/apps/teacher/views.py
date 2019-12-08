# coding=utf-8

from django.http import HttpResponse
from user_center.utils.request_auth import *
from . import agents
from user_center.utils.public_fun import *
import logging
import json
import traceback

logger = logging.getLogger(__name__)


def api_list_teacher(request):
    dict_resp = auth_check(request, "POST", module=MODULE_TEACHER)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        full_name = request.POST.get("full_name", "")
        code = request.POST.get("code", "")
        name_or_code = request.POST.get("name_or_code", "")
        is_in = request.POST.get("is_in", "")
        in_date_year = request.POST.get('in_date_year', '')
        kind = request.POST.get("kind", "")
        is_available = request.POST.get("is_available", "")
        # grade_name = request.POST.get("grade_name", "")
        # class_id = request.POST.get("class_id", "")
        # enrollment_year = request.POST.get("enrollment_year", "")
        verbose = request.POST.get("verbose", "")
        title = request.POST.get("title", "")
        dict_resp = agents.list_teacher(user=request.user, full_name=full_name, code=code, name_or_code=name_or_code,
                                        is_in=is_in, in_date_year=in_date_year, kind=kind, is_available=is_available,
                                        verbose=verbose, title=title)
        dictResp = paging_with_request(request, dict_resp)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_update_teacher(request):
    dict_resp = auth_check(request, "POST", module=MODULE_TEACHER)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        teacher_info = request.POST.get('teacher_info')
        account_id = request.POST.get("account_id", "")
        teacher_info = json.loads(teacher_info)
        dict_resp = agents.update_teacher(request.user, teacher_info, account_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_add_teacher(request):
    dict_resp = auth_check(request, "POST", module=MODULE_TEACHER)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        teacher_info = request.POST.get("teacher_info")
        teacher_info = json.loads(teacher_info)
        dict_resp = agents.add_teacher(request.user, teacher_info)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_import_teacher(request):
    dict_resp = auth_check(request, "POST", module=MODULE_TEACHER)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        file_obj = request.FILES['file']
        is_override = request.POST.get("is_override", "")

        dict_resp = agents.import_teacher(request.user, file_obj, is_override)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_export_teacher(request):
    dictResp = auth_check(request, "POST", module=MODULE_TEACHER)
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        full_name = request.POST.get("full_name", "")
        code = request.POST.get("code", "")
        name_or_code = request.POST.get("name_or_code", "")
        is_in = request.POST.get("is_in", "")
        in_date_year = request.POST.get('in_date_year', '')
        kind = request.POST.get("kind", "")
        is_available = request.POST.get("is_available", "")
        grade_name = request.POST.get("grade_name", "")
        # class_id = request.POST.get("class_id", "")
        # enrollment_year = request.POST.get("enrollment_year", "")
        verbose = request.POST.get("verbose", "")

        dictResp = agents.export_teacher(request.user, full_name, code, name_or_code, is_in, in_date_year, kind, is_available, verbose)
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


def api_detail_teacher(request):
    dict_resp = auth_check(request, "POST", module=MODULE_TEACHER)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        id = request.POST.get('teacher_id')
        account_id = request.POST.get("account_id", "")
        dict_resp = agents.detail_teacher(id, account_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_delete_teacher(request):
    dict_resp = auth_check(request, "POST", module=MODULE_TEACHER)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        id_list = request.POST.get('teacher_id_list', '[]')
        id_list = json.loads(id_list)
        dict_resp = agents.delete_teacher(request.user, id_list)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_leave_teacher(request):
    dict_resp = auth_check(request, "POST", module=MODULE_TEACHER)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        teacher_id_list = request.POST.get('teacher_id_list', '')
        id_list = json.loads(teacher_id_list)
        is_leave = request.POST.get('is_leave', '')
        dict_resp = agents.leave_teacher(request.user, id_list, is_leave)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_list_teacher_class(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        teacher_id = request.POST.get("teacher_id", "")
        dict_resp = agents.list_teacher_class(request.user, teacher_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_add_teacher_class(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        teacher_id = request.POST.get("teacher_id", "")
        class_id_list = request.POST.get("class_id_list", "")
        dict_resp = agents.add_teacher_class(request.user, teacher_id, class_id_list)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_delete_teacher_class(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        teacher_id = request.POST.get("teacher_id", "")
        class_id_list = request.POST.get("class_id_list", "")
        dict_resp = agents.delete_teacher_class(request.user, teacher_id, class_id_list)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_list_teacher_textbook(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        teacher_id = request.POST.get("teacher_id", "")
        subject_id = request.POST.get("subject_id", "")
        dict_resp = agents.list_teacher_textbook(request.user, teacher_id, subject_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_add_teacher_textbook(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        teacher_id = request.POST.get("teacher_id", "")
        textbook_id_list = request.POST.get("textbook_id_list", "")
        dict_resp = agents.add_teacher_textbook(request.user, teacher_id, textbook_id_list)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_update_teacher_textbook(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        teacher_id = request.POST.get("teacher_id", "")
        textbook_id = request.POST.get("textbook_id", "")
        dict_resp = agents.update_teacher_textbook(request.user, teacher_id, textbook_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_delete_teacher_textbook(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        teacher_id = request.POST.get("teacher_id", "")
        textbook_id_list = request.POST.get("textbook_id_list", "")
        dict_resp = agents.delete_teacher_textbook(request.user, teacher_id, textbook_id_list)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")