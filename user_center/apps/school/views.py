# coding=utf-8

from django.http import HttpResponse
from user_center.utils.request_auth import *
from user_center.utils.constant import *
from user_center.utils.public_fun import paging_with_request
import class_agents
import title_agents
import school_agents
import admin_agents
import logging
import json
import traceback


logger = logging.getLogger(__name__)


############################ 班级管理 ############################################################

def api_list_class_style(request):
    dict_resp = auth_check(request, method="POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    try:
        dict_resp = class_agents.list_class_style(request.user)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_update_class_style(request):
    dict_resp = auth_check(request, method="POST", module=MODULE_SYSTEM)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    try:
        primary_class_style_id = request.POST.get('primary_class_style_id')
        junior_class_style_id = request.POST.get('junior_class_style_id')
        senior_class_style_id = request.POST.get('senior_class_style_id')
        dict_resp = class_agents.update_class_style(request.user.school_id, primary_class_style_id, junior_class_style_id, senior_class_style_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_detail_class_style(request):
    dict_resp = auth_check(request, method="POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    try:
        dict_resp = class_agents.detail_class_style(request.user)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_list_class(request):
    dict_resp = auth_check(request, method="POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    try:
        grade_num = request.POST.get("grade_num")
        teach_class = request.POST.get("teach_class")
        dict_resp = class_agents.list_class(request.user, grade_num, teach_class)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_list_graduated_class(request):
    dict_resp = auth_check(request, method="POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    try:
        graduated_year = request.POST.get("graduated_year")
        gt_graduated_year = request.POST.get("gt_graduated_year")
        max_num = request.POST.get("max_num")
        dict_resp = class_agents.list_graduated_class(request.user, graduated_year, gt_graduated_year, max_num)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_add_grade_class(request):
    dict_resp = auth_check(request, "POST", MODULE_SYSTEM)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    try:
        grade_id = request.POST.get('grade_id')
        class_count = request.POST.get('class_count')
        dict_resp = class_agents.add_grade_class(request.user, grade_id, class_count)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_add_class(request):
    dict_resp = auth_check(request, method="POST", module=MODULE_SYSTEM)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    try:
        grade_id = request.POST.get("grade_id")
        class_alias = request.POST.get("class_alias", "")
        dict_resp = class_agents.add_class(request.user, grade_id, class_alias)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrinfo = traceback.format_exc()
        logger.error(sErrinfo)
        dict_resp = {"c":-1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_delete_class(request):
    dict_resp = auth_check(request, method="POST", module=MODULE_SYSTEM)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    try:
        id_list = request.POST.get("id_list")
        dict_resp = class_agents.delete_class(request.user, id_list)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_update_class(request):
    dict_resp = auth_check(request, method="POST", module=MODULE_SYSTEM)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        class_id = request.POST.get('class_id')
        class_alias = request.POST.get('class_alias')
        teacher_ids = request.POST.get('teacher_ids', '[]')
        dict_resp = class_agents.update_class(request.user, class_id, class_alias, teacher_ids)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrinfo = traceback.format_exc()
        logger.error(sErrinfo)
        dict_resp = {"c":-1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

############################ 年级管理 ############################################################


def api_list_grade(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    try:
        data_grade = school_agents.list_grade(request.user)
        dict_resp = dict(c=ERR_SUCCESS[0], m=ERR_SUCCESS[1], d=data_grade)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_annually_update(request):
    dict_resp = auth_check(request, "POST", MODULE_SYSTEM)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    try:
        dict_resp = school_agents.upgrade_school_term(request.user.school_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_undo_update(request):
    dict_resp = auth_check(request, "POST", MODULE_SYSTEM)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    try:
        dict_resp = school_agents.degrade_school_term(request.user.school_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_config_update_time(request):
    dict_resp = auth_check(request, "POST", module=MODULE_SYSTEM)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        month = request.POST.get('month')
        day = request.POST.get('day')
        dict_resp = school_agents.config_update_time(request.user, month, day)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_display_update_time(request):
    dict_resp = auth_check(request, "POST", module=MODULE_SYSTEM)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        dict_resp = school_agents.display_update_time(request.user)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_display_current_term(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        dict_resp = school_agents.display_current_term(request.user)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_detail_school(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        dict_resp = school_agents.detail_school(request.user)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_update_learning_period(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        primary_years = request.POST.get("primary_years", "")
        junior_years = request.POST.get("junior_years", "")
        senior_years = request.POST.get("senior_years", "")
        dict_resp = school_agents.update_learning_period(request.user.school_id, primary_years, junior_years, senior_years)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_add_title(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        name = request.POST.get("name", "")
        comment = request.POST.get("comment", "")
        dict_resp = title_agents.add_title(request.user, name, comment)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_update_title(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        tile_id = request.POST.get("tile_id", "")
        name = request.POST.get("name", "")
        comment = request.POST.get("comment", "")
        dict_resp = title_agents.update_title(request.user, tile_id, name, comment)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_delete_title(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        id_list = request.POST.get("id_list", "")
        dict_resp = title_agents.delete_title(request.user, id_list)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_list_title(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        exclude_class_master = request.POST.get("exclude_class_master", "")
        dict_resp = title_agents.list_title(request.user, exclude_class_master)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_list_school(request):
    dict_resp = auth_check(request, method="POST", is_admin=True)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        name_or_code = request.POST.get("name_or_code", "")
        dict_resp = admin_agents.list_school(name_or_code)
        dict_resp = paging_with_request(request, dict_resp)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_list_service(request):
    dict_resp = auth_check(request, method="POST", is_admin=True)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        school_id = request.POST.get("school_id", "")
        name_or_code = request.POST.get("name_or_code", "")
        dict_resp = admin_agents.list_service(school_id=school_id, name_or_code=name_or_code)
        dict_resp = paging_with_request(request, dict_resp)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_add_school(request):
    dict_resp = auth_check(request, method="POST", is_admin=True)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        school_code = request.POST.get("school_code", "")
        school_name = request.POST.get("school_name", "")
        primary_years = request.POST.get("primary_years", "")
        junior_years = request.POST.get("junior_years", "")
        senior_years = request.POST.get("senior_years", "")
        dict_resp = admin_agents.add_school(school_code=school_code, school_name=school_name,
                                            primary_years=primary_years, junior_years=junior_years,
                                            senior_years=senior_years)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_update_school_service(request):
    dict_resp = auth_check(request, method="POST", is_admin=True)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        school_id = request.POST.get("school_id", "")
        service_id_list = request.POST.get("service_id_list", "")
        dict_resp = admin_agents.update_school_service(school_id, service_id_list)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_add_manager(request):
    dict_resp = auth_check(request, method="POST", is_admin=True)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        school_id = request.POST.get("school_id", "")
        username = request.POST.get("username", "")
        full_name = request.POST.get("full_name", "")
        password = request.POST.get("password", "")
        dict_resp = admin_agents.add_manager(user=request.user, school_id=school_id, username=username,
                                             full_name=full_name, password=password)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_admin_delete_school(request):
    dict_resp = auth_check(request, method="POST", is_admin=True)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        school_id = request.POST.get("school_id", "")
        dict_resp = admin_agents.delete_school(school_id=school_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")