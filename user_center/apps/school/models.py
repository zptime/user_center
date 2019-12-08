# -*- coding=utf-8 -*-

from django.db import models
from user_center.apps.common.models import Image
from user_center.utils.constant import SCHOOL_PERIOD_CHOICE, SCHOOL_YEARS_CHOICE


class School(models.Model):
    code = models.CharField(max_length=30, verbose_name=u'学校标识码')
    name_simple = models.CharField(default="", blank=True, max_length=30, verbose_name=u'学校简称')
    name_full = models.CharField(max_length=30, verbose_name=u'学校全称')
    name_english = models.CharField(default="", blank=True, max_length=30, verbose_name=u'学校英文名称')
    # org_code = models.CharField(default="", blank=True, max_length=30, verbose_name=u'机构代码')

    property = models.CharField(default="", blank=True, choices=((u"公办", u"公办"), (u"民办", u"民办")), max_length=30,
                                verbose_name=u'学校属性')
    nature = models.CharField(default="", blank=True, choices=((u"部属", u"部属"), (u"省属", u"省属"), (u"市属", u"市属"),
                                                   (u"区属", u"区属")), max_length=30, verbose_name=u'学校性质')
    type = models.CharField(default="", blank=True, choices=((u"小学", u"小学"), (u"初级中学", u"初级中学"), (u"九年一贯制", u"九年一贯制"),
                                                 (u"高级中学", u"高级中学")), max_length=30, verbose_name=u'办学类别')
    primary_years = models.IntegerField(default=0, choices=((0, u"未设置"), (5, u"小学五年制"), (6, u"小学六年制")), verbose_name=u'小学年制')
    junior_years = models.IntegerField(default=0, choices=((0, u"未设置"), (3, u"初中三年制"), (4, u"初中四年制")), verbose_name=u'初中年制')
    senior_years = models.IntegerField(default=0, choices=((0, u"未设置"), (3, u"高中三年制")),verbose_name=u'高中年制')
    academic_year = models.IntegerField(default=0, blank=True, choices=((0, u"未设置"), (3, u"三年制"), (4, u"四年制"),
                                                                        (5, u"五年制"), (6, u"六年制"), (9, u"九年制"),
                                                                        (12, u"十二年制")), verbose_name=u"学制年限")
    province = models.CharField(default="", blank=True, max_length=30, verbose_name=u'省')
    city = models.CharField(default="", blank=True, max_length=30, verbose_name=u'市')
    district = models.CharField(default="", blank=True, max_length=30, verbose_name=u'区/县')
    town = models.CharField(default="", blank=True, max_length=30, verbose_name=u'镇/乡')
    village = models.CharField(default="", blank=True, max_length=30, verbose_name=u'村')
    street = models.CharField(default="", blank=True, max_length=30, verbose_name=u'街道')
    doorplate = models.CharField(default="", blank=True, max_length=30, verbose_name=u'门牌')

    superior_org = models.CharField(default="", blank=True, max_length=30, verbose_name=u'直属主管机构')
    founding_year = models.CharField(default="", blank=True, max_length=30, verbose_name=u'建校年月')
    anniversary = models.CharField(default="", blank=True, max_length=30, verbose_name=u'校庆日')

    phone = models.CharField(default="", blank=True, max_length=30, verbose_name=u'联系电话')
    fox = models.CharField(default="", blank=True, max_length=30, verbose_name=u'传真电话')
    zip = models.CharField(default="", blank=True, max_length=30, verbose_name=u'建校年月')
    web_site = models.CharField(default="", blank=True, max_length=30, verbose_name=u'建校年月')

    contact_person = models.CharField(default="", blank=True, max_length=30, verbose_name=u'联系人姓名')
    contact_mobile = models.CharField(default="", blank=True, max_length=30, verbose_name=u'联系人移动电话')
    contact_title = models.CharField(default="", blank=True, max_length=30, verbose_name=u'联系人职务')
    intro = models.CharField(default="", blank=True, max_length=512, verbose_name=u'学校简介')

    footer = models.CharField(default="", blank=True, max_length=256, verbose_name=u"主页底部显示内容")
    logo = models.ForeignKey(Image, blank=True, null=True, verbose_name=u"学校logo图", on_delete=models.PROTECT)
    title = models.CharField(default="", blank=True, max_length=32, verbose_name=u"学校title显示")

    is_active = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否激活')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "school"
        verbose_name_plural = u"学校"
        verbose_name = u"学校"

    def __unicode__(self):
        return self.name_full


class Grade(models.Model):
    school = models.ForeignKey(School, verbose_name=u'所属学校', on_delete=models.PROTECT)
    grade_num = models.IntegerField(verbose_name=u'年级序号')
    grade_name = models.CharField(default="", max_length=30, verbose_name=u'年级名称')

    class_amount = models.IntegerField(default=0,  blank=True, verbose_name=u'年级班级总数')
    period_grade_num = models.IntegerField(verbose_name=u'学段内年级序号')
    school_period = models.IntegerField(default=0,  blank=True, choices=SCHOOL_PERIOD_CHOICE, verbose_name=u'学段')
    school_years = models.IntegerField(default=0, blank=True, choices=SCHOOL_YEARS_CHOICE, verbose_name=u'年制')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "grade"
        verbose_name_plural = u"年级"
        verbose_name = u"年级"

    def __unicode__(self):
        return self.grade_name


