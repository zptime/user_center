# -*- coding=utf-8 -*-

from models import *
from user_center.utils.constant import *
from user_center.utils.err_code import *
from user_center.apps.service import agents as service_agents
from user_center.apps.teacher.models import *
from user_center.apps.open.agents import refresh_one_item_of_all_service
from user_center.apps.parent.models import *
from user_center.utils.file_fun import get_image_url
from user_center.utils.public_fun import gen_unique_name, check_idcard
from django.contrib import auth
from django.db.models import Q
from django.db import transaction
from user_center.apps.common.agents import check_verify_code

import re
import datetime
import logging


logger = logging.getLogger(__name__)


def login(request, login_name, password):
    username = get_username(login_name)
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return True
    return False


def get_username(login_name):
    username_list = Account.objects.filter(del_flag=NO).\
        filter(Q(username=login_name) | Q(code=login_name) | Q(mobile=login_name)).values_list("username", flat=True)
    if len(username_list) > 1:
        logger.warn("there are more than 1 user with the same login name [%s]" % login_name)
        return username_list[0]
    elif len(username_list) == 0:
        return ""
    else:
        return username_list[0]


def reset_password(user, account_id, new_password, old_password=""):
    school_id = user.school_id

    # admin reset password
    if account_id and new_password:
        user_role_list = []
        teacher = Teacher.objects.filter(school_id=school_id, account_id=user.id, del_flag=NO).first()
        if teacher:
            user_role_list = service_agents.get_service_user_role(service_code=SERVICE_CODE_USER_CENTER, user_id=teacher.id, school_id=school_id)
        if user_role_list:
            student_obj = Student.objects.filter(school_id=school_id, account_id=account_id, del_flag=NO)
            parent_obj = Parent.objects.filter(school_id=school_id, account_id=account_id, del_flag=NO)
            teacher_obj = Teacher.objects.filter(school_id=school_id, account_id=account_id, del_flag=NO)
            if ADMIN_USER_TYPE_SYSTEM_ADMIN in user_role_list:
                if not student_obj and not parent_obj and not teacher_obj:
                    return {"c": ERR_USER_AUTH[0], "m": ERR_USER_AUTH[1], "d": []}
            elif ADMIN_USER_TYPE_STUDENT_ADMIN in user_role_list:
                if not student_obj and not parent_obj:
                    return {"c": ERR_USER_AUTH[0], "m": ERR_USER_AUTH[1], "d": []}
            elif ADMIN_USER_TYPE_TEACHER_ADMIN in user_role_list:
                if not teacher_obj:
                    return {"c": ERR_USER_AUTH[0], "m": ERR_USER_AUTH[1], "d": []}
        else:
            teacher_obj = Teacher.objects.filter(school_id=school_id, account_id=user.id, del_flag=NO).first()
            if not teacher_obj or not teacher_obj.cls:
                return {"c": ERR_USER_AUTH[0], "m": ERR_USER_AUTH[1], "d": []}
            student = Student.objects.filter(school_id=school_id, cls=teacher_obj.cls, account_id=account_id, del_flag=NO).first()
            if not student:
                return {"c": ERR_USER_AUTH[0], "m": ERR_USER_AUTH[1], "d": []}
        user_obj = Account.objects.filter(id=account_id, del_flag=NO).first()
        if not user_obj:
            return {"c": ERR_USER_NOT_EXIST[0], "m": ERR_USER_NOT_EXIST[1], "d": []}
        user_obj.set_password(new_password)
        user_obj.encoded_pwd = xor_crypt_string(data=new_password, encode=True)
        user_obj.save()
    # reset self password
    elif old_password and new_password:
        if not user.check_password(old_password):
            return {"c": ERR_OLD_PASSWORD_ERROR[0], "m": ERR_OLD_PASSWORD_ERROR[1], "d": []}
        user.set_password(new_password)
        user.encoded_pwd = xor_crypt_string(data=new_password, encode=True)
        user.save()
    else:
        return {"c": ERR_REQUEST_PARAMETER_ERROR[0], "m": ERR_REQUEST_PARAMETER_ERROR[1], "d": []}

    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}


