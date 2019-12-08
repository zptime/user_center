# -*- coding=utf-8 -*-

from django.db import models
from user_center.apps.school.models import School, Class
from user_center.apps.account.models import Account
from user_center.apps.common.models import Image
from user_center.utils.constant import APPLICATION_STATUS_APPROVED, APPLICATION_STATUS_CHOICE


class Student(models.Model):
    school = models.ForeignKey(School, verbose_name=u'所属学校', on_delete=models.PROTECT)
    account = models.ForeignKey(Account, verbose_name=u'账号', on_delete=models.PROTECT)

    id_card = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u'身份证号')
    email = models.CharField(default="", max_length=254, blank=True, null=True, verbose_name=u'邮箱')
    full_name = models.CharField(max_length=30, db_index=True, verbose_name=u'姓名')
    sex = models.CharField(default=u"未设置", max_length=30, choices=((u"未设置", u"未设置"), (u"男", u"男"), (u"女", u"女")), verbose_name=u'性别')

    birthday = models.DateTimeField(blank=True, null=True, verbose_name=u'生日')
    native_place = models.CharField(default="", max_length=30, verbose_name=u'籍贯')
    address = models.CharField(default="", blank=True, max_length=128, verbose_name=u'地址')
    image = models.ForeignKey(Image, blank=True, null=True, verbose_name=u'头像', related_name="student_photo", on_delete=models.PROTECT)
    banner = models.ForeignKey(Image, blank=True, null=True, verbose_name=u'主页图片', related_name="student_banner_img", on_delete=models.PROTECT)

    cls = models.ForeignKey(Class, null=True, blank=True, verbose_name=u'班级', on_delete=models.PROTECT)
    kind = models.CharField(default="", blank=True, max_length=30, verbose_name=u'学生类型')
    is_in = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否在读')
    is_available = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否有效')

    entry_date = models.DateTimeField(blank=True, null=True, verbose_name=u'入校时间')
    out_date = models.DateTimeField(blank=True, null=True, verbose_name=u'出校时间')
    comments = models.CharField(default="", blank=True, max_length=512, verbose_name=u'备注')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "student"
        verbose_name_plural = u"学生"
        verbose_name = u"学生"

    def __unicode__(self):
        return self.full_name


class StudentClassApplication(models.Model):
    student = models.ForeignKey(Student, verbose_name=u'学生', on_delete=models.PROTECT)
    cls = models.ForeignKey(Class, verbose_name=u'班级', on_delete=models.PROTECT)

    status = models.IntegerField(default=APPLICATION_STATUS_APPROVED, choices=APPLICATION_STATUS_CHOICE, verbose_name=u'处理状态')
    comments = models.CharField(default="", max_length=254, blank=True, null=True, verbose_name=u'申请理由')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "student_class_application"
        verbose_name_plural = u"学生加入班级申请"
        verbose_name = u"学生加入班级申请"

    def __unicode__(self):
        return self.full_name