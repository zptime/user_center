# coding=utf-8
from django.db import transaction
from .models import *
from user_center.utils.err_code import *
from user_center.utils.constant import *
from django.conf import settings
from django.db.utils import ProgrammingError
from user_center.utils.request_auth import get_user_permission
from user_center.apps.teacher.models import Teacher
from class_agents import graduate_class, undo_graduate_class, update_class_grade, refresh_class_amount, update_class_style
import datetime
import logging
import json
import os
import traceback

logger = logging.getLogger(__name__)


# 查询学校列表
def list_school():
    school_list = School.objects.filter(del_flag=FLAG_NO).values("id", "code", "name_full")
    # ret_school_list
    for school in school_list:
        school["id"] = str(school["id"])
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": list(school_list)}


# 显示学校年级列表
def list_grade(user):
    grade_list = Grade.objects.filter(school=user.school, del_flag=FLAG_NO)
    # 检查用户角色班主任,只查看所带班级
    # module_list, user_role_list = get_user_permission(user)
    # if ADMIN_USER_TYPE_CLASS_ADMIN in user_role_list and len(user_role_list) == 1:
    #     teacher_obj = Teacher.objects.filter(school_id=user.school_id, account_id=user.id, del_flag=FLAG_NO).first()
    #     if teacher_obj:
    #         grade_list = grade_list.filter(id=teacher_obj.cls.grade_num)

    grade_list = grade_list.order_by('grade_num').values("id", 'grade_num', 'grade_name', 'class_amount',
                                                         'period_grade_num', 'school_period', 'school_years')
    grade_list = list(grade_list)
    return grade_list


# 查询学校详情
def detail_school(user, school_id=""):
    if school_id:
        school_id = int(school_id)
    else:
        school_id = user.school_id

    school_obj = School.objects.filter(id=school_id).first()
    if not school_obj:
        return {"c": ERR_SCHOOL_ID_ERR[0], "m": ERR_SCHOOL_ID_ERR[1], "d": []}
    ret_school_info = {"id": school_obj.id, "code": school_obj.code, "name_full": school_obj.name_full,
                       "name_simple": school_obj.name_simple, "type": school_obj.type,
                       "academic_year": school_obj.academic_year, "primary_years": school_obj.primary_years,
                       "junior_years": school_obj.junior_years, "senior_years": school_obj.senior_years}
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": [ret_school_info]}


# 学制学段
@transaction.atomic
def update_learning_period(school_id, primary_years, junior_years, senior_years):
    school_obj = School.objects.filter(id=school_id, del_flag=FLAG_NO).first()
    if not school_obj:
        return {"c": ERR_SCHOOL_ID_ERR[0], "m": ERR_SCHOOL_ID_ERR[1], "d": []}
    # 小学年制
    if primary_years:
        primary_years = int(primary_years)
    else:
        primary_years = 0
    # 初中年制
    if junior_years:
        junior_years = int(junior_years)
    else:
        junior_years = 0
    # 高中年制
    if senior_years:
        senior_years = int(senior_years)
    else:
        senior_years = 0
    # 检查年制设置是否正确
    if primary_years not in PRIMARY_YEARS_LIST \
            or junior_years not in JUNIOR_YEARS_LIST \
            or senior_years not in SENIOR_YEARS_LIST \
            or (primary_years+junior_years) > 9 \
            or (primary_years+junior_years+senior_years) > 12:
        return {"c": ERR_SCHOOL_LEARNING_PERIOD_ERROR[0], "m": ERR_SCHOOL_LEARNING_PERIOD_ERROR[1], "d": []}

    have_class = Class.objects.filter(school_id=school_id, del_flag=FLAG_NO).exists()
    if have_class:
        return {"c": ERR_SCHOOL_LEARNING_PERIOD_CLASS_ERROR[0], "m": ERR_SCHOOL_LEARNING_PERIOD_CLASS_ERROR[1], "d": []}

    # 更新学校学段学制
    school_obj.primary_years = primary_years
    school_obj.junior_years = junior_years
    school_obj.senior_years = senior_years
    school_obj.academic_year = primary_years + junior_years + senior_years
    school_obj.save()

    # 创建年级信息
    __init_grade(school_obj)

    # 更新class style
    __init_school_class_style(school_obj)

    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}


