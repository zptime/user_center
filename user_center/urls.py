#!/usr/bin/python
# -*- coding=utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django_cas_ng import views as cas_views

admin.autodiscover()

urlpatterns =[
    url(r'^admin/', include(admin.site.urls)),
]

from user_center.apps.page.views import *
urlpatterns += [
    #智慧校园主页
    url(r'^$', page_root),
    url(r'^login/$', page_login),
    url(r'^logout/$', page_logout),
    # url(r'^m/$', page_mobile_root),
    url(r'^m/register/', page_mobile_register),  # 注册页面不需要登陆
    url(r'^m/personal/parent/addParent', page_mobile_parent_invite),  # 家长邀请其它家长不需要登陆
    url(r'^m/', page_mobile),

    #找回密码
    url(r'^findpassword1/$', page_findpassword1),
    url(r'^findpassword2/$', page_findpassword2),
    url(r'^findpassword3/$', page_findpassword3),
    url(r'^findpassword4/$', page_findpassword4),

    #学校管理中心
    url(r'^index$', page_index),
    url(r'^root/index$', page_root_index),
    url(r'^page/application/main$', page_application_main),

    #个人中心
    url(r'^person/index$', page_person_index),
]

from user_center.apps.account.views import *
urlpatterns += [
    url(r'^api/login$', api_login),
    url(r'^api/logout$', api_logout),
    url(r'^api/reset/password$', api_reset_password),
    url(r'^api/batch_reset/password$', api_batch_reset_password),
    url(r'^api/check/username$', api_check_username),
    url(r'^api/detail/account$', api_detail_account),
    url(r'^api/list/user_type$', api_list_user_type),
    url(r'^api/change/user_type$', api_change_user_type),
    url(r'^api/reset/mobile$', api_reset_mobile),
    url(r'^api/detail/account_by_mobile$', api_detail_account_by_mobile),

    url(r'^user_center/api/detail/account$', api_detail_account),
    url(r'^user_center/api/list/user_type$', api_list_user_type),
    url(r'^user_center/api/change/user_type$', api_change_user_type),

    url(r'^user_center/api/logout$', api_logout),
]

from user_center.apps.student.views import *
urlpatterns += [
    url(r'^api/list/student$', api_list_student),
    url(r'^api/detail/student$', api_detail_student),
    url(r'^api/update/student$', api_update_student),
    url(r'^api/add/student$', api_add_student),
    url(r'^api/delete/student$', api_delete_student),
    url(r'^api/export/student$', api_export_student),
    url(r'^api/import/student$', api_import_student),
    url(r'^api/update/student_class$', api_update_student_class),
    url(r'^api/add/student_class_application$', api_add_student_class_application),
    url(r'^api/delete/student_class_application$', api_delete_student_class_application),
    url(r'^api/update/student_class_application$', api_update_student_class_application),
    url(r'^api/list/student_class_application$', api_list_student_class_application),
    url(r'^api/detail/student_class_application$', api_detail_student_class_application),
]

from user_center.apps.parent.views import *
urlpatterns += [
    url(r'^api/list/parent$', api_list_parent),
    url(r'^api/list/student_parent$', api_list_student_parent),
    url(r'^api/detail/parent$', api_detail_parent),
    url(r'^api/update/parent$', api_update_parent),
    url(r'^api/add/parent$', api_add_parent),
    url(r'^api/delete/parent$', api_delete_parent),
    url(r'^api/active/parent$', api_active_parent),
    url(r'^api/import/parent$', api_import_parent),
    url(r'^api/export/parent$', api_export_parent),

    url(r'^api/list/parent_student$', api_list_parent_student),
    url(r'^api/delete/parent_student$', api_delete_parent_student),
    url(r'^api/update/parent_student$', api_update_parent_student),
    url(r'^api/add/parent_by_student$', api_add_parent_by_student),
]

from user_center.apps.service.views import *
urlpatterns += [
    url(r'^api/list/admin_user$', api_list_admin_user),
    url(r'^api/list/admin_role$', api_list_admin_role),
    url(r'^api/update/admin_user$', api_update_admin_user),
    url(r'^api/delete/admin_user$', api_delete_admin_user),
    url(r'^api/export/admin_user$', api_export_admin_user),
    url(r'^api/list/role_user$', api_list_role_user),
    url(r'^api/update/role_user$', api_update_role_user),
    url(r'^api/list/service_apps$', api_list_service_apps),

    url(r'^user_center/api/list/service_apps$', api_list_service_apps),
]

