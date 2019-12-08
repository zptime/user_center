#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'user_center.apps.account'
    verbose_name = u"用户管理"
    
    # def ready(self):
    #     fresh_user_num_dict_cache()
