# coding=utf-8
from django.db import transaction
from models import *
from user_center.utils.constant import *
from user_center.utils.err_code import *
from user_center.utils.request_auth import get_user_permission
from user_center.utils.public_fun import trans_to_CH, convert_list_to_dict, convert_id_to_code
from user_center.utils.file_fun import get_image_url
from user_center.apps.student.models import Student
from user_center.apps.teacher.models import Teacher, TeacherClass
from user_center.apps.teacher.agents import refresh_teacher_amount, update_teacher_master_class
import datetime
import logging
import json
import sys

logger = logging.getLogger(__name__)


# 查询在校年级
def list_class(user=None, grade_num="", teach_class="", school_id=""):
    if school_id:
        school_id = int(school_id)
    else:
        school_id = user.school.id
    class_list = Class.objects.filter(school=school_id, graduate_status=FLAG_NO, del_flag=FLAG_NO)

    # 检查用户角色班主任,只查看所带班级
    # module_list, user_role_list = get_user_permission(user)
    # if ADMIN_USER_TYPE_CLASS_ADMIN in user_role_list and len(user_role_list) == 1:
    #     teacher_obj = Teacher.objects.filter(school_id=school_id, account_id=user.id, del_flag=FLAG_NO).first()
    #     if teacher_obj:
    #         class_list = class_list.filter(id=teacher_obj.cls_id)

    if grade_num:
        class_list = class_list.filter(grade_num=int(grade_num))
    teach_cls_id_list = []
    if teach_class:  # 标记是否标记该用户教授的班级
        teacher_obj = Teacher.objects.filter(school_id=school_id, account_id=user.id, del_flag=FLAG_NO).first()
        if teacher_obj:
            teach_cls_id_list = TeacherClass.objects.filter(teacher_id=teacher_obj, del_flag=FLAG_NO).values_list("cls_id", flat=True)

    class_list = class_list.order_by('grade_num', 'class_num').\
        values('id', 'grade_num', 'enrollment_year', 'grade_name', 'class_num',
               'class_name', 'class_alias', 'student_amount')

    cls_id_list = []
    for _data in class_list:
        cls_id_list.append(_data['id'])

    teacher_list = Teacher.objects.filter(school_id=school_id, cls_id__in=cls_id_list, del_flag=FLAG_NO).\
        values('cls_id', 'id', 'full_name', "image__url")
    teacher_dict = convert_list_to_dict(teacher_list, 'cls_id')

    for _data in class_list:
        cls_id = _data['id']
        # 班级码
        _data["class_code"] = convert_id_to_code(cls_id)
        # 是否为教授的班级
        if cls_id in teach_cls_id_list:
            _data["is_teach"] = FLAG_YES
        else:
            _data["is_teach"] = FLAG_NO
        # 填写班主任信息
        class_master_list = []
        if cls_id in teacher_dict.keys():
            for teacher in teacher_dict[cls_id]:
                class_master = {"id": teacher["id"], "full_name": teacher["full_name"],
                                "image_url": get_image_url(teacher["image__url"])}
                class_master_list.append(class_master)
        _data["teacher_data"] = class_master_list
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": list(class_list)}


# 查询毕业班列表
def list_graduated_class(user, graduated_year="", gt_graduated_year="", max_num="50"):
    school_id = user.school.id
    class_list = Class.objects.filter(school=school_id, graduate_status=FLAG_YES, del_flag=FLAG_NO)
    if graduated_year:
        class_list = class_list.filter(graduate_year=int(graduated_year))
    elif gt_graduated_year:
        class_list = class_list.filter(graduate_year__gt=int(graduated_year))
    if not max_num:
        max_num = sys.maxint
    class_list = class_list.order_by('-graduate_year', 'school_period', 'class_num').\
        values('id', 'grade_num', 'enrollment_year', 'grade_name',  'class_num', 'class_name', 'class_alias',
               'student_amount', 'school_period', 'school_years', 'graduate_year')

    # 返回班级数量接近max_num，毕业年限相同的班级需在一次返回
    ret_class_list = []
    i = 0
    current_graduate_year = 0
    for class_info in class_list:
        # 班级码
        class_info["class_code"] = convert_id_to_code(class_info["id"])
        i += 1
        ret_class_list.append(class_info)
        if current_graduate_year != class_info["graduate_year"]:
            if i > max_num:
                break
            else:
                current_graduate_year = class_info["graduate_year"]

    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": ret_class_list}


