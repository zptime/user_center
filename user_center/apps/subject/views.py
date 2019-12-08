#!/usr/bin/python
# -*- coding=utf-8 -*-

from user_center.utils.request_auth import *
from user_center.utils.public_fun import *
import agents

logger = logging.getLogger(__name__)

def api_admin_add_subject(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        subject_name = request.POST.get("subject_name", "")

        dict_resp = agents.admin_add_subject(request.user, subject_name=subject_name)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_list_subject(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        is_active = request.POST.get("is_active", '1')
        subject_name = request.POST.get("subject_name", "")
        dict_resp = agents.admin_list_subject(user=request.user, is_active=is_active, subject_name=subject_name)
        dictResp = paging_with_request(request, dict_resp)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = dict(c=-1, m=ex.message)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_edit_subject(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        subject_id = request.POST.get("subject_id", "")
        subject_name = request.POST.get("subject_name", "")

        dict_resp = agents.admin_edit_subject(request.user, subject_id=subject_id, subject_name=subject_name)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_freeze_subject(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        subject_id_list = request.POST.get("subject_id_list", [])
        if subject_id_list:
            subject_id_list = json.loads(subject_id_list)

        dict_resp = agents.admin_freeze_subject(request.user, subject_id_list=subject_id_list)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_unfreeze_subject(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        subject_id_list = request.POST.get("subject_id_list", [])
        if subject_id_list:
            subject_id_list = json.loads(subject_id_list)

        dict_resp = agents.admin_unfreeze_subject(request.user, subject_id_list=subject_id_list)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_delete_subject(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        subject_id_list = request.POST.get("subject_id_list", [])
        if subject_id_list:
            subject_id_list = json.loads(subject_id_list)

        dict_resp = agents.admin_delete_subject(request.user, subject_id_list=subject_id_list)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_import_subject(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        file_obj = request.FILES['file']

        dictResp = agents.admin_import_subject(user=request.user, file_obj=file_obj)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_admin_export_subject(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        is_active = request.POST.get("is_active", '1')

        dictResp = agents.admin_export_subject(user=request.user, is_active=is_active)
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


def api_school_add_subject(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        subject_id_list = request.POST.get("subject_id_list", "")
        if subject_id_list:
            subject_id_list = json.loads(subject_id_list)

        dict_resp = agents.school_add_subject(user=request.user, subject_id_list=subject_id_list)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_school_check_subject(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        subject_id = request.POST.get("subject_id", "")

        dict_resp = agents.school_check_subject(user=request.user, subject_id=subject_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_school_list_subject(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        dict_resp = agents.school_list_subject(user=request.user)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_school_update_subject(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        subject_id_list = request.POST.get("subject_id_list", [])
        if subject_id_list:
            subject_id_list = json.loads(subject_id_list)

        dict_resp = agents.school_update_subject(user=request.user, subject_id_list=subject_id_list)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_school_delete_subject(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        subject_id_list = request.POST.get("subject_id_list", [])
        if subject_id_list:
            subject_id_list = json.loads(subject_id_list)

        dict_resp = agents.school_delete_subject(user=request.user, subject_id_list=subject_id_list)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_add_textbook(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        subject_id = request.POST.get("subject_id", "")
        textbook_name = request.POST.get("textbook_name", "")
        grade_num = request.POST.get("grade_num", "")

        dict_resp = agents.admin_add_textbook(user=request.user, subject_id=subject_id, textbook_name=textbook_name, grade_num=grade_num)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_list_textbook(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        is_active = request.POST.get("is_active", '1')
        subject_id_list = request.POST.get("subject_id_list", [])
        if subject_id_list:
            subject_id_list = json.loads(subject_id_list)
        grade_num_list = request.POST.get("grade_num_list", [])
        if grade_num_list:
            grade_num_list = json.loads(grade_num_list)

        dict_resp = agents.admin_list_textbook(user=request.user, is_active=is_active, subject_id_list=subject_id_list, grade_num_list=grade_num_list)
        dictResp = paging_with_request(request, dict_resp)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = dict(c=-1, m=ex.message)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_detail_textbook(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        textbook_id = request.POST.get("textbook_id", "")

        dict_resp = agents.admin_detail_textbook(user=request.user, textbook_id=textbook_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")



def api_admin_edit_textbook(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        textbook_id = request.POST.get("textbook_id", "")
        textbook_name = request.POST.get("textbook_name", "")
        grade_num = request.POST.get("grade_num", "")

        dict_resp = agents.admin_edit_textbook(user=request.user, textbook_id=textbook_id, textbook_name=textbook_name, grade_num=grade_num)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_freeze_textbook(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        textbook_id = request.POST.get("textbook_id", "")

        dict_resp = agents.admin_freeze_textbook(user=request.user, textbook_id=textbook_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_unfreeze_textbook(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        textbook_id = request.POST.get("textbook_id", "")

        dict_resp = agents.admin_unfreeze_textbook(user=request.user, textbook_id=textbook_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_delete_textbook(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        textbook_id = request.POST.get("textbook_id", "")

        dict_resp = agents.admin_delete_textbook(user=request.user, textbook_id=textbook_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_school_add_textbook(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        textbook_id = request.POST.get("textbook_id", "")

        dict_resp = agents.school_add_textbook(user=request.user, textbook_id=textbook_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_school_list_textbook(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        subject_id_list = request.POST.get("subject_id_list", [])
        if subject_id_list:
            subject_id_list = json.loads(subject_id_list)
        grade_num_list = request.POST.get("grade_num_list", [])
        if grade_num_list:
            grade_num_list = json.loads(grade_num_list)
        not_belong_flag = request.POST.get("not_belong_flag", "0")

        dict_resp = agents.school_list_textbook(user=request.user, subject_id_list=subject_id_list, grade_num_list=grade_num_list,
                                                not_belong_flag=not_belong_flag)
        dictResp = paging_with_request(request, dict_resp)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = dict(c=-1, m=ex.message)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_school_delete_textbook(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        textbook_id = request.POST.get("textbook_id", "")

        dict_resp = agents.school_delete_textbook(user=request.user, textbook_id=textbook_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_add_chapter(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        textbook_id = request.POST.get("textbook_id", "")
        chapter_name = request.POST.get("chapter_name", "")
        parent_id = request.POST.get("parent_id", None)
        sn = request.POST.get("sn", "")

        dict_resp = agents.admin_add_chapter(user=request.user, textbook_id=textbook_id, chapter_name=chapter_name,
                                               parent_id=parent_id, sn=sn)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_list_chapter(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        textbook_id = request.POST.get("textbook_id", "")

        dict_resp = agents.admin_list_chapter(user=request.user, textbook_id=textbook_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_edit_chapter(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        chapter_id = request.POST.get("chapter_id", "")
        chapter_name = request.POST.get("chapter_name", "")

        dict_resp = agents.admin_edit_chapter(user=request.user, chapter_id=chapter_id, chapter_name=chapter_name)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_move_chapter(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        chapter_id = request.POST.get("chapter_id", "")
        parent_id = request.POST.get("parent_id", None)
        sn = request.POST.get("sn", "")

        dict_resp = agents.admin_move_chapter(user=request.user, chapter_id=chapter_id, parent_id=parent_id, sn=sn)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_delete_chapter(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        chapter_id = request.POST.get("chapter_id", "")

        dict_resp = agents.admin_delete_chapter(user=request.user, chapter_id=chapter_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

