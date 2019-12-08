#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from err_code import *
from constant import *
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django_cas_ng import views as cas_views

from user_center.apps.weixinmp.models import WeixinAccount

logger = logging.getLogger(__name__)

# 是否检查登录
IS_CHECK_LOGIN = True

#
# def auth_check(request, method="POST", role=None, check_login=True):
#     dict_resp = {}
#
#     log_request(request)
#     if not IS_CHECK_LOGIN:
#         return dict_resp
#
#     if check_login:
#         if not request.user.is_authenticated():
#             dict_resp = {'c': ERR_USER_NOTLOGGED[0], 'm': ERR_USER_NOTLOGGED[1]}
#             return dict_resp
#
#         if role:
#             if role not in get_user_role(request.user):
#                 dict_resp = {'c': ERR_USER_AUTH[0], 'm': ERR_USER_AUTH[1]}
#                 return dict_resp
#
#     if request.method != method.upper():
#         dict_resp = {'c': ERR_REQUESTWAY[0], 'm': ERR_REQUESTWAY[1]}
#         return dict_resp
#
#     return dict_resp
#
#
# def log_request(request):
#     # self.start_time = time.time()
#     remote_addr = request.META.get('REMOTE_ADDR')
#     if remote_addr in getattr(settings, 'INTERNAL_IPS', []):
#         remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or remote_addr
#     if hasattr(request, 'user'):
#         user_account = getattr(request.user, 'username', '-')
#     else:
#         user_account = 'nobody-user'
#
#     user_agent = "pc"
#     if check_weixin_agent(request):
#         user_agent = "wx"
#     if 'POST' == str(request.method):
#         logger.info('[POST] %s %s %s %s :' % (remote_addr, user_account, request.get_full_path(), user_agent))
#         logger.info(request.POST)
#     if 'GET' == str(request.method):
#         logger.info('[GET] %s %s %s %s :' % (remote_addr, user_account, request.get_full_path(), user_agent))
#         logger.info(request.GET)

#
# def get_user_role(user):
#     user_role_list = []
#     return user_role_list

import functools
from django import http
import traceback
import datetime
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from public_fun import convert_from_url_path
from django.shortcuts import render_to_response
# from ..apps.account.models import LoginCode
from django.contrib import auth


def check_weixin_agent(request):
    agent = request.META.get('HTTP_USER_AGENT', "")
    if "MicroMessenger" in agent:
        return True
    else:
        return False


def page_login_require(view_func):
    """
    A view decorator which returns the provided view function,
    modified to return a 403 when the remote address is not in
    the list of internal IPs defined in settings.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            if isinstance(request.user, AnonymousUser):
                ticket = request.GET.get("ticket", "")
                if ticket:
                    logger.info('caslogin--ticket=%s', ticket)
                    return cas_views.login(request, next_page=request.get_full_path())

                if check_weixin_agent(request):

                    school_id = request.GET.get("sid", "")
                    state = convert_from_url_path('http://' + request.META.get('HTTP_HOST', "") + request.get_full_path())
                    # print state
                    if not state:
                        return HttpResponseForbidden()
                    else:
                        return HttpResponseRedirect("/wx/authorize?state=" + state + "&sid=" + school_id)
                else:

                    token = request.GET.get("t", "")
                    now = datetime.datetime.now()
                    due_date = now + datetime.timedelta(hours=1)
                    # login_code = LoginCode.objects.filter(value=token, create_time__lt=due_date, del_flag=FLAG_NO).first()
                    login_code = None  # 暂时不允许直接通过token登陆。后面有需要再改，可能会通过openid登陆。
                    if not login_code:
                        return HttpResponseForbidden('<h1>Forbidden<br/> 请从手机微信公众号上登陆使用本系统</h1>')
                    else:
                        login_code.del_flag = FLAG_YES
                        auth.login(request, login_code.account)
                        login_code.save()
                        return view_func(request, *args, **kwargs)
            else:
                return view_func(request, *args, **kwargs)
        except Exception as ex:
            sErrInfo = traceback.format_exc()
            logger.error(sErrInfo)
            return HttpResponseForbidden('<h1>Forbidden</h1>')
    return wrapper


def get_fh_openid(view_func):
    # 获取烽火openid，必须放在page_login_require下面,或者已经登陆的页面下面才能获取到烽火的openid
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            if isinstance(request.user, AnonymousUser):
                # 未登陆用户不作处理，因为拿到openid也不知道绑到哪个用户上，
                # 且按道理这个装饰器需要放在page_login_require下面，所以只有登陆用户会走到这个流程里面来
                return view_func(request, *args, **kwargs)

            else:
                if check_weixin_agent(request):
                    # 查询用户是否已经记录了烽火openid，如果已经登记，没必要每个页面都访问这个复杂流程获取openid。
                    weixin_account = WeixinAccount.objects.filter(account=request.user, del_flag=FLAG_NO)
                    if weixin_account and weixin_account.first().openid_fh:
                        return view_func(request, *args, **kwargs)

                    state = convert_from_url_path('http://' + request.META.get('HTTP_HOST', "") + request.get_full_path())
                    # print state
                    if not state:
                        return HttpResponseForbidden()
                    else:
                        return HttpResponseRedirect("/wx/authorize_fh?state=%s" % state)
                else:
                    return HttpResponseForbidden('<h1>Forbidden<br/> 请从手机微信公众号上登陆使用本系统</h1>')
        except Exception as ex:
            sErrInfo = traceback.format_exc()
            logger.error(sErrInfo)
            return HttpResponseForbidden('<h1>Forbidden</h1>')
    return wrapper


def fh_page_login(view_func):
    # 获取烽火openid，获取对应的用户进行cas登陆。
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            if isinstance(request.user, AnonymousUser):
                ticket = request.GET.get("ticket", "")
                if ticket:
                    logger.info('caslogin--ticket=%s', ticket)
                    return cas_views.login(request, next_page=request.get_full_path())

                # 未登陆用户，先获取用户的code，为获取openid做准备
                if check_weixin_agent(request):
                    state = convert_from_url_path('http://' + request.META.get('HTTP_HOST', "") + request.get_full_path())

                    if not state:
                        return HttpResponseForbidden()
                    else:
                        return HttpResponseRedirect("/wx/authorize_fhlogin?state=%s" % state)
                else:
                    return HttpResponseForbidden('<h1>Forbidden<br/> 请从微信上登陆使用本系统</h1>')

            else:
                # 已登陆用户，获取用户当前所在学校，然后跳转到该学校的首页
                if check_weixin_agent(request):
                    return HttpResponseRedirect("/m?sid=%s" % request.user.school.id)
                else:
                    return HttpResponseForbidden('<h1>Forbidden<br/> 请从微信登陆使用本系统</h1>')

        except Exception as ex:
            sErrInfo = traceback.format_exc()
            logger.error(sErrInfo)
            return HttpResponseForbidden('<h1>Forbidden</h1>')
    return wrapper
