#!/usr/bin/python
# -*- coding=utf-8 -*-

from urllib import unquote
from django.shortcuts import render_to_response
from django.contrib.auth.models import AnonymousUser
from user_center.apps.account.agents import *
from user_center.utils.request_auth import *
from user_center.utils.constant import *
from django.contrib.auth import logout
from django_cas_ng import views as cas_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
import logging
from user_center.utils.weixin_auth import page_login_require, get_fh_openid

logger = logging.getLogger(__name__)

def get_param_val(full_path, name, default=''):
    index = full_path.find('?')
    if index > -1:
        param_path = full_path[index+1:]
        params = param_path.split('&')
        for param in params:
            pos_name = param.find(name)
            if pos_name>-1:
                pos_flag = param.find('=')
                if pos_flag>0:
                    return param[pos_flag+1:]
    return default

def page_login(request, next_page=None):
    if not isinstance(request.user, AnonymousUser):
        page_logout(request)
    if settings.CAS_AUTH:
        return cas_views.login(request, next_page=next_page)
    else:
        return render_to_response('page/base/login/login.html')

def page_logout(request):
    if settings.CAS_AUTH:
        return cas_views.logout(request)
    else:
        logout(request)
        return page_login(request)

def page_findpassword1(request):
    return render_to_response('page/base/login/findpassword/step1.html')

def page_findpassword2(request):
    mobile = request.GET.get('mobile', '')
    params = {'mobile': mobile}
    return render_to_response('page/base/login/findpassword/step2.html', params)

def page_findpassword3(request):
    mobile = request.GET.get('mobile', '')
    params = {'mobile': mobile}
    return render_to_response('page/base/login/findpassword/step3.html', params)

def page_findpassword4(request):
    return render_to_response('page/base/login/findpassword/success.html')

def page_root(request):
    if isinstance(request.user, AnonymousUser):
        return page_login(request)
    else:
        return page_index(request)

@login_required()
def page_index(request):
    if request.user.is_admin: #后台管理员身份
        baseroot_canbe_schoolsysadmin = True
        # 后台管理员兼任学校系统管理员参数baseroot_canbe_schoolsysadmin 配置为true时，默认访问学校管理中心应用，需要通过'/root/index'访问后台管理
        # 配置为false时，默认访问后台管理，只能访问后台管理，需要创建一个学校系统管理员用户去访问学校管理中心应用。
        if fun_schoolsysadmin(request) and baseroot_canbe_schoolsysadmin:
            return page_school_index(request)
        return page_root_index(request)
    else:
        nav_list, user_role_list = get_user_permission(request.user)
        if len(nav_list)<= 0: #学校管理中心视图数量小于等于0
            if request.user.type in [ USER_TYPE_STUDENT, USER_TYPE_TEACHER, USER_TYPE_PARENT ] :
                return page_person_index(request)
            else:
                return page_300(request)
        else:
            return page_school_index(request)

#后台管理入口
def page_root_index(request):
    if isinstance(request.user, AnonymousUser):
        return page_login(request)
    else:
        if request.user.is_admin:
            full_path = unquote(request.get_full_path())
            cuspath = get_param_val(full_path,'cuspath')
            if cuspath != '':
                return page_cuspath(request)
            else:
                nav_val = get_param_val(full_path,'nav','subject')
                params = {'nav_val': nav_val}
                path = 'page/root/'+nav_val+'/main.html'
                return render_to_response(path, params)
        else:
            return page_300(request)


@login_required()
def page_application_main(request):
    return render_to_response('page/school/manage/student/application_main.html')


def page_cuspath(request):
    params = {}
    full_path = unquote(request.get_full_path())
    index = full_path.find('?')
    if index > -1:
        param_path = full_path[index+1:]
        # param_path = 'cuspath=page/root/textbook/chapter.html&textbookId=4'
        param_list = param_path.split('&')
        for item in param_list:
            pos_flag = item.find('=')
            if pos_flag>0:
                key = item[0:pos_flag]
                value = item[pos_flag+1:]
                if key!= 'cuspath':
                    params[key] = value
    path = get_param_val(full_path,'cuspath')
    return render_to_response(path, params)


#学校管理中心应用入口
def page_school_index(request):
    params = {}
    nav_list = []
    nav_val = ''
    view_val = ''
    #一级、二级导航权限
    view_list, user_role_list = get_user_permission(request.user)
    role_mask = convert_user_role_list_to_mask(user_role_list)
    if len(view_list) <= 0:
        return page_300(request)
    if MODULE_SYSTEM in view_list:
        nav_list = ['manage','config']
        view_list = ['student','teacher','parent','class','duty','periodsection','manager','upgrade','classstyle','subject','textbook']
    else:
        nav_list = ['manage']
    params['nav_list'] = nav_list
    params['role_mask'] = role_mask
    params['view_list'] = view_list
    #一级、二级导航视图
    full_path = unquote(request.get_full_path())
    cur_nav_val = get_param_val(full_path,'nav')
    if cur_nav_val == '':
        nav_val = 'manage'
        recache = 'true'
    else:
        nav_val = cur_nav_val
        recache = 'false'
    if nav_val == 'config':
        view_val = get_param_val(full_path,'view','periodsection')
    elif nav_val == 'manage':
        view_val = get_param_val(full_path,'view',view_list[0])
    params['recache'] = recache
    params['nav_val'] = nav_val
    params['view_val'] = view_val
    #用户个人信息
    teacher = api_detail_account(request.user)["d"][0]
    params['account_id'] = teacher['account_id']
    params['id'] = teacher['id']
    params['full_name'] = teacher['full_name']
    path = 'page/school/'+nav_val+'/'+view_val+'/main.html'
    return render_to_response(path, params)

#个人中心应用入口
def page_person_index(request):
    if isinstance(request.user, AnonymousUser):
        return page_login(request)
    else:
        full_path = unquote(request.get_full_path())
        nav_val = get_param_val(full_path,'nav','info')
        if nav_val not in [ 'class','family','identity','info','security','share']:
            nav_val = 'info'
            # return page_300(request)
        user_type = request.user.type
        user_detail = api_detail_account(request.user)["d"][0]
        params = {'nav_val':nav_val, 'user_type':user_type, 'user_type_student':USER_TYPE_STUDENT, 'user_type_teacher': USER_TYPE_TEACHER, 'user_type_parent':USER_TYPE_PARENT,
                  'account_id':user_detail['account_id'], 'id':user_detail['id'], 'full_name': user_detail['full_name']}
        path =  'page/person/'+nav_val+'/main.html'
        return render_to_response(path, params)

#无访问权限
def page_300(request):
    return render_to_response('page/base/300.html')

def fun_schoolsysadmin(request):
    nav_list, user_role_list = get_user_permission(request.user)
    if MODULE_SYSTEM in nav_list:
        return True
    else:
        return False


@page_login_require
@get_fh_openid
def page_mobile(request):
    return render_to_response('mobile/index.html', locals())


def page_mobile_register(request):
    return render_to_response('mobile/index.html', locals())


def page_mobile_parent_invite(request):
    return render_to_response('mobile/index.html', locals())