def batch_reset_password(user, account_id_list, new_password):
    real_num = 0
    total_num = len(account_id_list)
    for account_id in account_id_list:
        ret_dict = reset_password(user, account_id, new_password)
        if ret_dict["c"] == ERR_SUCCESS[0]:
            real_num += 1
    # return msg
    if real_num == total_num:
        return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}
    elif total_num == 1:
        return {"c": ERR_OP_ERROR[0], "m": ERR_OP_ERROR[1], "d": []}
    else:
        msg = u"%d条记录重置失败，%d条记录重置成功" % (total_num-real_num, real_num)
        return {"c": ERR_OP_PART_ERROR[0], "m": msg, "d": []}


# 检查用户名是否合法
def check_username(username):
    err_code = __check_username_valid(username)
    if err_code != ERR_SUCCESS:
        return {"c": err_code[0], "m": err_code[1], "d": []}

    if Account.objects.filter(username=username, del_flag=NO).exists():
        return {"c": ERR_USER_NAME_CONFLICT_ERROR[0], "m": ERR_USER_NAME_CONFLICT_ERROR[1], "d": []}
    else:
        return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}


def api_list_user_type(user, account_id=""):
    user_type_list = []
    # account_id = int(account_id)
    account_id = user.id
    domain = service_agents.get_user_center_intra_url()

    student_list = Student.objects.filter(account_id=account_id, del_flag=NO).\
        values("id", "full_name", "school_id", "school__name_full", "school__name_simple", "image__url")
    for student in student_list:
        school_name = student["school__name_simple"]
        if not school_name:
            school_name = student["school__name_full"]
        image_url = ""
        if student["image__url"]:
            image_url = get_image_url(student["image__url"], domain=domain)
        user_type = dict(type_id=str(USER_TYPE_STUDENT), type_name=u"学生", school_id=str(student["school_id"]),
                         school_name=school_name, full_name=student["full_name"],
                         id=str(student["id"]), account_id=str(account_id), image_url=image_url, username=user.username)
        user_type_list.append(user_type)

    parent_list_ = Parent.objects.filter(account_id=account_id, is_active=FLAG_YES, del_flag=NO).\
        values("id", "full_name", "school_id", "school__name_full", "school__name_simple", "image__url")
    for parent in parent_list_:
        school_name = parent["school__name_simple"]
        if not school_name:
            school_name = parent["school__name_full"]
        image_url = ""
        if parent["image__url"]:
            image_url = get_image_url(parent["image__url"], domain=domain)
        user_type = dict(type_id=str(USER_TYPE_PARENT), type_name=u"家长", school_id=str(parent["school_id"]),
                         school_name=school_name, full_name=parent["full_name"],
                         id=str(parent["id"]), account_id=str(account_id), image_url=image_url, username=user.username)
        user_type_list.append(user_type)

    teacher_list = Teacher.objects.filter(account_id=account_id, is_in=True, del_flag=NO).\
        values("id", "full_name", "school_id", "school__name_full", "school__name_simple", "image__url", "school_code")
    for teacher in teacher_list:
        school_name = teacher["school__name_simple"]
        if not school_name:
            school_name = teacher["school__name_full"]
        image_url = ""
        if teacher["image__url"]:
            image_url = get_image_url(teacher["image__url"], domain=domain)
        user_type = dict(type_id=str(USER_TYPE_TEACHER), type_name=u"教师", school_id=str(teacher["school_id"]),
                         school_name=school_name, full_name=teacher["full_name"], school_code=teacher['school_code'],
                         id=str(teacher["id"]), account_id=str(account_id), image_url=image_url, username=user.username)
        user_type_list.append(user_type)

    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": user_type_list}