# 学期学年
@transaction.atomic
def __init_management(school_id, update_month=settings.SYS_AUTOUPDATE_TIME['MONTH'], update_day=settings.SYS_AUTOUPDATE_TIME['DAY']):
    pre_test = UpdateManagement.objects.filter(school_id=school_id, del_flag=FLAG_NO)
    if pre_test.exists():
        return
    today = datetime.date.today()
    sep_date = datetime.date(year=today.year, month=update_month, day=update_day)
    if today >= sep_date:
        cur_term = today.year
    else:
        cur_term = today.year - 1
    UpdateManagement.objects.create(school_id=school_id, cur_term=cur_term, update_month=update_month, update_day=update_day)


# 判断当前时间是否可以升级和回退操作
def __is_allow_update_term(update_month=None, update_day=None):
    """
        默认时判断当前时间是否可以升级和回退操作:
        当前配置时间：起始时间 6月1号
                   截止时间 9月30号
        当配置month和day时，判断传入时间是否在本区间内
    """
    today = datetime.date.today()
    if not update_month or not update_day:
        date_time = datetime.date.today()
    else:
        date_time = datetime.date(today.year, update_month, update_day)
    start_time = datetime.date(year=today.year, month=settings.TIME_RANGE_DICT["START_TIME"][0], day=settings.TIME_RANGE_DICT["START_TIME"][1])
    end_time = datetime.date(year=today.year, month=settings.TIME_RANGE_DICT["DEADLINE"][0], day=settings.TIME_RANGE_DICT["DEADLINE"][1])
    if date_time >= start_time and date_time <= end_time:
        return True
    else:
        return False


# 查询当前学年
def display_current_term(user):
    school_id = user.school_id
    manage = UpdateManagement.objects.filter(school_id=school_id, del_flag=FLAG_NO)
    if not manage:
        return {"c": ERR_SCHOOL_NOT_INIT_ERROR[0], "m": ERR_SCHOOL_NOT_INIT_ERROR[1], "d": []}

    manage_data = UpdateManagement.objects.filter(school_id=school_id, del_flag=FLAG_NO).values_list('cur_term', flat=True)
    term_data = list(manage_data)[0]
    term_string = str(term_data)+'~'+str(term_data+1)
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": term_string}


def degrade_school_term(school_id):
    return __update_school_term(school_id, is_upgrade=False)


def upgrade_school_term(school_id):
    return __update_school_term(school_id, is_upgrade=True)


def auto_upgrade_school_term(school_id):
    term_data = UpdateManagement.objects.filter(school_id=school_id, del_flag=FLAG_NO).first()
    today = datetime.date.today()
    start_time = datetime.date(year=today.year, month=term_data.update_month, day=term_data.update_day)
    if today > start_time:
        upgrade_school_term(school_id)
    else:
        return


