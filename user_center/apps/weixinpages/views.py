#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.conf import settings
import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from user_center.apps.page.views import page_logout
from user_center.apps.weixinmp.models import WeixinAccount
from user_center.utils.constant import FLAG_NO

if hasattr(settings, "WEB_DEV"):
    import functools

    def page_login_require(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return wrapper

    def get_fh_openid(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return wrapper

    def fh_page_login(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return wrapper
else:
    from user_center.utils.weixin_auth import page_login_require
    from user_center.utils.weixin_auth import get_fh_openid
    from user_center.utils.weixin_auth import fh_page_login



logger = logging.getLogger(__name__)


@page_login_require
def test_page(request):
    weixinaccount = WeixinAccount.objects.filter(account_id=request.user.id, del_flag=FLAG_NO).first()
    if not weixinaccount:
        page_logout(request)
        raise Exception(u'没有找到微信用户！请重新刷新本页面。')
    template_param = {
        "wx_openid": weixinaccount.openid,
        "wx_nickname": weixinaccount.name,
        "wx_headimgurl": weixinaccount.image_url,
    }
    return render_to_response("page/weixin/test.html", template_param)


@page_login_require
def weixin_homepage(request):
    school_id = request.GET.get("sid", "")
    openid = request.GET.get("openid", "")
    return HttpResponseRedirect("/m?sid=%s&openid=%s" % (school_id, openid))


@fh_page_login
def weixin_scan_fhcode(request):
    school_id = request.user.school.id
    # openid = request.GET.get("openid", "")
    return HttpResponseRedirect("/m?sid=%s" % school_id)
