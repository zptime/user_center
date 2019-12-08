#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.apps import AppConfig
# import school_agents


class MyAppConfig(AppConfig):
    name = 'user_center.apps.school'
    verbose_name = u"学校管理"
    
    # def ready(self):
    #     school_agents.init_school_db()