def api_change_user_type(user, school_id, type_id):
    if not school_id or not School.objects.filter(id=int(school_id), del_flag=NO).exists():
        return {"c": ERR_SCHOOL_ID_ERR[0], "m": ERR_SCHOOL_ID_ERR[1], "d": []}
    if not type_id or int(type_id) not in [USER_TYPE_STUDENT, USER_TYPE_TEACHER, USER_TYPE_PARENT]:
        return {"c": ERR_USER_TYPE_ERR[0], "m": ERR_USER_TYPE_ERR[1], "d": []}
    type_id = int(type_id)
    school_id = int(school_id)
    if type_id == USER_TYPE_STUDENT and not Student.objects.filter(account_id=user.id, school_id=school_id, del_flag=NO):
        return {"c": ERR_USER_TYPE_NOT_EXIST_ERROR[0], "m": ERR_USER_TYPE_NOT_EXIST_ERROR[1], "d": []}
    elif type_id == USER_TYPE_TEACHER and not Teacher.objects.filter(account_id=user.id, school_id=school_id, del_flag=NO):
        return {"c": ERR_USER_TYPE_NOT_EXIST_ERROR[0], "m": ERR_USER_TYPE_NOT_EXIST_ERROR[1], "d": []}
    elif type_id == USER_TYPE_PARENT and not Parent.objects.filter(account_id=user.id, school_id=school_id, del_flag=NO):
        return {"c": ERR_USER_TYPE_NOT_EXIST_ERROR[0], "m": ERR_USER_TYPE_NOT_EXIST_ERROR[1], "d": []}

    user.school_id = int(school_id)
    user.type = int(type_id)
    user.save()
    # 更新其它服务中对应的用户类型
    item_data = {"id": user.id, "type": type_id, "school_id": school_id}
    refresh_one_item_of_all_service("Account", item_data)
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}


def api_detail_account(user, username=""):
    __check_user_type_and_school(user)
    account = user
    # account = Account.objects.filter(username=user.id, del_flag=NO).first()
    # if not account:
    #     return {"c": ERR_USER_NOT_EXIST[0], "m": ERR_USER_NOT_EXIST[1], "d": []}
    account_id = account.id
    user_type_list = api_list_user_type(user)["d"]
    current_user_type = None
    for user_type in user_type_list:
        if user_type["school_id"] == str(account.school_id) and user_type["type_id"] == str(account.type):
            current_user_type = user_type
    if not current_user_type and user_type_list:
        current_user_type = user_type_list[0]
        account.school_id = int(current_user_type["school_id"])
        account.type = int(current_user_type["type_id"])
        account.save()
    if not current_user_type:
        return {"c": ERR_USER_NOT_EXIST[0], "m": ERR_USER_NOT_EXIST[1], "d": []}
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": [current_user_type]}


def check_and_delete_account(account_id):
    if not Student.objects.filter(account_id=account_id, del_flag=NO).exists() \
            and not Parent.objects.filter(account_id=account_id, del_flag=NO).exists() \
            and not Teacher.objects.filter(account_id=account_id, del_flag=NO).exists():
        Account.objects.filter(id=account_id, del_flag=NO).\
            update(username=gen_unique_name(), del_flag=YES, update_time=datetime.datetime.now())


