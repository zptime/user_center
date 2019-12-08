# coding=utf-8
import hashlib
from urllib import urlencode

from django.conf import settings
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
# from django.conf import settings
from user_center.apps.parent.models import Parent
from user_center.apps.school.models import School
from user_center.apps.teacher.models import Teacher
from user_center.apps.weixinmp.agents import get_weixin_school, get_type_current_user, get_parentbyid, get_fh_weixinschool
from user_center.apps.weixinmp.models import WeixinSchool, WeixinAccount, WeixinShortUrl
from user_center.settings.production import weixin_redirect_uri, AUTHENTICATION_BACKENDS, weixin_redirect_uri_fh, weixin_redirect_uri_fhlogin
from user_center.utils.constant import FLAG_NO
from user_center.utils.err_code import ERR_WX_USE_PARENT
from user_center.utils.gen_response import response200, get_cur_domain
from user_center.utils.public_fun import send_http_request, convert_to_url_path, wxtoken_compose
from user_center.utils.request_auth import auth_check, internal_or_403
from user_center.utils.utils_except import BusinessException
from user_center.utils.utils_log import log_request, log_response
from . import agents
import logging
import json
import traceback

logger = logging.getLogger(__name__)


def response_exception(exception, msg=''):
    if isinstance(exception, BusinessException):
        final_message = exception.msg
        if msg:
            final_message = u'%s, 原因: %s' % (msg, exception.msg)
        result = {'c': exception.code, 'm': final_message}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
    else:
        final_message = u'请求失败'
        if msg:
            final_message = msg
        result = {'c': -1, 'm': final_message}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def wx_get_code(request):
    try:
        state = request.GET.get("state", "")
        school_id = request.GET.get("sid", "")
        school = get_school_byid(school_id)
        weixinschool = get_weixin_school(school_id)

        if not school_id or not school or not weixinschool:
            return HttpResponseForbidden(u'<h1>Forbidden<br/> 获取学校信息失败，请从手机微信公众号上登陆使用本系统</h1>')

        weixin_scope = 'snsapi_base' if weixinschool.only_request_openid else 'snsapi_userinfo'

        state = get_shorturl_id(state)['id']
        param_dict = {
            "appid": weixinschool.app_id,
            "redirect_uri": weixin_redirect_uri + "?sid=" + school_id,  # settings.weixin_redirect_uri
            "response_type": "code",
            "scope": weixin_scope,
            "state": state,
            "sid": school_id,
        }
        param_str = urlencode(param_dict)
        redirect_uri = "https://open.weixin.qq.com/connect/oauth2/authorize?%s#wechat_redirect" % param_str
        logger.debug(redirect_uri)

        return HttpResponseRedirect(redirect_uri)
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        logger.error(ex.message)
        return HttpResponseForbidden(ex.message)


def get_account_address(account):
    teacher = Teacher.objects.filter(account=account, del_flag=FLAG_NO).first()
    parent = Parent.objects.filter(account=account, del_flag=FLAG_NO).first()

    if teacher:
        return teacher.address
    if parent:
        return parent.address
    return ''