from user_center.apps.open.views import *
urlpatterns += [
    url(r'^open/list/subnet$', open_list_subnet),
    url(r'^open/detail/update_time$', open_detail_update_time),
    url(r'^open/list/items$', open_list_items),
    url(r'^open/call/api$', open_call_api),
    url(r'^open/reset/password$', open_reset_password),

    # 第三方接入
    url(r'^open/redirect/service_url$', open_redirect_service_url),  # 跳转至第三方平台
    url(r'^open/app/auth$', open_app_auth),  # 从第三方平台跳转
    url(r'^open/check/token$', open_check_token),  # 检查用户是已经登录
    url(r'^open/check/wxtoken$', open_check_wxtoken),  # 通过微信token获取用户账号密码
    url(r'^open/list/school', open_list_school),
    url(r'^open/list/student', open_list_student),
    url(r'^open/list/teacher', open_list_teacher),
    url(r'^open/list/class', open_list_class),
]

from user_center.apps.api.views import *
urlpatterns += [
    url(r'^api/$', api_index),
    url(r'^api/docs/$', api_docs),
    # url(r'^api/docs/(?P<json>\w+)/$', 'module'),
]

from user_center.apps.school.views import *
urlpatterns += [
    # 班级
    url(r'^api/list/class$', api_list_class),
    url(r'^api/list/graduated_class$', api_list_graduated_class),
    url(r'^api/add/grade_class$', api_add_grade_class),
    url(r'^api/delete/class$', api_delete_class),
    url(r'^api/add/class$',api_add_class),
    url(r'^api/update/class$', api_update_class),
    # 班级样式
    url(r'^api/list/class_style$', api_list_class_style),
    url(r'^api/detail/class_style$', api_detail_class_style),
    url(r'^api/update/class_style$', api_update_class_style),
    # 学校
    url(r'^api/detail/school$', api_detail_school),
    url(r'^api/update/learning_period', api_update_learning_period),
    url(r'^api/list/grade$', api_list_grade),
    url(r'^api/annually_update/grade$', api_annually_update),  # 手动升年级
    url(r'^api/undo_update/grade$', api_undo_update),  # 撤销升年级
    url(r'^api/display/update_time$', api_display_update_time),
    url(r'^api/config/update_time$', api_config_update_time),
    url(r'^api/display/current_term$', api_display_current_term),
    # 职务
    url(r'^api/add/title$', api_add_title),
    url(r'^api/update/title$', api_update_title),
    url(r'^api/delete/title$', api_delete_title),
    url(r'^api/list/title$', api_list_title),

    url(r'^user_center/api/list/class$', api_list_class),
    url(r'^user_center/api/list/grade$', api_list_grade),

    # 后台管理
    url(r'^api/admin/list/school$', api_admin_list_school),
    url(r'^api/admin/list/service$', api_admin_list_service),
    url(r'^api/admin/add/school', api_admin_add_school),
    url(r'^api/admin/delete/school', api_admin_delete_school),
    url(r'^api/admin/update/school_service$', api_admin_update_school_service),
    url(r'^api/admin/add/manager$', api_admin_add_manager),
]

from user_center.apps.teacher.views import *
urlpatterns += [
    url(r'^api/list/teacher$', api_list_teacher),
    url(r'^api/detail/teacher$', api_detail_teacher),
    url(r'^api/update/teacher$', api_update_teacher),
    url(r'^api/delete/teacher$', api_delete_teacher),
    url(r'^api/leave/teacher$', api_leave_teacher),
    url(r'^api/add/teacher$', api_add_teacher),
    url(r'^api/export/teacher$', api_export_teacher),
    url(r'^api/import/teacher$', api_import_teacher),
    url(r'^api/list/teacher_class$', api_list_teacher_class),
    url(r'^api/delete/teacher_class$', api_delete_teacher_class),
    url(r'^api/add/teacher_class$', api_add_teacher_class),
    url(r'^api/list/teacher_textbook$', api_list_teacher_textbook),
    url(r'^api/delete/teacher_textbook$', api_delete_teacher_textbook),
    url(r'^api/add/teacher_textbook$', api_add_teacher_textbook),
    url(r'^api/update/teacher_textbook$', api_update_teacher_textbook),

    url(r'^user_center/api/list/teacher_textbook$', api_list_teacher_textbook),
    url(r'^user_center/api/update/teacher_textbook$', api_update_teacher_textbook),
    url(r'^user_center/api/add/teacher_textbook$', api_add_teacher_textbook),
    url(r'^user_center/api/delete/teacher_textbook$', api_delete_teacher_textbook),
    url(r'^user_center/api/list/teacher_class$', api_list_teacher_class),
    url(r'^user_center/api/delete/teacher_class$', api_delete_teacher_class),
    url(r'^user_center/api/add/teacher_class$', api_add_teacher_class),

]