# 批量添加班级
@transaction.atomic
def add_grade_class(user, grade_id, class_count):
    if not grade_id or not class_count:
        return {"c": ERR_REQUEST_PARAMETER_ERROR[0], "m": ERR_REQUEST_PARAMETER_ERROR[1], "d": []}
    grade_id = int(grade_id)
    class_count = int(class_count)

    for i in xrange(class_count):
        err_code = __add_class(user.school_id, grade_id)
        if err_code[0] != ERR_SUCCESS[0]:
            return {"c": err_code[0], "m": err_code[1], "d": []}
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}


@transaction.atomic
def add_class(user, grade_id, class_alias):
    if not grade_id:
        return {"c": ERR_REQUEST_PARAMETER_ERROR[0], "m": ERR_REQUEST_PARAMETER_ERROR[1], "d": []}
    err_code = __add_class(school_id=user.school_id, grade_id=grade_id, class_alias=class_alias)
    return {"c": err_code[0], "m": err_code[1], "d": []}


@transaction.atomic()
def __add_class(school_id, grade_id, class_num=None, class_alias=""):
    # 检查年级是否存在
    grade_id = int(grade_id)
    grade_obj = Grade.objects.filter(id=grade_id, del_flag=FLAG_NO).first()
    if not grade_obj:
        return ERR_GRADE_NOT_EXIST_ERROR

    # 检查班级是否已经存在
    if class_alias and Class.objects.filter(school_id=school_id, grade_num=grade_obj.grade_num, class_alias=class_alias, del_flag=FLAG_NO).exists():
        return ERR_CLASS_HAVE_EXIST_ERROR
    if class_num and Class.objects.filter(school_id=school_id, grade_num=grade_obj.grade_num, class_num=int(class_num), del_flag=FLAG_NO).exists():
        return ERR_CLASS_HAVE_EXIST_ERROR

    # 相关班级相关数据
    grade_num = grade_obj.grade_num
    grade_name = grade_obj.grade_name
    period_grade_num = grade_obj.period_grade_num
    enrollment_year = __get_enrollment_year(school_id, period_grade_num)
    school_period = grade_obj.school_period
    school_years = grade_obj.school_years
    if not class_num:  # 获取班级序号
        max_class_obj = Class.objects.filter(school_id=school_id, grade_num=grade_num, del_flag=FLAG_NO).\
            order_by("-class_num").first()
        if max_class_obj:
            class_num = max_class_obj.class_num + 1
        else:
            class_num = 1
    else:
        class_num = int(class_num)
    class_name = __get_class_name(school_id=school_id, grade_num=grade_num, class_num=class_num,
                                  period_grade_num=period_grade_num, school_period=school_period)  # 获取班级名称

    Class.objects.create(school_id=school_id, class_num=class_num, class_name=class_name, grade_num=grade_num,
                         grade_name=grade_name, enrollment_year=enrollment_year, period_grade_num=period_grade_num,
                         class_alias=class_alias, school_period=school_period, school_years=school_years)
    refresh_class_amount(school_id, [grade_obj])
    return ERR_SUCCESS


def init_class(school_obj):
    class_list = Class.objects.filter(school=school_obj, del_flag=FLAG_NO)
    for class_obj in class_list:
        if not class_obj.grade_num:
            class_obj.grade_num = 6
        grade_obj = Grade.objects.filter(grade_num=class_obj.grade_num, del_flag=FLAG_NO).first()
        if not grade_obj:
            raise Exception(u"没有找到对应的年级grade_num=%d" % class_obj.grade_num)
        update_class_grade(school_obj.id, class_obj, grade_obj)


# 更新班级年级
def update_class_grade(school_id, cls_obj, grade_obj):
    # 相关班级相关数据
    grade_num = grade_obj.grade_num
    grade_name = grade_obj.grade_name
    period_grade_num = grade_obj.period_grade_num
    school_period = grade_obj.school_period
    school_years = grade_obj.school_years
    class_name = __get_class_name(school_id=school_id, grade_num=grade_num, class_num=cls_obj.class_num,
                                  period_grade_num=period_grade_num, school_period=school_period)  # 获取班级名称
    cls_obj.class_name = class_name
    cls_obj.grade_num = grade_num
    cls_obj.grade_name = grade_name
    cls_obj.period_grade_num = period_grade_num
    cls_obj.school_period = school_period
    cls_obj.school_years = school_years
    cls_obj.save()


def graduate_class(cls_obj, graduate_year):
    cls_obj.graduate_year = graduate_year
    cls_obj.graduate_status = FLAG_YES
    cls_obj.save()


def undo_graduate_class(cls_obj):
    cls_obj.graduate_year = 0
    cls_obj.graduate_status = FLAG_NO
    cls_obj.save()