@transaction.atomic
def add_account(username="", password="", full_name="", id_card="", code="", tmp_code="", sex="", mobile="", email="",
                type=USER_TYPE_NOT_SET, school_id=None, address="", company="", is_mobile_login=YES, is_email_login=YES,
                image=None, is_override=YES):
    # check login name
    if not username and not id_card and not code and not tmp_code and not mobile and not email:
        logger.error("no login name found")
        return ERR_USER_INFO_INCOMPLETE

    # check login name valid
    account = None
    login_name_list = []
    if username:
        username = username.strip()
        err_code = __check_username_valid(username)
        if err_code != ERR_SUCCESS:
            return err_code
        login_name_list.append(username)
    if id_card:
        id_card = id_card.strip()
        err_code = __check_id_card_valid(id_card)
        if err_code != ERR_SUCCESS:
            return err_code
        login_name_list.append(id_card)
    if code:
        code = code.strip()
        err_code = __check_code_valid(code)
        if err_code != ERR_SUCCESS:
            return err_code
        login_name_list.append(code)
    if tmp_code:
        tmp_code = tmp_code.strip()
        err_code = __check_tmp_code_valid(tmp_code)
        if err_code != ERR_SUCCESS:
            return err_code
        login_name_list.append(tmp_code)
    if mobile:
        mobile = mobile.strip()
        err_code = __check_mobile_valid(mobile)
        if err_code != ERR_SUCCESS:
            return err_code
        login_name_list.append(mobile)
    if email:
        email = email.strip()
        err_code = __check_email_valid(email)
        if err_code != ERR_SUCCESS:
            return err_code
        login_name_list.append(email)

    # check login name conflict
    username_list = []
    for login_name in login_name_list:
        tmp_username = get_username(login_name)
        if tmp_username:
            username_list.append(tmp_username)
    if len(set(username_list)) == 1:  # 用户已经存在
        account = Account.objects.filter(username=username_list[0], del_flag=NO).first()
        if account:
            if account.type != type and (account.type == USER_TYPE_STUDENT or type == USER_TYPE_STUDENT):
                return ERR_USER_ALREADY_EXIST
            return [ERR_SUCCESS[0], account.id]
        # if not is_override:
        #     return ERR_USER_ALREADY_EXIST
    elif len(set(username_list)) > 1:  # 对应多个用户
        logger.error(u"提供登录信息对应多个用户[%d][%d]" % (username_list[0], username_list[1]))
        return ERR_USER_INFO_MULTI_LOGIN_NAME_ERROR

    # generate username and password if necessary
    if not username:
        username = gen_unique_name()
    if not password:
        if type == USER_TYPE_STUDENT and code:
            password = code[-6:]
        elif mobile:
            password = mobile[-6:]
        else:
            return ERR_USER_PASSWORD_NOT_EXIST_ERROR

    # create account if it not exist
    if not account:
        account = Account.objects.create_user(username, password)
    # update account info
    if full_name: account.full_name = full_name
    if id_card: account.id_card = id_card
    if code: account.code = code
    if tmp_code: account.tmp_code = tmp_code
    if sex: account.sex = sex
    if mobile: account.mobile = mobile; account.is_mobile_login = is_mobile_login
    if type: account.type = type; account.is_email_login = is_email_login
    if school_id: account.school_id = school_id
    if address: account.address = address
    if company: account.company = company
    if image: account.image = image
    account.save()

    return [ERR_SUCCESS[0], account.id]


def update_account(user, account, username=None, code=None, mobile=None):
    # 用户自己修改自己的用户名帐号信息（username）
    username_updated = False
    if user.id == account.id:
        if username and username != account.username:
            username = username.strip()
            if Account.objects.filter(username=username, del_flag=NO).exists():
                return ERR_USER_NAME_CONFLICT_ERROR
            err_code = __check_username_valid(username)
            if err_code != ERR_SUCCESS:
                return err_code
            account.username = username
            username_updated = True
    # 管理员采用修改修改学生的学籍帐号信息(code)
    else:
        if code and code != account.code:
            code = code.strip()
            if Account.objects.filter(code=code, del_flag=NO).exists():
                return ERR_USER_CODE_CONFLICT_ERROR
            err_code = __check_code_valid(code)
            if err_code != ERR_SUCCESS:
                return err_code
            account.code = code
        elif code == "":  # 支持设置为空
            account.code = code

    # 用户自己和管理员都能修改手机帐号信息
    if mobile and mobile != account.mobile:
        mobile = mobile.strip()
        if Account.objects.filter(mobile=mobile, del_flag=NO).exists():
            return ERR_USER_MOBILE_CONFLICT_ERROR
        err_code = __check_mobile_valid(mobile)
        if err_code != ERR_SUCCESS:
            return err_code
        account.mobile = mobile
    elif mobile == "":  # 支持设置为空
        account.mobile = mobile
    account.save()
    # 更新其它服务中对应的用户类型
    if username_updated:
        item_data = {"id": user.id, "username": username}
        refresh_one_item_of_all_service("Account", item_data)
    return ERR_SUCCESS


def __check_id_card_valid(login_name):
    if not re.match('[a-zA-Z0-9]+$', login_name):
        return ERR_USER_ID_CARD_ERROR
    if len(login_name) != 18 or not login_name[:17].isdigit():
        return ERR_USER_ID_CARD_ERROR
    else:
        return ERR_SUCCESS