from user_center.apps.common.views import *
urlpatterns += [
    url(r'^api/upload/image$', api_upload_image),
    url(r'^api/common/upload/image$', api_upload_image_v2),  # 为兼容移动端改造接口格式
    url(r'^api/get/imagecode$', api_get_imagecode),
    url(r'^api/verify/imagecode$', api_verify_imagecode),
    url(r'^api/send/messagecode$', api_send_messagecode),
    url(r'api/verify/messagecode$', api_verify_messagecode),
    url(r'api/unset/password$', api_unset_password),
    url(r'^api/check/imagecode$', api_check_imagecode),
    url(r'^user_center/api/get/user_center_url$', api_get_user_center_url),
]

from user_center.apps.subject.views import *
urlpatterns += [
    url(r'^api/admin_add/subject$', api_admin_add_subject),
    url(r'^api/admin_list/subject$', api_admin_list_subject),
    url(r'^api/admin_edit/subject$', api_admin_edit_subject),
    url(r'^api/admin_freeze/subject$', api_admin_freeze_subject),
    url(r'^api/admin_unfreeze/subject$', api_admin_unfreeze_subject),
    url(r'^api/admin_delete/subject$', api_admin_delete_subject),
    url(r'^api/admin_import/subject$', api_admin_import_subject),
    url(r'^api/admin_export/subject$', api_admin_export_subject),
    url(r'^api/school_add/subject$', api_school_add_subject),
    url(r'^api/school_check/subject$', api_school_check_subject),
    url(r'^api/school_update/subject$', api_school_update_subject),
    url(r'^api/school_list/subject$', api_school_list_subject),
    url(r'^api/school_delete/subject$', api_school_delete_subject),
    url(r'^api/admin_add/textbook$', api_admin_add_textbook),
    url(r'^api/admin_list/textbook$', api_admin_list_textbook),
    url(r'^api/admin_detail/textbook$', api_admin_detail_textbook),
    url(r'^api/admin_edit/textbook$', api_admin_edit_textbook),
    url(r'^api/admin_freeze/textbook$', api_admin_freeze_textbook),
    url(r'^api/admin_unfreeze/textbook$', api_admin_unfreeze_textbook),
    url(r'^api/admin_delete/textbook$', api_admin_delete_textbook),
    url(r'^api/school_add/textbook$', api_school_add_textbook),
    url(r'^api/school_list/textbook$', api_school_list_textbook),
    url(r'^api/school_delete/textbook$', api_school_delete_textbook),
    url(r'^api/admin_add/chapter$', api_admin_add_chapter),
    url(r'^api/admin_list/chapter$', api_admin_list_chapter),
    url(r'^api/admin_edit/chapter$', api_admin_edit_chapter),
    url(r'^api/admin_move/chapter$', api_admin_move_chapter),
    url(r'^api/admin_delete/chapter$', api_admin_delete_chapter),

    url(r'^user_center/api/school_list/subject$', api_school_list_subject),
    url(r'^user_center/api/school_list/textbook$', api_school_list_textbook),
]