def wx_code_to_access_token(request):
    try:
        code = request.GET.get("code")
        state = request.GET.get("state")
        school_id = request.GET.get("sid", "")
        school = get_school_byid(school_id)
        weixinschool = get_weixin_school(school_id)
        if not school or not weixinschool:
            return HttpResponseForbidden(u'<h1>Forbidden<br/> 获取学校信息失败，请从手机微信公众号上登陆使用本系统。</h1>')

        state = get_orginurl(shorturl_id=state, del_indb=False)['origin_url']
        param_dict = {
            "appid": weixinschool.app_id,
            "secret": weixinschool.app_secret,
            "code": code,
            "grant_type": "authorization_code"
        }
        param_str = urlencode(param_dict)
        uri = "https://api.weixin.qq.com/sns/oauth2/access_token?%s" % param_str
        logger.debug(uri)
        data_str = send_http_request(url=uri, method="GET")
        logger.debug(data_str)
        data = json.loads(data_str)
        if "errcode" in data or "openid" not in data or not data["openid"]:
            logger.error(uri)
            logger.error(data_str)
            return HttpResponseForbidden(data_str)

        account = agents.get_account_byopenid(data["openid"], school_id)

        # 检查是否是学校码扫码进来的，如果是扫码且没有绑定，则获取到openid后，将openid跳转到家长绑定的页面，如果已经绑定，则跳转到学校首页
        state_url = convert_to_url_path(state)
        if 'wx/page/scan/schoolcode?sid=' in state_url:
            if not account:
                return HttpResponseRedirect("/m/register/enrollParent?sid=%s&openid=%s" % (school_id, data["openid"]))
            else:
                return HttpResponseRedirect("/m?sid=%s" % school_id)

        # 检查是否是家长邀请码扫码进来的，则获取到openid后，将openid跳转到家长绑定的页面
        if 'wx/page/scan/parentcode?sid=' in state_url:
            params_get = state_url[state_url.find('?')+1:]  # ?后面的所有参数
            return HttpResponseRedirect("/m/personal/parent/addParent?%s&openid=%s" % (params_get, data["openid"]))

        # 检查是否是个人中心添加角色跳转过来
        if 'wx/page/add/role?sid=' in state_url:
            if not account:
                return HttpResponseForbidden(u'<h1>Forbidden<br/> 请从个人中心=》添加角色页页进入。</h1>')
            else:
                account_mobile = account.mobile
                address = get_account_address(account)
                params_get = state_url[state_url.find('?')+1:]  # ?后面的所有参数
                return HttpResponseRedirect("/m/register/identify?%s&openid=%s&mobile=%s&add=%s" % (params_get, data["openid"], account_mobile, address))

        # 检查用户是否关注公众号
        weixin_global_access_token = agents.get_weixin_global_access_token(weixinschool)
        if weixinschool.force_follow:
            uri = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (weixin_global_access_token, data["openid"])
            logger.debug(uri)
            wx_userinfo_str = send_http_request(url=uri, method="GET")
            logger.debug(wx_userinfo_str)
            wx_userinfo = json.loads(wx_userinfo_str)
            if "errcode" in wx_userinfo or "subscribe" not in wx_userinfo:
                logger.error(uri)
                logger.error(wx_userinfo_str)
                return HttpResponseForbidden(wx_userinfo_str)

            if wx_userinfo["subscribe"] == 0:
                if weixinschool.mp_image_url:
                    return HttpResponseRedirect(weixinschool.mp_image_url)
                else:
                    return HttpResponseForbidden(u'<h1>Forbidden<br/> 使用系统前，请先关注%s微信公众号</h1>' % weixinschool.school.name_full)

        # 检查openid是否绑定了用户,如果没有绑定，跳转到绑定页面
        if not account:
            params = {
                "openid": data["openid"],
                "school": school,
            }
            # return render_to_response("m/register/identify?sid=" + school_id, params)
            return HttpResponseRedirect("/m/register/identify?sid=%s&openid=%s" % (school_id, data["openid"]), params)

        if not weixinschool.only_request_openid:
            # 获取并更新用户信息
            # account = wx_get_userinfo(data["access_token"], data["openid"], school_id)
            # if not account:
            #     return HttpResponseForbidden()

            # 更新用户信息
            wx_update_weixinaccount(data["access_token"], data["openid"], school_id, account.id)

        if settings.DEBUG:
            # 测试登录单系统
            account.backend = AUTHENTICATION_BACKENDS[1]
            auth.login(request, account)
            redirect_uri = convert_to_url_path(state)
        else:
            # cas登陆
            cas_wx_token = wxtoken_compose(account.id)
            redirect_uri = '%slogin?source=wx&token=%s&service=%s' % (settings.CAS_SERVER_URL, cas_wx_token, convert_to_url_path(state))

        return HttpResponseRedirect(redirect_uri)
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        logger.error(ex.message)
        return HttpResponseForbidden(ex.message)


def wx_get_code_fh(request):
    try:
        state = request.GET.get("state", "")
        fh_weixinschool = get_fh_weixinschool()
        school_id = fh_weixinschool.school_id
        school = fh_weixinschool.school

        if not school_id or not school or not fh_weixinschool:
            return HttpResponseForbidden(u'<h1>Forbidden<br/> 烽火公众号系统异常，请联系系统管理员！</h1>')

        weixin_scope = 'snsapi_base'

        state = get_shorturl_id(state)['id']
        param_dict = {
            "appid": fh_weixinschool.app_id,
            "redirect_uri": weixin_redirect_uri_fh,  # settings.weixin_redirect_uri
            "response_type": "code",
            "scope": weixin_scope,
            "state": state,
            "sid": school_id,
        }
        param_str = urlencode(param_dict)
        redirect_uri = "https://open.weixin.qq.com/connect/oauth2/authorize?%s#wechat_redirect" % param_str
        logger.debug(redirect_uri)

        return HttpResponseRedirect(redirect_uri)
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        logger.error(ex.message)
        return HttpResponseForbidden(ex.message)


