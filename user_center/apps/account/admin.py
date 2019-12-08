#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.contrib import admin
from models import *


class AccountAppAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', "mobile",  'type', 'school', 'del_flag']
    exclude = ('status', 'num', 'encoded_pwd','last_login', 'create_time', 'update_time')
    search_fields = ["username", "school__name_full", "mobile"]
    actions = ['qry_password']

    def save_model(self, request, obj, form, change):
        if 'pbkdf2_sha256' not in obj.password:
            obj.encoded_pwd = xor_crypt_string(data=obj.password, encode=True)
            obj.set_password(obj.password)
        obj.num = obj.username
        obj.save()

    def qry_password(self, request, queryset):
        if queryset.count() < 1:
            self.message_user(request, u'请选择一条或多条记录查询密码')

        result = ''
        for eachrow in queryset:
            result = result + u'%s:%s\n\n' % (eachrow.username, xor_crypt_string(data=eachrow.encoded_pwd, decode=True))

        self.message_user(request, result)
    qry_password.short_description = u'查询用户密码'

admin.site.register(Account, AccountAppAdmin)