CODE_PREFIX = ["G", "L", "F"]


def __check_code_valid(login_name):
    if not re.match('[a-zA-Z0-9]+$', login_name):
        return ERR_USER_STUDENT_CODE_ERROR
    login_name = login_name.upper()
    # if login_name[0] != "G" or len(login_name) < 10 or not login_name[1:-1].isdigit():
    # if len(login_name) == 11 or not login_name[1:-1].isdigit():
    if len(login_name) < 10 or len(login_name) > 20 or not login_name[0] in CODE_PREFIX:
        return ERR_USER_STUDENT_CODE_ERROR
    else:
        return ERR_SUCCESS


def __check_tmp_code_valid(login_name):
    if not re.match('[a-zA-Z0-9]+$', login_name):
        return ERR_USER_STUDENT_CODE_ERROR
    login_name = login_name.upper()
    if login_name[0] != "L" or len(login_name) < 10 or not login_name[1:-1].isdigit():
        return ERR_USER_STUDENT_CODE_ERROR
    else:
        return ERR_SUCCESS


def __check_mobile_valid(login_name):
    if len(login_name) != 11 or not login_name.isdigit():
        return ERR_USER_MOBILE_ERROR
    else:
        return ERR_SUCCESS


def __check_email_valid(login_name):
    if not re.match('[a-zA-Z0-9_.@]+$', login_name):
        return ERR_USER_EMAIL_ERROR
    if "@" not in login_name:
        return ERR_USER_EMAIL_ERROR
    else:
        return ERR_SUCCESS


def __check_id_valid(login_name):
    if not login_name.isdigit():
        return ERR_USER_ID_ERROR
    elif int(login_name) <= 0 or int(login_name) > 99999999:
        return ERR_USER_ID_ERROR
    else:
        return ERR_SUCCESS


def __check_username_valid(login_name):
    if not re.match('[a-zA-Z0-9_.@]+$', login_name):
        return ERR_USER_USERNAME_ERROR
    if len(login_name) < 6 or __check_id_valid(login_name) == ERR_SUCCESS \
                           or __check_code_valid(login_name) == ERR_SUCCESS \
                           or __check_mobile_valid(login_name) == ERR_SUCCESS:
        return ERR_USER_USERNAME_ERROR
    else:
        return ERR_SUCCESS


def reset_mobile(user, new_mobile, messagecode):
    err_code = __check_mobile_valid(new_mobile)
    if err_code != ERR_SUCCESS:
        return {"c": err_code[0], "m":err_code[1], "d": []}
    if not check_verify_code(new_mobile, messagecode):
        return {"c": ERR_VERIFY_CODE_ERROR[0], "m": ERR_VERIFY_CODE_ERROR[1], "d": []}
    user.mobile = new_mobile
    user.save()
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}


def detail_account_by_mobile(mobile):
    account_obj = Account.objects.filter(mobile=mobile, del_flag=FLAG_NO).first()
    if not account_obj:
        return {"c": ERR_USER_NOT_EXIST[0], "m": ERR_USER_NOT_EXIST[1], "d": []}
    user_obj = get_user_obj(account_obj)
    account_info = {"username": account_obj.username, "mobile": mobile, "full_name": "", "image_url": ""}
    if user_obj:
        account_info["full_name"] = user_obj.full_name
        if user_obj.image:
            image_obj = Image.objects.filter(id=user_obj.image_id).first()
            if image_obj:
                account_info["image_url"] = get_image_url(image_obj.url)
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": [account_info]}


def get_user_obj(account):
    if account.type == USER_TYPE_STUDENT:
        return Student.objects.filter(school_id=account.school_id, account_id=account.id, del_flag=FLAG_NO).first()
    elif account.type == USER_TYPE_TEACHER:
        return Teacher.objects.filter(school_id=account.school_id, account_id=account.id, del_flag=FLAG_NO).first()
    elif account.type == USER_TYPE_PARENT:
        return Parent.objects.filter(school_id=account.school_id, account_id=account.id, del_flag=FLAG_NO).first()
    else:
        return None