from user_center.apps.weixinmp.views import *
urlpatterns += [
    # 下面两个接口比较危险，用于测试使用，否则有安全问题。上线时请关闭
    url(r'^update/access_token$', update_weixin_global_access_token),  # 微信强制刷新全局access_token
    url(r'^get/access_token$', get_weixin_global_access_token),  # 微信获取全局access_token

    # 获取用户资料，判断用户绑等信息，不直接由前台调用，由后台控制页面跳转流程。
    url(r'^MP_verify_jIjfmE2UW1zSOJPc.txt$', wx_get_verifyfile),  # 微信烽火公众号域名验证
    url(r'^MP_verify_PPYnxDn0rz5Y03R1.txt$', wx_get_hkfxverifyfile),  # 微信华科附小公众号域名验证
    url(r'^wx/authorize$', wx_get_code),  # 获取用户资料前，先获取code
    url(r'^wx/access_token$', wx_code_to_access_token),  # 根据code获取用户信息
    url(r'^wx/authorize_fh$', wx_get_code_fh),  # 获取烽火openid对应的code
    url(r'^wx/access_token_fh$', wx_code_to_access_token_fh),  # 根据烽火code获取用户openid
    url(r'^wx/authorize_fhlogin$', wx_get_code_fhlogin),  # 扫码获得烽火公众号openid后直接登陆系统。本步骤为先获取code
    url(r'^wx/access_token_fhlogin$', wx_code_to_access_token_fhlogin),  # 扫码获得烽火公众号openid后直接登陆系统。

    # 烽火二维码扫码相关接口。
    url(r'^api/wx/fh/qrcode$', api_fh_qrcode),  # 获取烽火二维码，用户扫码后，登录到手机端。

    # jsapi相关接口
    url(r'^wx/get/jsconfig$', wx_get_jsconfig),  # 供前端获取调用jsapi前的一些信息。
    url(r'^wx/mod/webdebugmod$', wx_mod_debugstatus),  # 供前端获取调用jsapi前的一些信息。

    url(r'^api/wx/service/list$', wx_service_list),  # 供前端获取调用jsapi前的一些信息。
    url(r'^api/wx/service/domain$', wx_service_domain),  # 获取app对应的域名。
    url(r'^api/wx/class/qrcode$', api_class_qrcode),  # 获取班级二维码,没有找到应用场景，未来再实现。
    url(r'^api/wx/school/qrcode$', api_school_qrcode),  # 获取学校绑定家长二维码地址
    url(r'^api/wx/parent/qrcode$', api_parent_qrcode),  # 获取家长推荐其它家长二维码地址
    url(r'^api/wx/get/accountopenid$', api_get_accountopenid),  # 根据accountid和学校ID列表，获取openid
    url(r'^api/wx/send/teacherbind/messagecode$', api_send_teacher_bind_messagecode),  # 发送老师绑定短信
    url(r'^api/wx/send/parentbind/messagecode$', api_send_parent_bind_messagecode),  # 发送家长绑定短信
    url(r'^api/wx/bind/teacher$', api_bind_teacher),  # 老师绑定微信号,调用本接口前，先调用api/wx/send/teacherbind/messagecode获取验证码
    url(r'^api/wx/bind/parent$', api_bind_parent),  # 家长绑定微信号,调用本接口前，先调用api/wx/send/parentbind/messagecode获取验证码
    url(r'^api/wx/add/child_by_parent$', api_add_child_by_parent),  # 家长给本人添加孩子
    url(r'^api/wx/invite/parent$', api_invite_parent),  # 家长邀请其它家长，先调用api/wx/send/parentbind/messagecode获取验证码


    # url(r'^api/openid/bindstatus$', api_openid_bindstatus),
]

from user_center.apps.weixinpages.views import *
urlpatterns += [
    url(r'^test/page$', test_page),
    url(r'^wx/page/scan/fhcode$', weixin_scan_fhcode),   # 已经绑定微信的华校任意学校的用户，扫烽火二维码登陆
    url(r'^wx/page/scan/schoolcode$', weixin_homepage),   # 扫学校码进入的页面,如果绑定了，则跳转到微信首页，如果没有绑定，则跳转到家长绑定页面。
    url(r'^wx/page/scan/parentcode$', weixin_homepage),   # 扫家长邀请码进入的页面,如果绑定了，则跳转到微信首页，如果没有绑定，则跳转到家长邀请绑定页面。
    url(r'^wx/page/add/role$', weixin_homepage),   # 用户到个人中心添加身份时，跳转页面。
]

# urlpatterns += patterns('',
#     url(r'^login/$', cas_views.login, name='cas_ng_login'),
#     url(r'^logout/$', cas_views.logout, name='cas_ng_logout'),
# )

# Development
from django.conf import settings
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    media = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = media + staticfiles_urlpatterns() + urlpatterns

# 初始化数据库数据
from user_center.apps.service import agents as service_agents
service_agents.init_service()

from user_center.apps.school import school_agents
school_agents.init_school_db()