def wx_code_to_access_token_fh(request):
    try:
        code = request.GET.get("code")
        state = request.GET.get("state")
        fh_weixinschool = get_fh_weixinschool()
        school_id = fh_weixinschool.school_id
        school = fh_weixinschool.school
        if not school or not fh_weixinschool:
            return HttpResponseForbidden(u'<h1>Forbidden<br/> 烽火公众号系统异常，请联系系统管理员！</h1>')

        state = get_orginurl(state)['origin_url']
        param_dict = {
            "appid": fh_weixinschool.app_id,
            "secret": fh_weixinschool.app_secret,
            "code": code,
            "grant_type": "authorization_code"
        }
        param_str = urlencode(param_dict)
        uri = "https://api.weixin.qq.com/sns/oauth2/access_token?%s" % param_str
        logger.debug(uri)
        data_str = send_http_request(url=uri, method="GET")
        logger.debug(data_str)
        data = json.loads(data_str)
        if "errcode" in data or "openid" not in data or not data["openid"]:
            logger.error(uri)
            logger.error(data_str)
            return HttpResponseForbidden(data_str)

        # 此时应该登陆过，直接记录用户openid, 不请求用户其它资料，可以对用户免打扰。
        WeixinAccount.objects.filter(account=request.user, del_flag=FLAG_NO).update(openid_fh=data["openid"])

        redirect_uri = convert_to_url_path(state)
        return HttpResponseRedirect(redirect_uri)
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        logger.error(ex.message)
        return HttpResponseForbidden(ex.message)


def wx_get_code_fhlogin(request):
    try:
        state = request.GET.get("state", "")
        fh_weixinschool = get_fh_weixinschool()
        school_id = fh_weixinschool.school_id
        school = fh_weixinschool.school

        if not school_id or not school or not fh_weixinschool:
            return HttpResponseForbidden(u'<h1>Forbidden<br/> 烽火公众号系统异常，请联系系统管理员！</h1>')

        weixin_scope = 'snsapi_base'

        state = get_shorturl_id(state)['id']
        param_dict = {
            "appid": fh_weixinschool.app_id,
            "redirect_uri": weixin_redirect_uri_fhlogin,  # settings.weixin_redirect_uri
            "response_type": "code",
            "scope": weixin_scope,
            "state": state,
            "sid": school_id,
        }
        param_str = urlencode(param_dict)
        redirect_uri = "https://open.weixin.qq.com/connect/oauth2/authorize?%s#wechat_redirect" % param_str
        logger.debug(redirect_uri)

        return HttpResponseRedirect(redirect_uri)
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        logger.error(ex.message)
        return HttpResponseForbidden(ex.message)


def wx_code_to_access_token_fhlogin(request):
    try:
        code = request.GET.get("code")
        state = request.GET.get("state")
        fh_weixinschool = get_fh_weixinschool()
        school_id = fh_weixinschool.school_id
        school = fh_weixinschool.school
        if not school or not fh_weixinschool:
            return HttpResponseForbidden(u'<h1>Forbidden<br/> 烽火公众号系统异常，请联系系统管理员！</h1>')

        state = get_orginurl(state)['origin_url']
        param_dict = {
            "appid": fh_weixinschool.app_id,
            "secret": fh_weixinschool.app_secret,
            "code": code,
            "grant_type": "authorization_code"
        }
        param_str = urlencode(param_dict)
        uri = "https://api.weixin.qq.com/sns/oauth2/access_token?%s" % param_str
        logger.debug(uri)
        data_str = send_http_request(url=uri, method="GET")
        logger.debug(data_str)
        data = json.loads(data_str)
        if "errcode" in data or "openid" not in data or not data["openid"]:
            logger.error(uri)
            logger.error(data_str)
            return HttpResponseForbidden(data_str)

        # 拿到openid后，找到对应的account，使用cas登陆
        account = agents.get_account_byfhopenid(data["openid"])
        if not account:
            return HttpResponseForbidden(u'<h1>Forbidden<br/> 请先通过学校的公众号绑定帐号！</h1>')

        if settings.DEBUG:
            # 测试登录单系统
            account.backend = AUTHENTICATION_BACKENDS[1]
            auth.login(request, account)
            redirect_uri = convert_to_url_path(state)
        else:
            # cas登陆
            cas_wx_token = wxtoken_compose(account.id)
            redirect_uri = '%slogin?source=wx&token=%s&service=%s' % (settings.CAS_SERVER_URL, cas_wx_token, convert_to_url_path(state))

        return HttpResponseRedirect(redirect_uri)
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        logger.error(ex.message)
        return HttpResponseForbidden(ex.message)


