# -*- coding=utf-8 -*-

from models import *
from user_center.utils.constant import *
from user_center.utils.file_fun import *
from user_center.utils.err_code import *
from user_center.apps.student.models import Student
from user_center.apps.parent.models import Parent
from user_center.apps.teacher.models import Teacher
from django.contrib import auth
from django.db.models import Q
from django.db import transaction
from user_center.apps.account.models import Account
from user_center.settings.production import *
from user_center.utils.public_fun import *
from user_center.apps.service.models import Service
import uuid
import os
import logging
import time

logger = logging.getLogger(__name__)


def get_user_center_url():
    user_center_obj = Service.objects.get(code=settings.SERVICE_USER_CENTER, del_flag=FLAG_NO)
    internet_url = get_domain_name(user_center_obj.internet_url)
    return internet_url


def upload_image(user, file_obj):
    file_name = file_obj.name
    file_size = file_obj.size
    ext = os.path.splitext(file_name)[-1].lower()
    if ext not in SUPPORTED_IMAGE_FILE_EXTENDS:
        return {"c": ERR_FILE_FORMAT_NOT_SUPPORTED[0], "m": ERR_FILE_FORMAT_NOT_SUPPORTED[1], "d": []}

    # save data
    school_id = user.school_id
    if not school_id:
        school_id = 0
    remote_file_name = gen_s3_file_path(suffix=ext, abs=False)
    remote_file_name = str(school_id) + "/" + remote_file_name
    md5sum = get_storage_obj().upload_file_obj(file_obj, remote_file_name)
    # url = AWS_STORAGE_BUCKET_NAME + '/' + remote_file_name
    # url = 'http://10.8.0.6/' + AWS_STORAGE_BUCKET_NAME + '/' + remote_file_name
    if not md5sum:
        raise Exception(u"文件存储失败")
    image_obj = Image.objects.create(name=file_name, url=remote_file_name, size=file_size, uploader=user.id)
    abs_url = get_image_url(remote_file_name)
    dict_resp = {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": [{"id": image_obj.id, 'url': abs_url}]}
    return dict_resp


def upload_image_v2(user, file_obj):
    file_name = file_obj.name
    file_size = file_obj.size
    ext = os.path.splitext(file_name)[-1].lower()
    if ext not in SUPPORTED_IMAGE_FILE_EXTENDS:
        return {"c": ERR_FILE_FORMAT_NOT_SUPPORTED[0], "m": ERR_FILE_FORMAT_NOT_SUPPORTED[1], "d": []}

    # save data
    school_id = user.school_id
    if not school_id:
        school_id = 0
    remote_file_name = gen_s3_file_path(suffix=ext, abs=False)
    remote_file_name = str(school_id) + "/" + remote_file_name
    md5sum = get_storage_obj().upload_file_obj(file_obj, remote_file_name)
    # url = AWS_STORAGE_BUCKET_NAME + '/' + remote_file_name
    # url = 'http://10.8.0.6/' + AWS_STORAGE_BUCKET_NAME + '/' + remote_file_name
    if not md5sum:
        raise Exception(u"文件存储失败")
    image_obj = Image.objects.create(name=file_name, url=remote_file_name, size=file_size, uploader=user.id)
    abs_url = get_image_url(remote_file_name)
    d = {
        'image_id': str(image_obj.id),
        'image_name': file_obj.name,
        'original_size': str(file_obj.size),
        'original_image_url': abs_url,
        'image_url': abs_url,
        'image_crop_url': abs_url,
        'original_width': '0',
        'original_height': '0',
    }
    dict_resp = {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": d}
    return dict_resp


def clean_overdue_images():
    now = datetime.datetime.now()
    due_date = now - datetime.timedelta(hours=settings.DATA_STORAGE_TMP_FILE_EXPIRED_HOURS)
    image_id_list = list(Image.objects.filter(update_time__lte=due_date, del_flag=NO).values_list("id", flat=True))
    student_image_id_list = list(Student.objects.all().values_list("image_id", flat=True))
    parent_image_id_list = list(Parent.objects.all().values_list("image_id", flat=True))
    teacher_image_id_list = list(Teacher.objects.all().values_list("image_id", flat=True))
    should_delete_image_id_list = set(image_id_list) - set(student_image_id_list) - set(parent_image_id_list) - set(teacher_image_id_list)
    should_delete_image_obj_list = Image.objects.filter(id__in=should_delete_image_id_list)

    for image_obj in should_delete_image_obj_list:
        obj_path = image_obj.url
        if get_storage_obj().exists(obj_path) is not None:
            if get_storage_obj().delete(obj_path):
                image_obj.del_flag = YES
                image_obj.save()
                logger.info("clean overdue image: %s" % obj_path)


import random
from PIL import Image as PILImg
from PIL import ImageDraw, ImageFont, ImageFilter
from user_center.settings.production import STATICFILES_DIRS

import urllib, urllib2, json, httplib
import string, hashlib

_letter_cases = "abcdefghjkmnpqrstuvwxy" # 小写字母，去除可能干扰的i，l，o，z
_upper_cases = _letter_cases.upper() # 大写字母
_numbers = ''.join(map(str, range(3, 10))) # 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))


def create_validate_code(size=(120, 30),
                         chars=init_chars,
                         img_type="GIF",
                         mode="RGB",
                         bg_color=(255, 255, 255),
                         fg_color=(0, 0, 255),
                         font_size=20,
                         font_type="Monaco.ttf",
                         length=4,
                         draw_lines=True,
                         n_line=(1, 2),
                         draw_points=True,
                         point_chance = 2):
    '''
    @todo: 生成验证码图片
    @param size: 图片的大小，格式（宽，高），默认为(120, 30)
    @param chars: 允许的字符集合，格式字符串
    @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
    @param mode: 图片模式，默认为RGB
    @param bg_color: 背景颜色，默认为白色
    @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
    @param font_size: 验证码字体大小
    @param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
    @param length: 验证码字符个数
    @param draw_lines: 是否划干扰线
    @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
    @param draw_points: 是否画干扰点
    @param point_chance: 干扰点出现的概率，大小范围[0, 100]
    @return: [0]: PIL Image实例
    @return: [1]: 验证码图片中的字符串
    '''

    width, height = size # 宽， 高
    img = PILImg.new(mode, size, bg_color) # 创建图形
    draw = ImageDraw.Draw(img) # 创建画笔

    def get_chars():
        '''生成给定长度的字符串，返回列表格式'''
        return random.sample(chars, length)

    def create_lines():
        '''绘制干扰线'''
        line_num = random.randint(*n_line) # 干扰线条数

        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            #结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        '''绘制干扰点'''
        chance = min(100, max(0, int(point_chance))) # 大小限制在[0, 100]

        for w in xrange(width):
            for h in xrange(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        '''绘制验证码字符'''
        c_chars = get_chars()
        strs = ' %s ' % ' '.join(c_chars) # 每个字符前后以空格隔开


        # font = ImageFont.load_default().font
        font = ImageFont.truetype(os.path.join(STATICFILES_DIRS[0], 'fonts', font_type), font_size)
        # font = ImageFont.truetype(('F:\Users\Administrator\PycharmProjects\huiyu\server\vschool\static\portal\fonts\Monaco.ttf'), font_size)
        # F:\Users\Administrator\PycharmProjects\huiyu\server\vschool\static\portal\fonts\Monaco.ttf
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width)/10, (height - font_height)/3),
                    strs, font=font, fill=fg_color)

        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strs()

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, PILImg.PERSPECTIVE, params) # 创建扭曲
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强（阈值更大）

    return img, strs