def get_user_info(user):
    account_id = user.id
    user_type = user.type
    school_id = user.school_id
    domain = service_agents.get_user_center_intra_url()
    user_info = {}

    if user_type == USER_TYPE_STUDENT:
        user_info = Student.objects.filter(school_id=school_id, account_id=account_id, del_flag=NO).\
            values("id", "sex", "full_name", "id_card", "image__url",
                   "school__name_full", "school__name_simple", "school__type",
                   "school__province", "school__city", "school__district",
                   "cls__grade_num", "cls__class_name", "cls__enrollment_year").first()
    elif user_type == USER_TYPE_TEACHER:
        user_info = Teacher.objects.filter(school_id=school_id, account_id=account_id, del_flag=NO).\
            values("id", "sex", "full_name", "id_card", "image__url",
                   "school__name_full", "school__name_simple", "school__type",
                   "school__province", "school__city", "school__district").first()

    ret_user_info = {"account_id": account_id,
                     "user_type": user_type,
                     "school_id": school_id,
                     "mobile": user.mobile,
                     "username": user.username,
                     "user_id": user_info.get("id", ""),
                     "full_name": user_info.get("full_name", ""),
                     "sex": user_info.get("sex", ""),
                     "id_card": user_info.get("id_card", ""),
                     "image_url": get_image_url(user_info.get("image__url", ""), domain=domain),
                     "school_name_full": user_info.get("school__name_full", ""),
                     "school_name_simple": user_info.get("school__name_simple", ""),
                     "school_type": user_info.get("school__type", ""),
                     "school_province": user_info.get("school__province", ""),
                     "school_city": user_info.get("school__city", ""),
                     "school_district": user_info.get("school__district", ""),
                     "grade_num": user_info.get("cls__grade_num", ""),
                     "class_name": user_info.get("cls__class_name", ""),
                     "enrollment_year": user_info.get("cls__enrollment_year", ""),
                     }
    return ret_user_info


def __check_user_type_and_school(user):
    if not user.type or not user.school_id:
        return
    need_reset = False
    if user.type == USER_TYPE_STUDENT:
        if not Student.objects.filter(account_id=user.id, school_id=user.school_id, del_flag=FLAG_NO).exists():
            need_reset = True
    elif user.type == USER_TYPE_TEACHER:
        if not Teacher.objects.filter(account_id=user.id, school_id=user.school_id, is_in=True, del_flag=FLAG_NO).exists():
            need_reset = True
    elif user.type == USER_TYPE_PARENT:
        parent_obj = Parent.objects.filter(account_id=user.id, school_id=user.school_id, is_active=FLAG_YES, del_flag=FLAG_NO).first()
        if not parent_obj:
            need_reset = True
        else:
            if not ParentStudent.objects.filter(parent=parent_obj, del_flag=FLAG_NO).exists():
                parent_obj.del_flag = FLAG_YES
                parent_obj.save()
                need_reset = True
    if need_reset:
        user.school_id = None
        user.type = USER_TYPE_NOT_SET
        user.save()


def check_id_code_have_occupied(id_card, account_id):
    valid, msg = check_idcard(id_card)
    if not valid:
        logger.warn("id_card: %s check error msg: %s" % (id_card, msg))
        raise Exception(u"身份证号格式不正确")
    student_list = Student.objects.filter(id_card=id_card, del_flag=FLAG_NO).values("id", "account_id", "id_card")
    for student in student_list:
        if student["account_id"] != account_id:
            logger.warn("id_card %s have used student_id=%d" % (id_card, account_id))
            return True
    teacher_list = Teacher.objects.filter(id_card=id_card, del_flag=FLAG_NO).values("id", "account_id", "id_card")
    for teacher in teacher_list:
        if teacher["account_id"] != account_id:
            logger.warn("id_card %s have used teacher_id=%d" % (id_card, account_id))
            return True
    parent_list = Parent.objects.filter(id_card=id_card, del_flag=FLAG_NO).values("id", "account_id", "id_card")
    for parent in parent_list:
        if parent["account_id"] != account_id:
            logger.warn("id_card %s have used parent_id=%d" % (id_card, account_id))
            return True
    return False
