#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from wsgiref.util import FileWrapper
from django.http import HttpResponse
import os

from user_center.utils.err_code import ERR_SUCCESS


def gen_file_response(file_path):
    wrapper = FileWrapper(open(file_path, 'rb'))
    response = HttpResponse(wrapper, content_type='application/vnd.ms-excel')
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Encoding'] = 'utf-8'
    response['Content-Disposition'] = 'attachment;filename=%s' % os.path.basename(file_path)
    return response


def response(result):
    """
    功能说明：   返回json
    """
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")


def response200(result):
    """
        OK
    """
    return HttpResponse(json.dumps({'c': ERR_SUCCESS[0], 'm': ERR_SUCCESS[1], 'd': result}, ensure_ascii=False), content_type='application/json')


def get_cur_domain(request):
    """
    获取当前请求的域名
    :param request: view的request
    :return:
    """
    return request.META.get('HTTP_HOST', "")
