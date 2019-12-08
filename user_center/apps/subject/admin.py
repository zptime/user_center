#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.contrib import admin
from models import *

class SubjectAppAdmin(admin.ModelAdmin):
    list_display = ['name',  'is_active', 'editor', 'del_flag']
    list_filter = ['name', 'is_active', 'del_flag']
    search_fields = ['name']

admin.site.register(Subject, SubjectAppAdmin)


class TextbookAppAdmin(admin.ModelAdmin):
    list_display = ['name',  'is_active', 'editor', 'subject', 'grade_num', 'chapter_count', 'del_flag']
    list_filter = ['name', 'is_active', 'del_flag']
    search_fields = ['name', 'subject__name']

admin.site.register(Textbook, TextbookAppAdmin)


class ChapterAppAdmin(admin.ModelAdmin):
    list_display = ['name',  'textbook', 'parent', 'open', 'is_parent', 'del_flag']
    list_filter = ['name', 'del_flag']
    search_fields = ['name', 'textbook__name']

admin.site.register(Chapter, ChapterAppAdmin)


class SchoolSubjectAppAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject',  'school', 'del_flag']
    list_filter = ['id', 'del_flag']

admin.site.register(SchoolSubject, SchoolSubjectAppAdmin)


class SchoolTextbookAppAdmin(admin.ModelAdmin):
    list_display = ['id', 'textbook',  'school', 'del_flag']
    list_filter = ['id', 'del_flag']

admin.site.register(SchoolTextbook, SchoolTextbookAppAdmin)