def get_school_byid(school_id):
    if not school_id:
        return None
    school = School.objects.filter(id=school_id, del_flag=FLAG_NO).first()
    if not school:
        raise Exception(u'操作失败，未获取到学校信息！')
    return school


def wx_update_weixinaccount(access_token, openid, school_id, account_id):
    try:
        param_dict = {
            "access_token": access_token,
            "openid": openid,
            "lang": "zh_CN",
        }
        param_str = urlencode(param_dict)
        uri = "https://api.weixin.qq.com/sns/userinfo?%s" % param_str
        logger.debug(uri)
        data_str = send_http_request(url=uri, method="GET")
        logger.debug(data_str)
        data = json.loads(data_str)
        if "errcode" in data or "openid" not in data or not data["openid"]:
            logger.error(uri)
            logger.error(data_str)
            return None
        # print data
        wx_openid = data["openid"]
        wx_nickname = data["nickname"]
        wx_sex = data["sex"]
        wx_province = data["province"]
        wx_city = data["city"]
        wx_country = data["country"]
        wx_headimgurl = data["headimgurl"]
        wx_unionid = data.get("unionid", "")

        weixinaccount = WeixinAccount.objects.get(school_id=school_id, openid=wx_openid, account_id=account_id, del_flag=FLAG_NO)
        if not weixinaccount:
            raise Exception(u'系统异常，获取微信用户信息失败！')

        weixinaccount.name = wx_nickname
        weixinaccount.sex = wx_sex
        weixinaccount.province = wx_province
        weixinaccount.city = wx_city
        weixinaccount.country = wx_country
        weixinaccount.image_url = wx_headimgurl
        weixinaccount.unionid = wx_unionid
        weixinaccount.save()

        return
    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)


def wx_get_verifyfile(request):
    filedata = 'jIjfmE2UW1zSOJPc'
    response = HttpResponse(filedata)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="MP_verify_jIjfmE2UW1zSOJPc.txt"'
    return response


def wx_get_hkfxverifyfile(request):
    filedata = 'PPYnxDn0rz5Y03R1'
    response = HttpResponse(filedata)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="MP_verify_PPYnxDn0rz5Y03R1.txt"'
    return response


@internal_or_403
def get_weixin_global_access_token(request):
    log_request(request)
    school_id = request.GET.get("sid", "")
    weixin_app_id = request.GET.get("appid", "")

    try:
        weixinschool = get_weixin_school(school_id, weixin_app_id)
        cur_access_token = agents.get_weixin_global_access_token(weixinschool)
    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)
    log_response(request, cur_access_token)

    return response200(cur_access_token)


@internal_or_403
def update_weixin_global_access_token(request):
    school_id = request.GET.get("sid", "")
    weixin_app_id = request.GET.get("appid", "")

    try:
        weixinschool = get_weixin_school(school_id, weixin_app_id)
        globalaccesstokeninfo = agents.update_weixin_global_access_token(weixinschool)
    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)
    log_response(request, globalaccesstokeninfo)

    return response200(globalaccesstokeninfo)


def wx_get_jsconfig(request):
    log_request(request)
    school_id = request.POST.get("sid", "")
    if not school_id:
        # 不传sid就必须登陆。
        dictResp = auth_check(request, "POST", check_login=True)
        if dictResp != {}:
            return HttpResponse(json.dumps(dictResp, ensure_ascii=False), content_type="application/json")
        school_id = request.user.school.id

    weixin_app_id = request.POST.get("appid", "")
    url = request.POST.get("url", "")

    try:
        weixinschool = get_weixin_school(school_id, weixin_app_id)
        result = agents.wx_get_jsconfig(weixinschool, url)
    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)
    log_response(request, result)

    return response200(result)


def wx_mod_debugstatus(request):
    debug_status = request.POST.get("debug_status", "")

    try:
        result = agents.wx_mod_debugstatus(debug_status)
    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)
    log_response(request, result)

    return response200(result)


