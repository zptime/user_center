# -*- coding=utf-8 -*-

from django.db import models
from user_center.apps.school.models import School, Class, Title
from user_center.apps.account.models import Account
from user_center.apps.common.models import Image
from user_center.apps.subject.models import Subject, Textbook


class Teacher(models.Model):
    school = models.ForeignKey(School, verbose_name=u'所属学校', on_delete=models.PROTECT)
    account = models.ForeignKey(Account, verbose_name=u'账号', on_delete=models.PROTECT)

    id_card = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u'身份证号')
    email = models.CharField(default="", max_length=254, blank=True, null=True, verbose_name=u'邮箱')
    full_name = models.CharField(max_length=30, db_index=True, verbose_name=u'姓名')
    sex = models.CharField(default=u"未设置", max_length=30, choices=((u"未设置", u"未设置"), (u"男", u"男"), (u"女", u"女")), verbose_name=u'性别')
    school_code = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u"教工号")
    tmp_code = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u"临时教工号")

    birthday = models.DateTimeField(blank=True, null=True, verbose_name=u'生日')
    native_place = models.CharField(default="", blank=True, max_length=30, verbose_name=u'籍贯')
    address = models.CharField(default="", blank=True, max_length=128, verbose_name=u'地址')
    image = models.ForeignKey(Image, blank=True, null=True, verbose_name=u'头像', related_name="teacher_photo", on_delete=models.PROTECT)
    banner = models.ForeignKey(Image, blank=True, null=True, verbose_name=u'主页图片', related_name="teacher_banner_img", on_delete=models.PROTECT)

    cls = models.ForeignKey(Class, blank=True, null=True,  verbose_name=u'管理班级', on_delete=models.PROTECT)
    title = models.ForeignKey(Title, blank=True, null=True,  verbose_name=u'职务', on_delete=models.PROTECT)
    kind = models.CharField(default="", blank=True, max_length=30, verbose_name=u'类型')
    is_in = models.BooleanField(default=True, verbose_name=u'是否在校')
    is_available = models.BooleanField(default=True, verbose_name=u'是否有效')

    in_date = models.DateTimeField(blank=True, null=True, verbose_name=u'入校时间')
    out_date = models.DateTimeField(blank=True, null=True, verbose_name=u'出校时间')
    comments = models.CharField(default="", blank=True, max_length=512, verbose_name=u'备注')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "teacher"
        verbose_name_plural = u"教师"
        verbose_name = u"教师"

    def __unicode__(self):
        return self.full_name


class TeacherClass(models.Model):
    teacher = models.ForeignKey(Teacher, verbose_name=u'教师', on_delete=models.PROTECT)
    cls = models.ForeignKey(Class, verbose_name=u'班级', on_delete=models.PROTECT)
    is_master = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否为班主任')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "teacher_class"
        verbose_name_plural = u"教师所授班级"
        verbose_name = u"教师所授班级"

    def __unicode__(self):
        return str(self.id)


class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, verbose_name=u'教师', related_name="teacher_subject_teacher_related",  on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, verbose_name=u'所授科目', related_name="teacher_subject_subject_related", on_delete=models.PROTECT)
    is_current = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否为当前科目')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "teacher_subject"
        verbose_name_plural = u"教师所授科目"
        verbose_name = u"教师所授科目"

    def __unicode__(self):
        return str(self.id)


class TeacherTextbook(models.Model):
    teacher = models.ForeignKey(Teacher, verbose_name=u'教师',  related_name="teacher_textbook_teacher_related", on_delete=models.PROTECT)
    textbook = models.ForeignKey(Textbook, verbose_name=u'所授教材', related_name="teacher_textbook_textbook_related", on_delete=models.PROTECT)
    is_current = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否为当前教材')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "teacher_textbook"
        verbose_name_plural = u"教师使用教材"
        verbose_name = u"教师使用教材"

    def __unicode__(self):
        return str(self.id)
