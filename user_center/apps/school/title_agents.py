# coding=utf-8
from django.db import transaction
from models import *
from user_center.apps.teacher.models import Teacher
from user_center.utils.public_fun import *
from user_center.utils.err_code import *


def init_title(school_id):
    if Title.objects.filter(school_id=school_id, del_flag=FLAG_NO).exists():
        return True
    for title in INIT_TITLE_LIST:
        Title.objects.create(school_id=school_id, name=title["name"], comments=title["comments"])
    return True


def add_title(user, name, comments=""):
    school_id = user.school_id
    name = name.strip()
    if Title.objects.filter(school_id=school_id, name=name, del_flag=FLAG_NO).exists():
        return {"c": ERR_TITLE_HAVE_EXIST_ERROR[0], "m": ERR_TITLE_HAVE_EXIST_ERROR[1], "d": []}
    Title.objects.create(school_id=school_id, name=name, comments=comments)
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}


def update_title(user, title_id, name, comments=""):
    school_id = user.school_id
    title_id = int(title_id)
    name = name.strip()
    title_obj = Title.objects.filter(id=title_id).first()
    if not title_obj:
        return {"c": ERR_TITLE_NOT_EXIST_ERROR[0], "m": ERR_TITLE_NOT_EXIST_ERROR[1], "d": []}
    elif title_obj.name in INIT_TITLE_NAME_LIST:
        return {"c": ERR_TITLE_INTERNAL_ERROR[0], "m": ERR_TITLE_INTERNAL_ERROR[1], "d": []}
    elif Title.objects.filter(school_id=school_id, name=name, del_flag=FLAG_NO).exclude(id=title_id).exists():
        return {"c": ERR_TITLE_HAVE_EXIST_ERROR[0], "m": ERR_TITLE_HAVE_EXIST_ERROR[1], "d": []}
    title_obj.name = name
    title_obj.comments = comments
    title_obj.save()
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}


@transaction.atomic
def delete_title(user, title_id_list):
    school_id = user.school_id

    title_id_list = json.loads(title_id_list)
    total_num = len(title_id_list)
    real_num = 0
    for title_id in title_id_list:
        if Teacher.objects.filter(school_id=school_id, title_id=title_id, del_flag=FLAG_NO).exists():
            if total_num == 1:
                return {"c": ERR_TITLE_HAVE_TEACHER_ERROR[0], "m": ERR_TITLE_HAVE_TEACHER_ERROR[1], "d": []}
            else:
                continue
        title_obj = Title.objects.filter(school_id=school_id, id=title_id, del_flag=FLAG_NO).first()
        if title_obj.name in INIT_TITLE_NAME_LIST:
            return {"c": ERR_TITLE_INTERNAL_ERROR[0], "m": ERR_TITLE_INTERNAL_ERROR[1], "d": []}
        if title_obj:
            title_obj.del_flag = FLAG_YES
            title_obj.save()
            real_num += 1
    if real_num < total_num:
        if total_num == 1:
            return {"c": ERR_DELETE_ERROR[0], "m": ERR_DELETE_ERROR[1], "d": []}
        else:
            err_msg = u"%d删除成功，%d删除失败" % (real_num, total_num-real_num)
            return {"c": ERR_DELETE_PART[0], "m": err_msg, "d": []}
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}


def list_title(user, exclude_class_master=""):
    school_id = user.school_id
    init_title(school_id)
    teacher_id_list = Teacher.objects.filter(school_id=school_id, title_id__isnull=False, del_flag=FLAG_NO,
                                             is_in=True).values("id", "title_id")
    teacher_title_dict = convert_list_to_dict(teacher_id_list, "title_id")
    title_list = Title.objects.filter(school_id=school_id, del_flag=FLAG_NO)
    ret_title_list = []
    for title in title_list:
        if title.id in teacher_title_dict.keys() and title.teacher_amount != len(teacher_title_dict[title.id]):
            title.teacher_amount = len(teacher_title_dict[title.id])
            title.save()
        ret_title = {"id": title.id, "name": title.name, "comments": title.comments, "teacher_amount": title.teacher_amount}
        if not ret_title["comments"]:
            ret_title["comments"] = u"自定义类型"
        if exclude_class_master and int(exclude_class_master) == FLAG_YES and title.name == TILE_NAME_CLASSMASTER:
            continue
        ret_title_list.append(ret_title)

    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": ret_title_list}