def __get_enrollment_year(school_id, period_grade_num):
    manage_data = UpdateManagement.objects.filter(school_id=school_id, del_flag=FLAG_NO).\
        values_list('cur_term', 'update_month', 'update_day').first()
    if not manage_data:
        raise Exception(ERR_TEAM_NOT_EXIST_ERROR[1])
    cur_term, update_month, update_day = tuple(manage_data)

    enrollment_year = cur_term - period_grade_num + 1
    return enrollment_year


def __get_class_name(school_id, grade_num, class_num, period_grade_num, school_period):
    class_style = None
    if school_period == SCHOOL_PERIOD_PRIMARY[0]:
        class_style = SchoolClassStyle.objects.\
            filter(school=school_id, primary_class_style__isnull=False, del_flag=FLAG_NO).first().primary_class_style
    elif school_period == SCHOOL_PERIOD_JUNIOR[0]:
        class_style = SchoolClassStyle.objects.\
            filter(school=school_id, junior_class_style__isnull=False, del_flag=FLAG_NO).first().junior_class_style
    elif school_period == SCHOOL_PERIOD_SENIOR[0]:
        class_style = SchoolClassStyle.objects.\
            filter(school=school_id, senior_class_style__isnull=False, del_flag=FLAG_NO).first().senior_class_style
    if not class_style:
        raise Exception(ERR_CLASS_NO_STYLE_ERROR[1])
    pattern = class_style.pattern
    args = class_style.args
    grade_num_cap = trans_to_CH(grade_num)
    class_num_cap = trans_to_CH(class_num)
    period_grade_num_cap = trans_to_CH(period_grade_num)

    args = args.split(";")
    values = []
    for arg in args:
        if arg in CLASS_STYLE_ARGS_LIST:
            values.append(eval(arg))
    class_name = pattern % tuple(values)
    return class_name


@transaction.atomic
def delete_class(user, id_list):
    school_id = user.school_id
    id_list = json.loads(id_list)
    class_id_list = map(lambda x: int(x), id_list)

    err_msg_list = []
    total_num = len(class_id_list)
    real_num = 0
    for class_id in class_id_list:
        class_obj = Class.objects.filter(school_id=school_id, id=class_id, del_flag=FLAG_NO).first()
        if Student.objects.filter(school_id=school_id, cls_id=class_id, del_flag=FLAG_NO).exists():
            err_msg = u"【%s】中有学生，无法删除" % class_obj.class_name
            err_msg_list.append(err_msg)
            continue
        # 取消该班级的班主任
        Teacher.objects.filter(school_id=school_id, cls_id=class_id, del_flag=FLAG_NO).update(cls=None, update_time=datetime.datetime.now())
        # 清除教师班级关联
        TeacherClass.objects.filter(cls_id=class_id, del_flag=FLAG_NO).update(del_flag=FLAG_YES, update_time=datetime.datetime.now())
        # 删除该班级
        if class_obj:
            grade_num = class_obj.grade_num
            class_obj.del_flag=FLAG_YES
            class_obj.save()
            # 重新调整班级序号
            class_list = Class.objects.filter(school_id=school_id, grade_num=grade_num, del_flag=FLAG_NO).order_by('class_num')
            class_num = 1
            for cls in class_list:
                cls.class_num = class_num
                cls.class_name = __get_class_name(school_id=school_id, grade_num=cls.grade_num,
                                                  class_num=cls.class_num, period_grade_num=cls.period_grade_num,
                                                  school_period=cls.school_period)
                cls.save()
                class_num += 1
            real_num += 1
    if real_num >= 1:
        refresh_class_amount(school_id)
        refresh_teacher_amount(school_id)
    if total_num == real_num:
        return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}
    elif total_num == 1:
        return {"c": ERR_DELETE_ERROR[0], "m": err_msg_list[0], "d": []}
    else:
        return {"c": ERR_DELETE_PART[0], "m": ERR_DELETE_PART[1], "d": err_msg_list}


# 支持更新班级别名和班主任
@transaction.atomic
def update_class(user, class_id, class_alias="", teacher_ids=""):
    class_id = int(class_id)
    school_id = user.school.id
    teacher_ids = json.loads(teacher_ids)
    if class_alias:
        cls_obj = Class.objects.filter(school_id=school_id, id=class_id, del_flag=FLAG_NO).first()
        cls_obj.class_alias = class_alias
        cls_obj.save()
    if teacher_ids:
        Teacher.objects.filter(school_id=school_id, cls_id=class_id, del_flag=FLAG_NO).update(cls_id=None, update_time=datetime.datetime.now())
        Teacher.objects.filter(school_id=school_id, id__in=teacher_ids, del_flag=FLAG_NO).update(cls_id=class_id, update_time=datetime.datetime.now())
        title_obj = Title.objects.filter(school_id=school_id, name=TILE_NAME_CLASSMASTER, del_flag=NO).first()
        refresh_teacher_amount(school_id, [title_obj])
    # 更新所授班级
    update_teacher_master_class(teacher_ids, int(class_id))
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}


