﻿#!/usr/bin/python
# -*- coding: utf-8 -*-

# 状态标志位
FLAG_YES = 1
FLAG_NO = 0

# 中文数字转换：1—99
NUM_CHINESE_SIMPLE = [u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十']

# 班级风格显示
SEPARATE_SET = {'zero_sep':'0', 'empty_sep':'', 'right_parentheses':")", 'left_parentheses':"("}


# 删除标志
YES = 1  # 已删除
NO = 0   # 未删除


# 时间格式
DATE_FORMAT_MONTH = 2
DATE_FORMAT_DAY = 3
DATE_FORMAT_TIME = 4
SECONDS_PER_DAY = 24*60*60

# 用户类型
USER_TYPE_NOT_SET = 0
USER_TYPE_STUDENT = 1  # 学生
USER_TYPE_TEACHER = 2  # 教师
USER_TYPE_PARENT = 4   # 家长
USER_TYPE_STUDENT_PARENT = 5   # 学生及家长
USER_TYPE_TEACHER_PARENT = 6   # 老师及家长
USER_TYPE_ALL = 7   # 老师/家长/学生
USER_TYPE_MAP = {USER_TYPE_NOT_SET: u'未知', USER_TYPE_STUDENT: u'学生', USER_TYPE_TEACHER: u'老师', USER_TYPE_PARENT: u'家长'}

# 管理员类型
ADMIN_USER_TYPE_SYSTEM_ADMIN = "1"  # 系统管理员
ADMIN_USER_TYPE_STUDENT_ADMIN = "2"  # 学生信息管理员
ADMIN_USER_TYPE_TEACHER_ADMIN = "4"  # 教师信息管理员
ADMIN_USER_TYPE_CLASS_ADMIN = "8"    # 班级管理员-班主任

# 模块权限
MODULE_STUDENT = "student"
MODULE_TEACHER = "teacher"
MODULE_PARENT = "parent"
MODULE_CLASS = "class"
MODULE_SERVICE = "service"
MODULE_SYSTEM = "system"
MODULE_LIST = [MODULE_STUDENT, MODULE_TEACHER, MODULE_PARENT, MODULE_CLASS, MODULE_SERVICE, MODULE_SYSTEM]

# 服务代码
SERVICE_CODE_USER_CENTER = "user_center"

# 家长列表的显示方式
PARENT_LIST_ONE_PARENT_PER_LINE = 0
PARENT_LIST_ONE_PARENT_MULTI_LINE = 1

# 登录名类型
LOGIN_NAME_TYPE_USER_NAME = 1
LOGIN_NAME_TYPE_ID_CARD = 2
LOGIN_NAME_TYPE_CODE = 3
LOGIN_NAME_TYPE_TMP_CODE = 4
LOGIN_NAME_TYPE_MOBILE = 5
LOGIN_NAME_TYPE_EMAIL = 6

# 学生类型
STUDENT_TYPE_NORMAL = u"正常"
STUDENT_TYPE_MIGRANT = u"借读"
STUDENT_TYPE_RESERVED = u"保籍"
STUDENT_TYPE_TRANSFER = u"转校"
STUDENT_TYPE_SUSPEND = u"休学"
STUDENT_TYPE_QUIT = u"退学"
STUDENT_TYPE_GRADUATE = u"毕业"

IN_SCHOOL_STUDENT_TYPE_LIST = [STUDENT_TYPE_NORMAL, STUDENT_TYPE_MIGRANT]
OUT_SCHOOL_STUDENT_TYPE_LIST = [STUDENT_TYPE_RESERVED, STUDENT_TYPE_TRANSFER, STUDENT_TYPE_SUSPEND, STUDENT_TYPE_QUIT, STUDENT_TYPE_GRADUATE, ]

# 服务管理归类
SERVICE_CLASSIFY_CHOICE = ((1, u"基础管理"), (2, u"校务"), (3, u"教师教学"), (4, u"教师发展"), (5, u"校宣互动"), (9, u"第三方应用"))
SERVICE_CLASSIFY_DICT = {1: u"基础管理", 2: u"校务", 3: u"教师教学", 4: u"教师发展", 5: u"校宣互动",9: u"第三方应用"}

SERVICE_ACCESS_MASK_CHOICE = ((1, u"学生"), (2, u"教师"), (3, u"学生|教师"), (4, u"家长"), (5, u"学生|家长"),
                              (6, u"教师|家长"), (7, u"学生|教师|家长"), (0, u"只对管理员开放"),)
SERVICE_ACCESS_MASK_ONLY_MANAGER = 0

# 服务类型
SERVICE_TYPE_INTERNAL = 1
SERVICE_TYPE_VENDER = 2

# 中文是否和bool值对应
BOOL_CHOICE = {u"是":"1", u"否":"0"}

# 职务
INIT_TITLE_LIST = [{"name": u"教师", "comments": u"普通学校人员默认为教师"},
                   {"name": u"班主任", "comments": u"管理班级和班级学生，可在班级管理中添加"},
                   {"name": u"校长", "comments": u"查看全校师生信息，拥有学校管理权"}]
TILE_NAME_TEACHER = INIT_TITLE_LIST[0]["name"]
TILE_NAME_CLASSMASTER = INIT_TITLE_LIST[1]["name"]
TILE_NAME_SCHOOLMASTER = INIT_TITLE_LIST[2]["name"]
INIT_TITLE_NAME_LIST = [TILE_NAME_TEACHER, TILE_NAME_CLASSMASTER, TILE_NAME_SCHOOLMASTER]

# 年级序号状态
GRADE_NUM_NOT_SET = (0, u"未设置")
GRADE_NUM_FIRST = (1, u"一年级")
GRADE_NUM_SECOND = (2, u"二年级")
GRADE_NUM_THIRD = (3, u"三年级")
GRADE_NUM_FOURTH = (4, u"四年级")
GRADE_NUM_FIFTH = (5, u"五年级")
GRADE_NUM_SIXTH = (6, u"六年级")
GRADE_NUM_SEVENTH = (7, u"七年级")
GRADE_NUM_EIGHTH = (8, u"八年级")
GRADE_NUM_NINTH = (9, u"九年级")
GRADE_NUM_TENTH = (10, u"高一")
GRADE_NUM_ELEVENTH = (11, u"高二")
GRADE_NUM_TWELFTH = (12, u"高三")

GRADE_NUM_CHOICE = (GRADE_NUM_NOT_SET, GRADE_NUM_FIRST, GRADE_NUM_SECOND, GRADE_NUM_THIRD, GRADE_NUM_FOURTH,
                    GRADE_NUM_FIFTH, GRADE_NUM_SIXTH, GRADE_NUM_SEVENTH, GRADE_NUM_EIGHTH, GRADE_NUM_NINTH,
                    GRADE_NUM_TENTH, GRADE_NUM_ELEVENTH, GRADE_NUM_TWELFTH)

PRIMARY_YEARS_LIST = [0, 5, 6]
JUNIOR_YEARS_LIST = [0, 3, 4]
SENIOR_YEARS_LIST = [0, 3]
# SCHOOL_YEARS_LIST = [0, 3, 4, 5, 6]

SCHOOL_YEARS_ZERO = (0, u"未设置")
SCHOOL_YEARS_THREE = (3, u"三年制")
SCHOOL_YEARS_FOUR = (4, u"四年制")
SCHOOL_YEARS_FIVE = (5, u"五年制")
SCHOOL_YEARS_SIX = (6, u"六年制")
SCHOOL_YEARS_CHOICE = (SCHOOL_YEARS_ZERO, SCHOOL_YEARS_THREE, SCHOOL_YEARS_FOUR, SCHOOL_YEARS_FIVE, SCHOOL_YEARS_SIX)

SCHOOL_PERIOD_PRIMARY = (1, u"小学")
SCHOOL_PERIOD_JUNIOR = (2, u"初中")
SCHOOL_PERIOD_SENIOR = (4, u"高中")
SCHOOL_PERIOD_CHOICE = (SCHOOL_PERIOD_PRIMARY, SCHOOL_PERIOD_JUNIOR, SCHOOL_PERIOD_SENIOR)

# 申请状态
APPLICATION_STATUS_NOT_PROCESS = (1, u"未处理")
APPLICATION_STATUS_APPROVED = (2, u"已同意")
APPLICATION_STATUS_REFUSED = (3, u"已拒绝")
APPLICATION_STATUS_CHOICE = (APPLICATION_STATUS_NOT_PROCESS, APPLICATION_STATUS_APPROVED, APPLICATION_STATUS_REFUSED)

# 校验手机号在帐号中存在
CHECK_MOBILE_ACCOUNT_NOT = 0
CHECK_MOBILE_ACCOUNT_IS = 1
CHECK_MOBILE_ACCOUNT_IGNORE = 2

MAX_IMPORT_PRENT_NUM = 1000

