#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.contrib import admin
from models import *


class StudentAppAdmin(admin.ModelAdmin):
    list_display = ['id',  'school', 'account', 'full_name', 'cls', 'is_in', 'is_available', 'del_flag']
    list_filter = ['account', 'del_flag']
    search_fields = ["school__name_full", "full_name", "account__username"]

admin.site.register(Student, StudentAppAdmin)
