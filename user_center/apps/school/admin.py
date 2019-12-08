#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.contrib import admin
from models import *
from school_agents import init_school


class SchoolAppAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_full',  'code', 'property', 'intro', 'footer', "logo_id", "title", 'del_flag']
    list_filter = ['name_full', 'del_flag']
    search_fields = ["name_full", "code"]

    def save_model(self, request, obj, form, change):
        if obj.primary_years == 0 and obj.junior_years == 0 and obj.senior_years == 0:
            raise Exception(u"至少选择（小学、初中、高中）学段学制")
        obj.save()
        init_school(school_obj=obj)

admin.site.register(School, SchoolAppAdmin)


class GradeAppAdmin(admin.ModelAdmin):
    list_display = ['id', 'school',  'grade_num', 'grade_name', 'del_flag']
    list_filter = ['grade_num', 'del_flag']
    search_fields = ["school__name_full", "grade_num"]

admin.site.register(Grade, GradeAppAdmin)


class ClassAppAdmin(admin.ModelAdmin):
    list_display = ['id', 'school',  'class_num', 'class_name', 'enrollment_year', 'del_flag']
    list_filter = ['class_name', 'del_flag']
    search_fields = ["school__name_full", "class_num"]

admin.site.register(Class, ClassAppAdmin)


class ClassStyleAppAdmin(admin.ModelAdmin):
    list_display = ['id', 'style_example',  'pattern', 'args', 'school_period', 'del_flag']
    list_filter = ['school_period', 'del_flag']
    search_fields = ["school_period"]

admin.site.register(ClassStyle, ClassStyleAppAdmin)


class SchoolClassStyleAppAdmin(admin.ModelAdmin):
    list_display = ['id', 'school',  'primary_class_style', 'junior_class_style', 'senior_class_style', 'del_flag']
    list_filter = ['school', 'del_flag']
    search_fields = ["school"]

admin.site.register(SchoolClassStyle, SchoolClassStyleAppAdmin)


class TitleAppAdmin(admin.ModelAdmin):
    list_display = ['id', 'school',  'name', 'type', 'comments', 'teacher_amount', 'del_flag']
    list_filter = ['name', 'del_flag']
    search_fields = ["name"]

admin.site.register(Title, TitleAppAdmin)