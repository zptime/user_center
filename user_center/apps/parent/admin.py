#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.contrib import admin
from models import *


class ParentAppAdmin(admin.ModelAdmin):
    list_display = ['id', 'school', 'account', 'full_name', 'sex', 'del_flag']
    list_filter = ['id', 'del_flag']
    search_fields = ["school__name_full", "full_name"]
    raw_id_fields = ("account",)

admin.site.register(Parent, ParentAppAdmin)


class ParentStudentAppAdmin(admin.ModelAdmin):
    list_display = ['id', 'parent', 'student', 'relation', 'del_flag']
    list_filter = ['id', 'del_flag']

admin.site.register(ParentStudent, ParentStudentAppAdmin)