def api_class_qrcode(request):
    dict_resp = auth_check(request, "GET", check_login=False)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        class_id = request.GET.get("class_id", "")
        dict_resp = agents.api_class_qrcode(class_id=class_id)
        # dictResp = paging_with_request(request, dict_resp)
        return response200(dict_resp)

    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)


def api_school_qrcode(request):
    dict_resp = auth_check(request, "GET", check_login=False)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        school_id = request.GET.get("sid", "")
        if not school_id:
            school_id = request.user.school.id
        cur_domain = get_cur_domain(request)
        dict_resp = agents.api_school_qrcode(cur_domain, school_id)
        # dictResp = paging_with_request(request, dict_resp)
        return response200(dict_resp)

    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)


def api_parent_qrcode(request):
    dict_resp = auth_check(request, "GET", check_login=True)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        cur_type_user = get_type_current_user(request.user)
        if not isinstance(cur_type_user, Parent):
            raise BusinessException(ERR_WX_USE_PARENT)

        parent_id = request.GET.get("parent_id", "")
        school_id = request.GET.get("sid", "")
        if not parent_id:
            cur_type_user = get_type_current_user(request.user)
            if not isinstance(cur_type_user, Parent):
                raise BusinessException(ERR_WX_USE_PARENT)
            parent_id = cur_type_user.id
            school_id = cur_type_user.school_id

        cur_domain = get_cur_domain(request)
        dict_resp = agents.api_parent_qrcode(cur_domain, school_id, parent_id)
        # dictResp = paging_with_request(request, dict_resp)
        return response200(dict_resp)

    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)


def api_fh_qrcode(request):
    dict_resp = auth_check(request, "GET", check_login=False)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        cur_domain = get_cur_domain(request)
        dict_resp = agents.api_fh_qrcode(cur_domain)
        # dictResp = paging_with_request(request, dict_resp)
        return response200(dict_resp)

    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)


def wx_service_list(request):
    dict_resp = auth_check(request, "GET", check_login=True)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        dict_resp = agents.get_wx_service_list(request.user)
        return response200(dict_resp)

    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)


def wx_service_domain(request):
    dict_resp = auth_check(request, "GET", check_login=True)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        app_code = request.GET.get("app_code", "")
        dict_resp = agents.get_wx_service_domain(app_code)
        return response200(dict_resp)

    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)


def api_get_accountopenid(request):
    # 避免传入数据过大，本接口使用POST方式
    dict_resp = auth_check(request, "POST", check_login=False)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        account_id_list = request.POST.get("account_id_list", "")
        school_id = request.POST.get("sid", "")
        dict_resp = agents.api_get_accountopenid(account_id_list, school_id)
        return response200(dict_resp)

    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)


def api_send_teacher_bind_messagecode(request):
    dict_resp = auth_check(request, "GET", check_login=False)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        mobile = request.GET.get("mobile", "")
        dict_resp = agents.api_send_bind_messagecode(mobile, check_account_exist=True, check_user_bind=False)
        return response200(dict_resp)

    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)


def api_send_parent_bind_messagecode(request):
    dict_resp = auth_check(request, "GET", check_login=False)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        mobile = request.GET.get("mobile", "")
        dict_resp = agents.api_send_bind_messagecode(mobile, check_account_exist=False, check_user_bind=False)
        return response200(dict_resp)

    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)


def api_bind_teacher(request):
    dict_resp = auth_check(request, "POST", check_login=False)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        mobile = request.POST.get("mobile", "")
        address = request.POST.get("address", "")
        student_list_json = request.POST.get("student_list_json", "")
        messagecode = request.POST.get("messagecode", "")
        openid = request.POST.get("openid", "")
        school_id = request.POST.get("sid", "")
        only_check = request.POST.get("only_check", "")
        dict_resp = agents.api_bind_teacher(openid, school_id, mobile, address, student_list_json, messagecode, only_check=only_check)
        return response200(dict_resp)

    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)


def api_bind_parent(request):
    dict_resp = auth_check(request, "POST", check_login=False)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        mobile = request.POST.get("mobile", "")
        fullname = request.POST.get("fullname", "")
        sex = request.POST.get("sex", "")
        address = request.POST.get("address", "")
        student_list_json = request.POST.get("student_list_json", "")
        messagecode = request.POST.get("messagecode", "")
        openid = request.POST.get("openid", "")
        school_id = request.POST.get("sid", "")
        class_id = request.POST.get("class_id", "")
        only_check = request.POST.get("only_check", "")
        dict_resp = agents.api_bind_parent(openid, school_id, class_id, mobile, address, fullname, sex, student_list_json, messagecode, only_check=only_check)
        return response200(dict_resp)

    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)


