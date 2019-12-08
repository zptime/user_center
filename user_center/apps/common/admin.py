#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.contrib import admin
from models import *


class ImageAppAdmin(admin.ModelAdmin):
    list_display = ['id',  'name', 'url', 'size', 'del_flag']
    list_filter = ['name', 'del_flag']

admin.site.register(Image, ImageAppAdmin)