def check_validate(request, code, length=4, expire_time=None):
        if not isinstance(code, (str,unicode)):
            return False, u"验证码错误"
        elif len(code) != length:
            return False, u"验证码错误"
        else:
            if expire_time:
                create_timestamp = int(request.session['create_time'])
                curtime = time.time()
                timestamp = int(curtime)
                if create_timestamp + expire_time < timestamp:
                    return False, u'验证码超时'
            if code.lower() == request.session.get("code").lower():
                return True, u"验证成功"
            else:
                return False, u"验证码错误"


def check_imagecode(request, code):
    result = check_validate(request, code)
    if not result[0]:
        return dict(c=-1, m=result[1], d=[])
    else:
        return dict(c=ERR_SUCCESS[0], m=ERR_SUCCESS[1], d=[])


def verify_imagecode(request, mobile, code, check_mobile_account=CHECK_MOBILE_ACCOUNT_IS):
    if not mobile or not code:
        return dict(c=ERR_VERIFY_CODE_NOT_NULL[0], m=ERR_VERIFY_CODE_NOT_NULL[1], d=[])
    check_mobile_account = int(check_mobile_account)
    if check_mobile_account == CHECK_MOBILE_ACCOUNT_IS and not Account.objects.filter(mobile=mobile, del_flag=FLAG_NO).exists():
        return dict(c=ERR_VERIFY_CODE_USER_NOT_EXIST[0], m=ERR_VERIFY_CODE_USER_NOT_EXIST[1], d=[])
    if check_mobile_account == CHECK_MOBILE_ACCOUNT_NOT and Account.objects.filter(mobile=mobile, del_flag=FLAG_NO).exists():
        return dict(c=ERR_VERIFY_CODE_USER_EXIST[0], m=ERR_VERIFY_CODE_USER_EXIST[1], d=[])
    if len(mobile) != 11 or not mobile.isdigit():
        return dict(c=ERR_USER_MOBILE_ERROR[0], m=ERR_USER_MOBILE_ERROR[1], d=[])

    result = check_validate(request, code)
    if not result[0]:
        return dict(c=-1, m=result[1], d=[])
    else:
        raw_query = VerifyCode.objects.filter(mobile=mobile)
        if not raw_query:
            VerifyCode.objects.create(mobile=mobile, IMCode_status=FLAG_YES)
        else:
            if len(raw_query) == 1:
                raw_query.update(IMCode_status=FLAG_YES, del_flag=FLAG_NO, code='', timestamp="", code_status=FLAG_NO, update_time=datetime.datetime.now())
            else:
                ids = raw_query.values_list('id', flat=True)
                ids = list(ids)
                first = ids[0]
                others = id[1:]
                VerifyCode.objects.filter(id=first).update(IMCode_status=FLAG_YES, del_flag=FLAG_NO, code='', timestamp="", code_status=FLAG_NO, update_time=datetime.datetime.now())
                VerifyCode.objects.filter(id__in=others).delete()

        return dict(c=ERR_SUCCESS[0], m=ERR_SUCCESS[1], d=[])


