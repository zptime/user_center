# -*- coding=utf-8 -*-

from django.db import models
from user_center.apps.school.models import School
from user_center.apps.account.models import Account
from user_center.apps.student.models import Student
from user_center.apps.common.models import Image
from user_center.utils.constant import APPLICATION_STATUS_APPROVED, APPLICATION_STATUS_CHOICE

class Parent(models.Model):
    school = models.ForeignKey(School, verbose_name=u'所属学校', on_delete=models.PROTECT)
    account = models.ForeignKey(Account, verbose_name=u'账号', related_name="parent_account", on_delete=models.PROTECT)

    id_card = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u'身份证号')
    email = models.CharField(default="", max_length=254, blank=True, null=True, verbose_name=u'邮箱')
    full_name = models.CharField(max_length=30, db_index=True, verbose_name=u'姓名')
    sex = models.CharField(default=u"未设置", max_length=30, choices=((u"未设置", u"未设置"), (u"男", u"男"), (u"女", u"女")), verbose_name=u'性别')

    birthday = models.DateTimeField(blank=True, null=True, verbose_name=u'生日')
    native_place = models.CharField(default="", max_length=30, verbose_name=u'籍贯')
    address = models.CharField(default="", blank=True, max_length=128, verbose_name=u'地址')
    company = models.CharField(default="", blank=True,  max_length=30, verbose_name=u'单位')
    image = models.ForeignKey(Image, blank=True, null=True, verbose_name=u'头像', related_name="parent_photo", on_delete=models.PROTECT)
    banner = models.ForeignKey(Image, blank=True, null=True, verbose_name=u'主页图片', related_name="parent_banner_img", on_delete=models.PROTECT)

    comments = models.CharField(default="",  blank=True, max_length=512, verbose_name=u'备注')
    is_active = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否激活')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "parent"
        verbose_name_plural = u"家长"
        verbose_name = u"家长"

    def __unicode__(self):
        return self.full_name


class ParentStudent(models.Model):
    parent = models.ForeignKey(Parent, verbose_name=u'家长', on_delete=models.PROTECT)
    student = models.ForeignKey(Student, verbose_name=u'孩子', related_name="child_account", on_delete=models.PROTECT)
    relation = models.CharField(default="",  blank=True, max_length=30, verbose_name=u'所属关系')
    comments = models.CharField(default="",  blank=True, max_length=512, verbose_name=u'备注')
    status = models.IntegerField(default=APPLICATION_STATUS_APPROVED[0], choices=APPLICATION_STATUS_CHOICE, verbose_name=u'处理状态')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "parent_student"
        verbose_name_plural = u"家长学生"
        verbose_name = u"家长学生"

    def __unicode__(self):
        return str(self.id)