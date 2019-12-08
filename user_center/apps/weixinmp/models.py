# -*- coding=utf-8 -*-

from django.db import models

from user_center.apps.account.models import Account
from user_center.apps.school.models import School
from user_center.apps.service.models import Service
from user_center.utils.constant import USER_TYPE_ALL


class WeixinSchool(models.Model):
    school = models.ForeignKey(School, verbose_name=u'学校', on_delete=models.PROTECT)
    app_id = models.CharField(max_length=32, verbose_name=u'微信开发者appid')
    app_secret = models.CharField(max_length=64, verbose_name=u'微信开发者app_secret')
    interface_url = models.CharField(default="", blank=True, null=True, max_length=256, verbose_name=u'微信接口url')
    interface_token = models.CharField(default="", blank=True, null=True, max_length=64, verbose_name=u'微信接口interface_token')
    only_request_openid = models.IntegerField(default=1, choices=((1, u"只请求openid"), (0, u"请求全用户资料")), verbose_name=u'是否仅请求openid')  # 仅请求openid则免授权
    access_token = models.CharField(default="", blank=True, null=True, max_length=600, verbose_name=u'微信接口access_token')
    access_token_update_time = models.DateTimeField(default=None, blank=True, null=True, verbose_name=u'access_token下次更新时间')
    jsapi_ticket = models.CharField(default="", blank=True, null=True, max_length=600, verbose_name=u'微信接口jsapi_ticket')
    jsapi_ticket_update_time = models.DateTimeField(default=None, blank=True, null=True, verbose_name=u'jsapi_ticket下次更新时间')
    mp_image_url = models.CharField(default="", blank=True, null=True, max_length=256, verbose_name=u'公众号图片地址')
    mp_follow_url = models.CharField(default="", blank=True, null=True, max_length=256, verbose_name=u'公众号地址')  # 用户点击后直接关注，貌似无法实现，先预留
    force_follow = models.IntegerField(default=1, choices=((1, u"强制关注"), (0, u"不强制关注")), verbose_name=u'是否强制用户关注公众号')  # 仅请求openid则免授权
    desc = models.CharField(default="", blank=True, null=True, max_length=500, verbose_name=u'描述信息')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "weixin_school"
        verbose_name_plural = u"学校微信公众号信息表"
        verbose_name = u"学校微信公众号信息表"

    def __unicode__(self):
        return self.school.name_full + self.app_id


class WeixinAccount(models.Model):
    school = models.ForeignKey(School, verbose_name=u'学校', on_delete=models.PROTECT, default=None)
    account = models.ForeignKey(Account, verbose_name=u'账户', on_delete=models.PROTECT)
    openid = models.CharField(max_length=64, verbose_name=u'微信用户所在学校公众号的openid')
    openid_fh = models.CharField(max_length=64, verbose_name=u'微信用户对应的烽火公众号的openid', default="", blank=True, null=True)
    name = models.CharField(default="", blank=True, null=True, max_length=64, verbose_name=u'微信用户呢称')
    image_url = models.CharField(default="", blank=True, null=True, max_length=512, verbose_name=u'微信用户头像地址')
    province = models.CharField(default="", blank=True, null=True, max_length=32, verbose_name=u'省')
    city = models.CharField(default="", blank=True, null=True, max_length=32, verbose_name=u'市')
    country = models.CharField(default="", blank=True, null=True, max_length=32, verbose_name=u'区')
    sex = models.CharField(default="", blank=True, null=True, max_length=10, verbose_name=u'微信用户性别')
    unionid = models.CharField(default="", blank=True, null=True, max_length=64, verbose_name=u'微信unionid')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "weixin_account"
        verbose_name_plural = u"微信与华校用户关系表"
        verbose_name = u"微信与华校用户关系表"

    def __unicode__(self):
        return self.account.full_name + self.openid


class WeixinService(models.Model):
    entrance = models.CharField(max_length=64, verbose_name=u'入口')
    service = models.ForeignKey(Service, verbose_name=u'服务', on_delete=models.PROTECT)
    support_user_type = models.PositiveSmallIntegerField(u'支持用户类型', default=USER_TYPE_ALL)
    url = models.CharField(default="", blank=True, null=True, max_length=512, verbose_name=u'微信应用图标跳转地址')
    icon = models.CharField(default="", blank=True, null=True, max_length=512, verbose_name=u'微信应用图标图片地址')
    group = models.CharField(default="", blank=True, null=True, max_length=32, verbose_name=u'分组名称')
    sort = models.IntegerField(default=99, verbose_name=u'显示顺序')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "weixin_service"
        verbose_name_plural = u"微信端服务列表"
        verbose_name = u"微信端服务列表"

    def __unicode__(self):
        return self.entrance


class WeixinShortUrl(models.Model):
    origin_url = models.TextField(default="", blank=True, null=True, verbose_name=u'原始URL')
    md5 = models.CharField(default="", blank=True, null=True, max_length=150, verbose_name=u'原始URL的MD5')
    short_url = models.TextField(default="", blank=True, null=True, verbose_name=u'缩短后编码')  # 可以是一个id，也可以是一个新的url
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "weixin_short_url"
        verbose_name_plural = u"微信短url服务"
        verbose_name = u"微信短url服务"

    def __unicode__(self):
        return self.origin_url
