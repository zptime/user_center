# -*- coding=utf-8 -*-

from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'图片名称')
    url = models.CharField(max_length=255, verbose_name=u'图片路径')
    size = models.IntegerField(default=0,  verbose_name=u'图片大小')

    uploader = models.IntegerField(default=0, verbose_name=u'上传者帐号ID')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "image"
        verbose_name_plural = u"图片"
        verbose_name = u"图片"

    def __unicode__(self):
        return self.name


class VerifyCode(models.Model):
    mobile = models.CharField(default="", max_length=30, blank=True, null=True, verbose_name=u"手机号")
    IMCode_status = models.IntegerField(default=0,choices=((0, u"未验证"), (1, u"已验证")), verbose_name=u"图片验证码状态")
    code = models.CharField(default='', max_length=30, blank=True, null=True, verbose_name=u"短信验证码")
    timestamp = models.CharField(default="", max_length=30, blank=True, null=True, verbose_name=u"短信验证码生成时间戳")
    code_status = models.IntegerField(default=0, choices=((0, u"未验证"), (1, u"已验证")), verbose_name=u"短信验证码验证状态")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "verifycode"
        verbose_name = u'验证码'
        verbose_name_plural = u"验证码"

    def __unicode__(self):
        return self.__class__.__name__