def send_message(mobile):
    def get_nonce(length):
        """
             get不可重复字符串
        """
        # 不可重复字符串
        random_str = ''.join(random.sample(string.ascii_letters, length))
        return  random_str

    # get the current time str use timestamp
    def get_curtime_str():
        now = time.time()
        curtime = int(now)
        return str(curtime)

    # get the sha1 hexcode string : AppSecret + Nounce + Curtime
    def get_sha1_code(AppSecret, Nonce, Curtime):
        sha1obj = hashlib.sha1()
        sha1obj.update(AppSecret + Nonce + Curtime)
        sha1code = sha1obj.hexdigest()
        return sha1code

    if not mobile:
        raise Exception(u"电话号码不能为空")
    raw_query = VerifyCode.objects.filter(mobile=mobile, del_flag=FLAG_NO, IMCode_status=FLAG_YES)
    if not raw_query:
        raise Exception(u"错误请求")
    else:
        AppKey = APPKEY_EASY
        AppSecret = APPSECRET_EASY
        templateid = TEMPLATEID_EASY

        Nonce_16 = get_nonce(16)
        Curtime = get_curtime_str()
        CheckSum = get_sha1_code(AppSecret, Nonce_16, Curtime)

        data = {"mobile":mobile,
                "templateid":templateid,
                }

        data = urllib.urlencode(data)

        headers = {"AppKey":AppKey,
                   "Content-Type":'application/x-www-form-urlencoded',
                   "CurTime":Curtime,
                   "CheckSum":CheckSum,
                   "Nonce":Nonce_16,
                   }

        # get the verify code from remote
        conn = httplib.HTTPSConnection("api.netease.im")

        conn.request('POST', '/sms/sendcode.action', data, headers)
        r1 = conn.getresponse()
        data1 = r1.read()
        conn.close()
        data1 = json.loads(data1, 'utf-8')
        code = ''
        if data1['code']== 200:
            code = data1['obj']
            msg = data1['msg']

        raw_query.update(code=str(code), timestamp=Curtime, update_time=datetime.datetime.now())
        return dict(c=ERR_SUCCESS[0], m=ERR_SUCCESS[1], d=[])


