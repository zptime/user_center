# coding=utf-8
from django.db import transaction
from django.db.models import Q
from django.conf import settings
from .models import *
from user_center.utils.err_code import *
from user_center.utils.constant import *
from user_center.apps.account.models import Account
from user_center.apps.service.models import *
from user_center.apps.teacher.agents import add_teacher
from user_center.apps.service.agents import update_admin_user
from school_agents import init_school
import logging
import json
import datetime
import os
import traceback

logger = logging.getLogger(__name__)


# 查询学校列表
def list_school(name_or_code=""):
    school_list = School.objects.filter(del_flag=FLAG_NO)
    if name_or_code:
        school_list = school_list.filter(Q(name_full__contains=name_or_code)
                                         | Q(name_simple__contains=name_or_code)
                                         | Q(code__contains=name_or_code))
    school_list = school_list.values("id", "code", "name_full", "name_simple", "type", "academic_year")

    user_center_role_obj = Role.objects.filter(service__code=settings.SERVICE_USER_CENTER, code=ADMIN_USER_TYPE_SYSTEM_ADMIN, del_flag=FLAG_NO).first()

    for school in school_list:
        admin_list = UserRole.objects.filter(school_id=school["id"], role=user_center_role_obj, del_flag=FLAG_NO).values_list("user__account__username", flat=True)
        admins_str = u"，".join(admin_list)
        school["managers"] = admins_str

    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": list(school_list)}


# 查询服务列表
def list_service(school_id="", name_or_code=""):
    service_list = Service.objects.exclude(internet_url="").filter(del_flag=FLAG_NO)
    service_id_list = []
    if name_or_code:
        service_list = service_list.filter(Q(code__contains=name_or_code) |
                                           Q(name__contains=name_or_code))
    if school_id:
        service_id_list = SchoolService.objects.filter(school_id=int(school_id)).values_list("service_id", flat=True)
    # if service_id_list:
    #     service_list = service_list.filter(id__in=service_id_list)
    service_list = service_list.values("id", "code", "name", "intranet_url", "internet_url")
    for service in service_list:
        if service["id"] in service_id_list:
            service["open"] = True
        else:
            service["open"] = False

    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": list(service_list)}


# 添加学校
@transaction.atomic
def add_school(school_code, school_name, primary_years=0, junior_years=0, senior_years=0):
    if primary_years == 0 and junior_years == 0 and senior_years == 0:
        raise Exception(u"至少选择（小学、初中、高中）学段学制")
    if not school_code or not school_name:
        raise Exception(u"学校名称和学校代码不能为空")
    if School.objects.filter(code=school_code).exists():
        raise Exception(u"学校代码已存在")
    if School.objects.filter(name_full=school_name).exists():
        raise Exception(u"学校名已存在")
    academic_year = int(primary_years) + int(junior_years) + int(senior_years)

    school_obj = School.objects.create(code=school_code, name_full=school_name, name_simple=school_name,
                                       primary_years=int(primary_years), junior_years=int(junior_years),
                                       senior_years=int(senior_years), academic_year=int(academic_year))
    init_school(school_obj=school_obj)

    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}


# 删除学校
@transaction.atomic
def delete_school(school_id):
    school_obj = School.objects.filter(id=int(school_id)).first()
    if not school_obj:
        raise Exception(u"学校不存在")
    school_obj.del_flag = FLAG_YES
    school_obj.save()

    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}


# 修改学校开通服务
@transaction.atomic
def update_school_service(school_id, service_id_list):
    service_id_list = json.loads(service_id_list)
    org_service_id_list = SchoolService.objects.filter(school_id=school_id, del_flag=FLAG_NO)\
        .values_list("service_id", flat=True)
    add_service_id_list = list(set(service_id_list) - set(org_service_id_list))
    delete_service_id_list = list(set(org_service_id_list) - set(service_id_list))

    # 删除
    SchoolService.objects.filter(school_id=school_id, service_id__in=delete_service_id_list).\
        update(del_flag=FLAG_YES, update_time=datetime.datetime.now())

    # 增加
    for service_id in add_service_id_list:
        school_service_obj = SchoolService.objects.filter(school_id=school_id, service_id=service_id).first()
        if school_service_obj:
            school_service_obj.del_flag = FLAG_NO
            school_service_obj.save()
        else:
            SchoolService.objects.create(school_id=school_id, service_id=service_id)
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}


# 添加用户中心管理员
@transaction.atomic
def add_manager(user, school_id, username, full_name=u"学校管理员", password="123456"):
    user.school_id = school_id
    teacher_data = {"username": username, "password": password, "full_name": full_name}

    # 检查学校是否开通了用户中心服务
    if not SchoolService.objects.filter(school_id=school_id, service__code=settings.SERVICE_USER_CENTER, del_flag=FLAG_NO).exists():
        raise Exception(u"该学校没有开通学校管理中心")

    if Account.objects.filter(username=username, del_flag=FLAG_NO).exists():
        raise Exception(u"该用户名已经存在")
    ret_dict = add_teacher(user, teacher_data)
    if ret_dict["c"] != ERR_SUCCESS[0]:
        return ret_dict
    teacher_id = ret_dict["d"][0]

    role_obj = Role.objects.filter(service__code=settings.SERVICE_USER_CENTER, code=ADMIN_USER_TYPE_SYSTEM_ADMIN, del_flag=FLAG_NO).first()

    role_id_list = [role_obj.id]
    role_id_list = json.dumps(role_id_list)
    update_admin_user(user, role_id_list, teacher_id)
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}



