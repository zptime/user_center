#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.contrib import admin
from models import *


class TeacherAppAdmin(admin.ModelAdmin):
    list_display = ['id',  'school', 'account', 'full_name', 'school_code', 'id_card', 'is_in', 'is_available', 'del_flag']
    list_filter = ['account', 'school_code', 'del_flag']
    search_fields = ["school__name_full", "full_name", "account__username", "school_code"]

admin.site.register(Teacher, TeacherAppAdmin)


class TeacherClassAppAdmin(admin.ModelAdmin):
    list_display = ['id',  'teacher', 'cls', 'is_master', 'del_flag']
    list_filter = ['teacher', 'cls', 'del_flag']
    search_fields = ["teacher", "cls"]

admin.site.register(TeacherClass, TeacherClassAppAdmin)


class TeacherSubjectAppAdmin(admin.ModelAdmin):
    list_display = ['id',  'teacher', 'subject', 'is_current', 'del_flag']
    list_filter = ['teacher', 'subject', 'del_flag']
    search_fields = ["teacher", "subject"]

admin.site.register(TeacherSubject, TeacherSubjectAppAdmin)


class TeacherTextbookAppAdmin(admin.ModelAdmin):
    list_display = ['id',  'teacher', 'textbook', 'is_current', 'del_flag']
    list_filter = ['teacher', 'textbook', 'del_flag']
    search_fields = ["teacher", "subject"]

admin.site.register(TeacherTextbook, TeacherTextbookAppAdmin)