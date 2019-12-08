#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.contrib import admin
from models import *


class ServiceAppAdmin(admin.ModelAdmin):
    list_display = ['id',  'code', 'name', 'intranet_url', 'internet_url', 'del_flag']
    list_filter = ['name', 'del_flag']
    search_fields = ["code", "name"]

admin.site.register(Service, ServiceAppAdmin)


class SubnetAdmin(admin.ModelAdmin):
    list_display = ['id',  'cidr', 'comments', 'del_flag']
    list_filter = ['del_flag']
    search_fields = ["cidr"]

admin.site.register(Subnet, SubnetAdmin)


class RoleAppAdmin(admin.ModelAdmin):
    list_display = ['id',  'code', 'name', 'service', 'del_flag']
    list_filter = ['name', 'del_flag']
    search_fields = ["code", "name", "service__name"]

admin.site.register(Role, RoleAppAdmin)


class UserRoleAppAdmin(admin.ModelAdmin):
    list_display = ['id', 'school', 'role', 'user',  'del_flag']
    list_filter = ['del_flag']
    search_fields = ["school__name_full", "user__full_name", "role__name"]

admin.site.register(UserRole, UserRoleAppAdmin)


class SchoolServiceAppAdmin(admin.ModelAdmin):
    list_display = ['id',  'service', 'school',  'del_flag']
    list_filter = ['del_flag']
    search_fields = ["service__name", "school__name_full"]

admin.site.register(SchoolService, SchoolServiceAppAdmin)


class ParameterAppAdmin(admin.ModelAdmin):
    list_display = ['id',  'name', 'default_value', 'comments', 'del_flag']
    list_filter = ['del_flag']
    search_fields = ["service__name"]

admin.site.register(Parameter, ParameterAppAdmin)


class SchoolParameterAppAdmin(admin.ModelAdmin):
    list_display = ['id',  'parameter', 'school', 'value', 'del_flag']
    list_filter = ['del_flag']
    search_fields = ["school"]

admin.site.register(SchoolParameter, SchoolParameterAppAdmin)