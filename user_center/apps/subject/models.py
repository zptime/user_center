# -*- coding=utf-8 -*-

from django.db import models
from user_center.apps.school.models import School
from user_center.apps.account.models import Account
from user_center.apps.common.models import Image
from user_center.utils.constant import GRADE_NUM_CHOICE, GRADE_NUM_NOT_SET


class Subject(models.Model):
    name = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u'名称')
    is_active = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否生效')
    editor = models.ForeignKey(Account, blank=True, null=True, verbose_name=u'编辑者', on_delete=models.PROTECT)
    image = models.ForeignKey(Image, blank=True, null=True, verbose_name=u'图片', on_delete=models.PROTECT)

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "subject"
        verbose_name_plural = u"科目"
        verbose_name = u"科目"

    def __unicode__(self):
        return self.name


class Textbook(models.Model):
    name = models.CharField(default="", max_length=128, blank=True, db_index=True, verbose_name=u'名称')
    is_active = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否生效')
    editor = models.ForeignKey(Account, blank=True, null=True, verbose_name=u'编辑者', on_delete=models.PROTECT)
    image = models.ForeignKey(Image, blank=True, null=True, verbose_name=u'图片', on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, verbose_name=u'科目', on_delete=models.PROTECT)
    grade_num = models.IntegerField(default=GRADE_NUM_NOT_SET[0], choices=GRADE_NUM_CHOICE, verbose_name=u'年级编号')
    chapter_count = models.IntegerField(default=0, verbose_name=u'章节数目')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "textbook"
        verbose_name_plural = u"教材"
        verbose_name = u"教材"

    def __unicode__(self):
        return self.name


class Chapter(models.Model):
    textbook = models.ForeignKey(Textbook, verbose_name=u'教材', on_delete=models.PROTECT)
    name = models.CharField(default="", max_length=128, blank=True, db_index=True, verbose_name=u'名称')
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=u'父节点ID', on_delete=models.PROTECT, related_name="parent_related")
    open = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否展开')
    is_parent = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否为没有子节点的父节点')
    sn = models.IntegerField(null=True, blank=True, verbose_name=u'编号')
    # 备用字段
    up_brother = models.ForeignKey('self', null=True, blank=True, verbose_name=u'上一个的兄弟节点的ID', on_delete=models.PROTECT, related_name="up_brother_related")
    resource_count = models.IntegerField(default=0, verbose_name=u'资源数量')
    is_active = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否生效')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "chapter"
        verbose_name_plural = u"章节"
        verbose_name = u"章节"

    def __unicode__(self):
        return self.name


class SchoolSubject(models.Model):
    subject = models.ForeignKey(Subject, verbose_name=u'科目', on_delete=models.PROTECT)
    school = models.ForeignKey(School, verbose_name=u'学校', on_delete=models.PROTECT)

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "school_subject"
        verbose_name_plural = u"学校开设科目"
        verbose_name = u"学校开设科目"

    def __unicode__(self):
        return str(self.id)


class SchoolTextbook(models.Model):
    textbook = models.ForeignKey(Textbook, verbose_name=u'教材', on_delete=models.PROTECT)
    school = models.ForeignKey(School, verbose_name=u'学校', on_delete=models.PROTECT)

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "school_textbook"
        verbose_name_plural = u"学校使用教材"
        verbose_name = u"学校使用教材"

    def __unicode__(self):
        return str(self.id)