def api_add_child_by_parent(request):
    dict_resp = auth_check(request, "POST", check_login=True)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        student_list_json = request.POST.get("student_list_json", "")
        dict_resp = agents.api_add_child_by_parent(request.user, student_list_json)
        return response200(dict_resp)

    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)


def api_invite_parent1(request):
    dict_resp = auth_check(request, "POST", check_login=False)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        parent_id = request.POST.get("parent_id", "")
        parent = get_parentbyid(parent_id)
        user = parent.account

        mobile = request.POST.get("mobile", "")
        fullname = request.POST.get("fullname", "")
        sex = request.POST.get("sex", "")
        address = request.POST.get("address", "")
        # student_list_json = request.POST.get("student_list_json", "")
        messagecode = request.POST.get("messagecode", "")
        school_id = parent.school_id
        relation = request.POST.get("relation", "")
        dict_resp = agents.api_invite_parent1(user, school_id, mobile, address, fullname, sex, relation, messagecode)
        return response200(dict_resp)

    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)


def api_invite_parent(request):
    dict_resp = auth_check(request, "POST", check_login=False)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        parent_id = request.POST.get("parent_id", "")
        parent = get_parentbyid(parent_id)
        school_id = parent.school_id

        mobile = request.POST.get("mobile", "")
        fullname = request.POST.get("fullname", "")
        sex = request.POST.get("sex", "")
        address = request.POST.get("address", "")
        # student_list_json = request.POST.get("student_list_json", "")
        messagecode = request.POST.get("messagecode", "")
        openid = request.POST.get("openid", "")
        # school_id = request.POST.get("sid", "")
        # class_id = request.POST.get("class_id", "")
        relation = request.POST.get("relation", "")
        only_check = request.POST.get("only_check", "")
        dict_resp = agents.api_invite_parent(openid, parent_id, school_id, mobile, address, fullname, sex, relation, messagecode, only_check=only_check)
        # dict_resp = agents.api_bind_parent(openid, school_id, class_id, mobile, address, fullname, sex, student_list_json, messagecode)

        return response200(dict_resp)

    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)


def get_shorturl_id(url, short_url='', add_id_2_shorturl=True):
    # 获取短地址， add_id_2_shorturl 表示将新的短地址数据库记录的的id，拼接到shorturl后面。
    md5str = get_md5(url)
    weixinshorturl = WeixinShortUrl.objects.filter(md5=md5str, del_flag=FLAG_NO).first()

    if not weixinshorturl:
        weixinshorturl = WeixinShortUrl()
        weixinshorturl.origin_url = url
        weixinshorturl.md5 = md5str
        weixinshorturl.save()
        weixinshorturl.short_url = short_url + str(weixinshorturl.id) if add_id_2_shorturl and weixinshorturl.id else short_url
        weixinshorturl.save()

    result = {
        "id": weixinshorturl.id,
        "md5": weixinshorturl.md5,
        "short_url": weixinshorturl.short_url,
        "origin_url": weixinshorturl.origin_url,
    }
    return result


def get_orginurl(shorturl_id, shorturl='', md5='', del_indb=False):
    # del_indb 使用后，自动将短记录在数据库中做物理删除，避免无用数据太多。
    weixinshorturl = WeixinShortUrl.objects.filter(del_flag=0)
    if shorturl_id:
        weixinshorturl = weixinshorturl.filter(id=shorturl_id)

    if shorturl:
        weixinshorturl = weixinshorturl.filter(short_url=shorturl)

    if md5:
        weixinshorturl = weixinshorturl.filter(md5=md5)

    if not weixinshorturl:
        return None
    else:
        weixinshorturl = weixinshorturl.first()

    result = {
        "id": weixinshorturl.id,
        "md5": weixinshorturl.md5,
        "short_url": weixinshorturl.short_url,
        "origin_url": weixinshorturl.origin_url,
    }

    if del_indb:
        WeixinShortUrl.objects.filter(id=weixinshorturl.id).delete()

    return result


def get_md5(str_in):
    hl = hashlib.md5()
    hl.update(str_in.encode(encoding='utf-8'))
    md5str = hl.hexdigest()
    return md5str
