# -*- coding=utf-8 -*-

from django.db import models
from user_center.apps.teacher.models import Teacher
from user_center.apps.school.models import School
from user_center.utils.constant import *
from user_center.apps.common.models import Image


class Service(models.Model):
    code = models.CharField(max_length=30, verbose_name=u'服务编码')
    name = models.CharField(max_length=30, verbose_name=u'服务名称')
    type = models.IntegerField(default=0, choices=((1, u"内部服务"), (2, u"第三方服务")), verbose_name=u'服务类型')
    intranet_url = models.CharField(default="", max_length=256, blank=True, verbose_name=u'内网服务访问地址')
    internet_url = models.CharField(default="", max_length=256, blank=True, verbose_name=u'外网服务访问地址')
    access_key = models.CharField(default="", blank=True, max_length=30, verbose_name=u'服务访问ID')
    secret_key = models.CharField(default="", blank=True, max_length=30, verbose_name=u'服务访问密钥')
    comments = models.CharField(default="", blank=True, max_length=512, verbose_name=u'备注')
    image = models.ForeignKey(Image, blank=True, null=True, verbose_name=u'图片', on_delete=models.PROTECT)

    access_mask = models.IntegerField(default=7, choices=SERVICE_ACCESS_MASK_CHOICE, verbose_name=u"允许访问的用户类型")
    is_cls_adviser_as_mgr = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'班主任是否视为管理员')

    classify = models.IntegerField(default=0, choices=SERVICE_CLASSIFY_CHOICE, verbose_name=u"服务归类管理")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "service"
        verbose_name_plural = u"服务"
        verbose_name = u"服务"

    def __unicode__(self):
        return self.name


class Subnet(models.Model):
    cidr = models.CharField(max_length=30, verbose_name=u'子网描述字符串CIDR')
    comments = models.CharField(default="", blank=True, max_length=512, verbose_name=u'备注')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "subnet"
        verbose_name_plural = u"内网子网"
        verbose_name = u"内网子网"

    def __unicode__(self):
        return self.cidr


class Role(models.Model):
    service = models.ForeignKey(Service, verbose_name=u'所属服务', on_delete=models.PROTECT)
    code = models.CharField(default="", max_length=30, verbose_name=u'角色编号')
    name = models.CharField(default="", max_length=30, verbose_name=u'角色名称')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "role"
        verbose_name_plural = u"角色"
        verbose_name = u"角色"

    def __unicode__(self):
        return self.name


class UserRole(models.Model):
    school = models.ForeignKey(School, verbose_name=u'学校', on_delete=models.PROTECT)
    role = models.ForeignKey(Role, verbose_name=u'用户角色', on_delete=models.PROTECT)
    user = models.ForeignKey(Teacher, verbose_name=u'用户', on_delete=models.PROTECT)

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "user_role"
        verbose_name_plural = u"用户角色"
        verbose_name = u"用户角色"

    def __unicode__(self):
        return str(self.id)


class SchoolService(models.Model):
    service = models.ForeignKey(Service, verbose_name=u'服务', on_delete=models.PROTECT)
    school = models.ForeignKey(School, verbose_name=u'学校', on_delete=models.PROTECT)

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "school_service"
        verbose_name_plural = u"学校服务"
        verbose_name = u"学校服务"

    def __unicode__(self):
        return str(self.id)


class Parameter(models.Model):
    service = models.ForeignKey(Service, verbose_name=u'所属服务', on_delete=models.PROTECT)
    name = models.CharField(default="", max_length=30, verbose_name=u'参数名')
    default_value = models.CharField(default="", blank=True, max_length=1024, verbose_name=u'参数默认值')
    comments = models.CharField(default="", blank=True, max_length=1024, verbose_name=u'参数说明')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "service_parameter"
        verbose_name_plural = u"服务参数"
        verbose_name = u"服务参数"

    def __unicode__(self):
        return self.name


class SchoolParameter(models.Model):
    parameter = models.ForeignKey(Parameter, verbose_name=u'参数', on_delete=models.PROTECT)
    school = models.ForeignKey(School, verbose_name=u'学校', on_delete=models.PROTECT)
    value = models.CharField(default="", blank=True, max_length=1024, verbose_name=u'参数值')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "school_parameter"
        verbose_name_plural = u"学校服务参数"
        verbose_name = u"学校服务参数"

    def __unicode__(self):
        return str(self.id)
