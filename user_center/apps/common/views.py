#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from user_center.utils.request_auth import *
from user_center.utils.gen_response import *
from user_center.utils.constant import *
from user_center.utils.err_code import *
import agents
import json
import traceback
import logging
import time
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

logger = logging.getLogger(__name__)


def api_get_user_center_url(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        internet_url = agents.get_user_center_url()
        resp_data = {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": [internet_url]}
        return HttpResponse(json.dumps(resp_data), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_upload_image(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    try:
        file_obj = request.FILES['image']

        dictResp = agents.upload_image(request.user, file_obj)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_upload_image_v2(request):
    dictResp = auth_check(request, "POST")
    if dictResp != {}:
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")
    try:
        file_obj = request.FILES['image']
        dictResp = agents.upload_image_v2(request.user, file_obj)    # 为兼容移动端改造接口格式
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


# 生成图片验证码，将图片返回，code保存到session中
def api_get_imagecode(request):
    try:
        image_code = agents.create_validate_code()
        image = image_code[0]
        code = image_code[1]
        # image.save('d:/image.gif', 'GIF')
        mstream = StringIO.StringIO()
        image.save(mstream, "GIF")

        curtime = time.time()
        curtimestamp = str(int(curtime))
        request.session['code'] = code
        request.session['creat_time'] = curtimestamp
        return HttpResponse(mstream.getvalue(), "image/gif")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_verify_imagecode(request):
    try:
        mobile = request.POST.get("mobile")
        code = request.POST.get('code')
        check_mobile_account = request.POST.get('check_mobile_account', CHECK_MOBILE_ACCOUNT_IS)
        dictResp = agents.verify_imagecode(request, mobile, code, check_mobile_account)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


# 检查验码是否正确
def api_check_imagecode(request):
    try:
        code = request.POST.get('code')
        dictResp = agents.check_imagecode(request, code)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_send_messagecode(request):
    try:
        mobile = request.GET["mobile"]
        dictResp = agents.send_message(mobile)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_verify_messagecode(request):
    try:
        mobile = request.POST.get("mobile")
        code = request.POST.get("code")
        dictResp = agents.verify_messagecode(mobile, code)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")


def api_unset_password(request):
    try:
        mobile = request.POST.get("mobile")
        newpassword = request.POST.get("newpassword")
        newcopy = request.POST.get("newcopy")
        dictResp = agents.unset_password(mobile, newpassword, newcopy)
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dictResp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")