@transaction.atomic
def __update_school_term(school_id, is_upgrade=True):
    # 只能在规定时间段内修改学年
    if not __is_allow_update_term():
        err_msg = u"请在指定时间区段[%d/%d-%d/%d]内修改学年数据" %\
                  (settings.TIME_RANGE_DICT["START_TIME"][0], settings.TIME_RANGE_DICT["START_TIME"][1],
                   settings.TIME_RANGE_DICT["DEADLINE"][0], settings.TIME_RANGE_DICT["DEADLINE"][1])
        return {"c": ERR_CANNOT_OP_TERM_ERROR[0], "m": err_msg, "d": []}
    # 获取该学校的学年配置数据
    term_data = UpdateManagement.objects.filter(school_id=school_id, del_flag=FLAG_NO).first()

    # 检查是否已经升级过学年，当前年份等于当前学年，即为升级过年级
    today = datetime.date.today()
    cur_year = today.year
    if is_upgrade and term_data.cur_term != cur_year-1:
        return {"c": ERR_HAVE_UPGRADE_TERM_ERROR[0], "m": ERR_HAVE_UPGRADE_TERM_ERROR, "d": []}
    elif not is_upgrade and term_data.cur_term != cur_year:
        return {"c": ERR_CANNOT_DEGRADE_TERM_ERROR[0], "m": ERR_CANNOT_DEGRADE_TERM_ERROR, "d": []}
    # 检查是否有一年级班级，如果有不能回退
    if not is_upgrade and Class.objects.filter(school=school_id, graduate_status=FLAG_NO, period_grade_num=1, del_flag=FLAG_NO).exists():
        return {"c": ERR_HAVE_FIRST_GRADE_CLASS_TERM_ERROR[0], "m": ERR_HAVE_FIRST_GRADE_CLASS_TERM_ERROR, "d": []}

    # 更新学期数据
    delta = 1
    if not is_upgrade:
        delta = -1
    term_data.cur_term += delta
    term_data.save()

    # 修改所有班级的年级信息 （grade_num， period_grade_num，class_name， grade_name）
    # 修改班级的毕业相关信息（graduate_year， graduate_status）
    # 只更新未毕业班级
    grade_obj_list = Grade.objects.filter(school_id=school_id, del_flag=FLAG_NO)
    grade_obj_dict = {}
    for grade_obj in grade_obj_list:
        grade_obj_dict[grade_obj.grade_num] = grade_obj

    class_list = Class.objects.filter(school=school_id, graduate_status=FLAG_NO, del_flag=FLAG_NO)
    for cls_obj in class_list:
        if is_upgrade:
            if cls_obj.period_grade_num == cls_obj.school_years:  # 将毕业的班级
                graduate_class(cls_obj, cur_year)
            elif cls_obj.period_grade_num < cls_obj.school_years:  # 非将毕业的班级
                grade_obj = grade_obj_dict[cls_obj.grade_num + delta]
                update_class_grade(school_id, cls_obj, grade_obj)
            else:
                raise Exception(ERR_CLASS_GRADE_NUM_TOO_LARGE_ERROR[1])
        else:
            grade_obj = grade_obj_dict[cls_obj.grade_num + delta]
            update_class_grade(school_id, cls_obj, grade_obj)
    # 年级回退后应该将刚毕业的班级恢复为在读
    if not is_upgrade:
        class_list = Class.objects.filter(school=school_id, graduate_year=cur_year, graduate_status=FLAG_YES, del_flag=FLAG_NO)
        for cls_obj in class_list:
            grade_obj = grade_obj_dict[cls_obj.grade_num]
            undo_graduate_class(cls_obj)
            update_class_grade(school_id, cls_obj, grade_obj)
    # 更新年级中的班级数量
    refresh_class_amount(school_id)
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}


@transaction.atomic
def display_update_time(user):
    school_id = user.school_id
    manages = UpdateManagement.objects.filter(school_id=school_id, del_flag=FLAG_NO)
    if not manages:
        return dict(c=ERR_SCHOOL_NOT_INIT_ERROR[0], m=ERR_SCHOOL_NOT_INIT_ERROR[1], d=[])
    else:
        manage = manages.first()
        manage_id = manage.id
        update_month = manage.update_month
        update_day = manage.update_day
        manage.save()
        UpdateManagement.objects.filter(school_id=school_id, del_flag=FLAG_NO).exclude(id=manage_id).\
            update(del_flag=FLAG_YES, update_time=datetime.datetime.now())
        date = dict(month=update_month, day=update_day)
        return dict(c=ERR_SUCCESS[0], m=ERR_SUCCESS[1], d=date)


# 配置升学年时间
@transaction.atomic
def config_update_time(user, month, day):
    school_id = user.school_id
    if not month or not day :
        return dict(c=ERR_REQUEST_PARAMETER_ERROR[0], m=ERR_REQUEST_PARAMETER_ERROR[1], d=[])
    month = int(month)
    day = int(day)
    if not __is_allow_update_term(month, day):
        msg = u"升学年的时间区段必须在[%d/%d-%d/%d]内" % \
              (settings.TIME_RANGE_DICT["START_TIME"][0], settings.TIME_RANGE_DICT["START_TIME"][1],
               settings.TIME_RANGE_DICT["DEADLINE"][0], settings.TIME_RANGE_DICT["DEADLINE"][1])
        return dict(c=ERR_TIME_CONF[0], m=ERR_TIME_CONF[1]+msg, d=[])
    item_data = UpdateManagement.objects.filter(school_id=school_id, del_flag=FLAG_NO).first()
    if item_data:
        item_data.update_month = month
        item_data.update_day = day
        item_data.save()
    return dict(c=ERR_SUCCESS[0], m=ERR_SUCCESS[1], d=[])


# 创建学校时初始化该学校相关数据
@transaction.atomic
def init_school(school_obj):
    try:
        # 初始化学段项目
        __init_learning_period(school_obj)
        # 初始化学校学期相关数据
        __init_management(school_obj.id)
        # 初始化年级信息
        if not Grade.objects.filter(school_id=school_obj.id, del_flag=FLAG_NO).exists():
            __init_grade(school_obj)
        # 初始化学校的班级样式数据库
        __init_school_class_style(school_obj, False)
    except Exception as ex:
        logger.error(u"初始化学校相关数据失败")
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)