class Class(models.Model):
    school = models.ForeignKey(School, verbose_name=u'所属学校', on_delete=models.PROTECT)
    # teacher = models.ForeignKey(Teacher, verbose_name=u'班主任')
    grade_num = models.IntegerField(default=0, null=True, verbose_name=u"年级编号")  # （1~12）
    period_grade_num = models.IntegerField(default=0, verbose_name=u'学段内年级序号')
    class_num = models.IntegerField(verbose_name=u'班级编号')
    class_name = models.CharField(default="", blank=True, max_length=30, verbose_name=u'班级名称')
    grade_name = models.CharField(default="", blank=True, max_length=30, verbose_name=u'年级名称')
    enrollment_year = models.IntegerField(default=0, verbose_name=u'入学年度')
    graduate_year = models.IntegerField(default=0, blank=True, verbose_name=u'毕业年度')
    graduate_status = models.IntegerField(default=0, choices=((1, u"是"),(0, u"否")), verbose_name=u'是否毕业')

    student_amount = models.IntegerField(default=0,  blank=True, verbose_name=u'班级学生总数')
    class_alias = models.CharField(default="", blank=True, max_length=30, verbose_name=u'班级别名')
    school_period = models.IntegerField(default=0,  blank=True, choices=SCHOOL_PERIOD_CHOICE, verbose_name=u'学段')
    school_years = models.IntegerField(default=0, blank=True, choices=SCHOOL_YEARS_CHOICE, verbose_name=u'年制')
    image = models.ForeignKey(Image, blank=True, null=True, verbose_name=u'图片', on_delete=models.PROTECT)

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "class"
        verbose_name_plural = u"班级"
        verbose_name = u"班级"

    def __unicode__(self):
        return self.class_name


CLASS_STYLE_ARGS_LIST = ["grade_num", "grade_num_cap", "class_num", "class_num_cap", "period_grade_num", "period_grade_num_cap"]


class ClassStyle(models.Model):
    style_example = models.CharField(default='', blank=True, max_length=30, verbose_name=u'样式示例')
    pattern = models.CharField(default='', blank=True, max_length=30, verbose_name=u'样式模式字符串')
    args = models.CharField(default='', blank=True, max_length=30, verbose_name=u'参数列表')

    school_period = models.IntegerField(default=0,  blank=True, choices=SCHOOL_PERIOD_CHOICE, verbose_name=u'学段')
    is_active = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u"是否激活")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = 'class_style'
        verbose_name = u'班级样式'
        verbose_name_plural = u'班级样式'

    def __unicode__(self):
        return self.style_example


class SchoolClassStyle(models.Model):
    school = models.ForeignKey(School, verbose_name=u"所属学校", on_delete=models.PROTECT)
    primary_class_style = models.ForeignKey(ClassStyle, null=True, blank=True, verbose_name=u"小学班级样式", on_delete=models.PROTECT, related_name="primary_class_style_related")
    junior_class_style = models.ForeignKey(ClassStyle, null=True, blank=True, verbose_name=u"初中班级样式", on_delete=models.PROTECT, related_name="junior_class_style_related")
    senior_class_style = models.ForeignKey(ClassStyle, null=True, blank=True, verbose_name=u"高中班级样式", on_delete=models.PROTECT, related_name="senior_class_style_related")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = 'school_class_style'
        verbose_name = u'学校班级样式'
        verbose_name_plural = u'学校班级样式'

    def __unicode__(self):
        return str(self.id)


class UpdateManagement(models.Model):
    school = models.ForeignKey(School, verbose_name=u"所属学校", on_delete=models.PROTECT)
    cur_term = models.IntegerField(default=None, blank=True, null=True, verbose_name=u'当前学年')
    update_month = models.IntegerField(blank=True, null=True, verbose_name=u'自动升年级月份')
    update_day = models.IntegerField(blank=True, null=True, verbose_name=u'自动升年级日期')
    auto_status = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'自动升级状态')
    manual_status = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'手动升级状态')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = 'update_management'
        verbose_name = u'升级管理'
        verbose_name_plural = u'升级管理'

    def __unicode__(self):
        return self.__class__.__name__


class Title(models.Model):
    school = models.ForeignKey(School, verbose_name=u"所属学校", related_name="title_school_related", on_delete=models.PROTECT)
    name = models.CharField(default='', max_length=30, verbose_name=u'职务名称')
    type = models.IntegerField(default=2, choices=((1, u"系统内置"), (2, u"用户自定义")), verbose_name=u'职务类型')
    comments = models.CharField(default='', max_length=256, verbose_name=u'职务名称')
    teacher_amount = models.IntegerField(default=0, blank=True, verbose_name=u'教师人数')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = 'title'
        verbose_name = u'职务'
        verbose_name_plural = u'职务'

    def __unicode__(self):
        return self.name