def list_class_style(user):
    school_id = user.school_id

    have_primary = True
    have_junior = True
    have_senior = True
    if school_id:
        school_class_style = SchoolClassStyle.objects.filter(school_id=school_id, del_flag=FLAG_NO).first()
        if not school_class_style:
            return {"c": ERR_SCHOOL_NOT_INIT_ERROR[0], "m": ERR_SCHOOL_NOT_INIT_ERROR[1], "d": []}
        if not school_class_style.primary_class_style:
            have_primary = False
        if not school_class_style.junior_class_style:
            have_junior = False
        if not school_class_style.senior_class_style:
            have_senior = False
    ret_class_style = {"primary": [], "junior": [], "senior": []}
    class_style_list = ClassStyle.objects.filter(del_flag=FLAG_NO).values("id", "style_example", "school_period")
    for class_style in class_style_list:
        if have_primary and class_style["school_period"] == SCHOOL_PERIOD_PRIMARY[0]:
            ret_class_style["primary"].append(class_style)
        elif have_junior and class_style["school_period"] == SCHOOL_PERIOD_JUNIOR[0]:
            ret_class_style["junior"].append(class_style)
        elif have_senior and class_style["school_period"] == SCHOOL_PERIOD_SENIOR[0]:
            ret_class_style["senior"].append(class_style)
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": [ret_class_style]}


def detail_class_style(user):
    school_id = user.school_id
    school_class_style = SchoolClassStyle.objects.filter(school_id=school_id, del_flag=FLAG_NO).first()
    if not school_class_style:
        return {"c": ERR_SCHOOL_NOT_INIT_ERROR[0], "m": ERR_SCHOOL_NOT_INIT_ERROR[1], "d": []}
    ret_class_style = {"primary": {}, "junior": {}, "senior": {}}
    if school_class_style.primary_class_style:
        class_style = school_class_style.primary_class_style
        ret_class_style["primary"] = {"id": class_style.id,
                                      "style_example": class_style.style_example,
                                      "school_period": class_style.school_period}
    if school_class_style.junior_class_style:
        class_style = school_class_style.junior_class_style
        ret_class_style["junior"] = {"id": class_style.id,
                                     "style_example": class_style.style_example,
                                     "school_period": class_style.school_period}
    if school_class_style.senior_class_style:
        class_style = school_class_style.senior_class_style
        ret_class_style["senior"] = {"id": class_style.id,
                                     "style_example": class_style.style_example,
                                     "school_period": class_style.school_period}

    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": [ret_class_style]}


@transaction.atomic()
def update_class_style(school_id, primary_class_style_id="", junior_class_style_id="", senior_class_style_id=""):
    school_class_style = SchoolClassStyle.objects.filter(school_id=school_id, del_flag=FLAG_NO).first()
    if not school_class_style:
        return {"c": ERR_SCHOOL_NOT_INIT_ERROR[0], "m": ERR_SCHOOL_NOT_INIT_ERROR[1], "d": []}
    if primary_class_style_id:
        school_class_style.primary_class_style_id = int(primary_class_style_id)
    else:
        school_class_style.primary_class_style = None
    if junior_class_style_id:
        school_class_style.junior_class_style_id = int(junior_class_style_id)
    else:
        school_class_style.junior_class_style = None
    if senior_class_style_id:
        school_class_style.senior_class_style_id = int(senior_class_style_id)
    else:
        school_class_style.senior_class_style = None
    school_class_style.save()

    # 更新所有在校
    class_list = Class.objects.filter(school_id=school_id, graduate_status=FLAG_NO, del_flag=FLAG_NO)
    for cls_obj in class_list:
        cls_obj.class_name = __get_class_name(school_id=school_id, grade_num=cls_obj.grade_num,
                                              class_num=cls_obj.class_num, period_grade_num=cls_obj.period_grade_num,
                                              school_period=cls_obj.school_period)
        cls_obj.save()
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}


# 更新年级中的班级总数
def refresh_class_amount(school_id, grade_obj_list=[]):
    if not grade_obj_list:
        grade_obj_list = Grade.objects.filter(school_id=school_id, del_flag=FLAG_NO)
    for grade_obj in grade_obj_list:
        class_amount = Class.objects.filter(school_id=school_id, grade_num=grade_obj.grade_num, del_flag=FLAG_NO).count()
        grade_obj.class_amount = class_amount
        grade_obj.save()