def verify_messagecode(mobile, code, expire_time=None):
    if not mobile or not code:
        raise Exception(u"手机号/验证码不为空")
    raw_query = VerifyCode.objects.filter(mobile=mobile, del_flag=FLAG_NO, IMCode_status=FLAG_YES).values_list("code", "timestamp")
    if not raw_query:
        raise Exception(u"请求错误")
    else:
        codedata = list(raw_query)[0]
        if expire_time:
            create_timestamp = int(codedata[1])
            curtime = time.time()
            timestamp = int(curtime)
            if create_timestamp + expire_time < timestamp:
                raise Exception(u'验证码超时')
        if codedata[0] == code:
            VerifyCode.objects.filter(mobile=mobile, del_flag=FLAG_NO, IMCode_status=FLAG_YES).update(code_status=FLAG_YES, update_time=datetime.datetime.now())
            return dict(c=ERR_SUCCESS[0], m=ERR_SUCCESS[1], d=[])
        else:
            raise Exception(u"验证码错误")


def unset_password(mobile, newpassword, newcopy=None):
    if not mobile:
        raise Exception(u"手机号不能为空")
    if newcopy:
        if newpassword != newcopy:
            raise Exception(u"密码输入不相同")
    raw_query = VerifyCode.objects.filter(mobile=mobile, del_flag=FLAG_NO, IMCode_status=FLAG_YES, code_status=FLAG_YES)
    if not newpassword:
        raw_query.update(del_flag=FLAG_YES, update_time=datetime.datetime.now())
        return dict(c=ERR_SUCCESS[0], m=ERR_SUCCESS[1], d=[])
    if not raw_query:
        raise Exception(u"请求错误")
    else:
        account = Account.objects.filter(mobile=mobile, del_flag=FLAG_NO).first()
        account.set_password(newpassword)
        account.encoded_pwd = xor_crypt_string(data=newpassword, encode=True)
        account.save()
        raw_query.update(del_flag=FLAG_YES, update_time=datetime.datetime.now())
        return dict(c=ERR_SUCCESS[0], m=ERR_SUCCESS[1], d=[])


VERIFY_CODE_TIMEOUT_MINUTES = 10


def check_verify_code(mobile, messagecode):
    verify_code_list = VerifyCode.objects.filter(mobile=mobile, code=messagecode, del_flag=FLAG_NO, IMCode_status=FLAG_YES, code_status=FLAG_YES)
    now = datetime.datetime.now()
    due_time = now + datetime.timedelta(minutes=VERIFY_CODE_TIMEOUT_MINUTES)
    for verify_code in verify_code_list:
        if verify_code.update_time > due_time:
            continue
        else:
            return True
    return False


