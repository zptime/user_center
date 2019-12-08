#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.apps import AppConfig
# import agents


class MyAppConfig(AppConfig):
    name = 'user_center.apps.service'
    verbose_name = u"服务管理"
    
    # def ready(self):
    #     agents.init_service()