# 初始化数据库，数据库为空时执行一次
def init_school_db():
    # 检查数据是否已经初始化
    try:
        if ClassStyle.objects.filter(del_flag=NO).exists():
            return
    except ProgrammingError:  # syncdb时会抛出该异常
        return
    file_name = os.path.join(settings.BASE_DIR, "user_center", "settings", "school.json")
    try:
        f = file(file_name)
        service_info = json.load(f)

        # 初始化服务
        class_style_list = service_info["class_style"]
        for class_style in class_style_list:
            ClassStyle.objects.create(style_example=class_style["style_example"], pattern=class_style["pattern"],
                                      args=class_style["args"], school_period=class_style["school_period"])
    except Exception as ex:
        logger.error(u"初始化学校模块相关数据库出错")
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)


def __init_learning_period(school_obj):
    # 数据迁移时使用
    # if school_obj.academic_year == 6:
    #     school_obj.primary_years = 6
    #     school_obj.save()
    if school_obj.primary_years + school_obj.junior_years + school_obj.senior_years != school_obj.academic_year:
        raise Exception(u"请手动初始化学段项目")


def __init_grade(school_obj):
    Grade.objects.filter(school_id=school_obj.id).update(del_flag=FLAG_YES, update_time=datetime.datetime.now())
    # 小学
    grade_num = 1
    period_grade_num = 1
    while period_grade_num <= school_obj.primary_years:
        Grade.objects.create(school_id=school_obj.id, grade_num=grade_num, grade_name=GRADE_NUM_CHOICE[grade_num][1],
                             period_grade_num=period_grade_num, school_period=SCHOOL_PERIOD_PRIMARY[0],
                             school_years=school_obj.primary_years)
        period_grade_num += 1
        grade_num += 1

    # 初中
    grade_num = 7
    if school_obj.junior_years == 4:
        grade_num = 6
    period_grade_num = 1
    while period_grade_num <= school_obj.junior_years:
        Grade.objects.create(school_id=school_obj.id, grade_num=grade_num, grade_name=GRADE_NUM_CHOICE[grade_num][1],
                             period_grade_num=period_grade_num, school_period=SCHOOL_PERIOD_JUNIOR[0],
                             school_years=school_obj.junior_years)
        period_grade_num += 1
        grade_num += 1

    # 高中
    grade_num = 10
    period_grade_num = 1
    while period_grade_num <= school_obj.senior_years:
        Grade.objects.create(school_id=school_obj.id, grade_num=grade_num, grade_name=GRADE_NUM_CHOICE[grade_num][1],
                             period_grade_num=period_grade_num, school_period=SCHOOL_PERIOD_SENIOR[0],
                             school_years=school_obj.senior_years)
        period_grade_num += 1
        grade_num += 1

@transaction.atomic
def __init_school_class_style(school_obj, is_update_class_name=True):
    primary_class_style = junior_class_style = senior_class_style = None
    if school_obj.primary_years > 0:
        primary_class_style = ClassStyle.objects.filter(school_period=SCHOOL_PERIOD_PRIMARY[0], del_flag=FLAG_NO).first()
    if school_obj.junior_years > 0:
        junior_class_style = ClassStyle.objects.filter(school_period=SCHOOL_PERIOD_JUNIOR[0], del_flag=FLAG_NO).first()
    if school_obj.senior_years > 0:
        senior_class_style = ClassStyle.objects.filter(school_period=SCHOOL_PERIOD_SENIOR[0], del_flag=FLAG_NO).first()
    school_class_style, created = SchoolClassStyle.objects.update_or_create(school_id=school_obj.id)
    school_class_style.primary_class_style=primary_class_style
    school_class_style.junior_class_style=junior_class_style
    school_class_style.senior_class_style=senior_class_style
    school_class_style.save()

    if not is_update_class_name:
        return
    # 更新所有班级样式
    primary_class_style_id = junior_class_style_id = senior_class_style_id = ""
    if primary_class_style:
        primary_class_style_id = primary_class_style.id
    if junior_class_style:
        junior_class_style_id = junior_class_style.id
    if senior_class_style:
        senior_class_style_id = senior_class_style.id
    update_class_style(school_obj.id, primary_class_style_id, junior_class_style_id, senior_class_style_id)