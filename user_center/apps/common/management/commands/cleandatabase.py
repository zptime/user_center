#!/usr/bin/python
# coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from user_center.apps.open.agents import class_name_to_class
from user_center.utils.constant import *
import datetime


class Command(BaseCommand):
    help = "this is a command customized for cleaning the database with a period of time(default is 7 days)!"
    default_time_period = 7
    DELETE_MODEL_CLS_LIST = ["VerifyCode", "Subnet", "Grade", "UpdateManagement", "UserRole", "Role",
                             "ParentStudent", "Parent", "Student", "Teacher", "Account", "SchoolService",
                             "Class", "ClassStyle", "School", "Service", "Image"]

    def add_arguments(self, parser):
        parser.add_argument('--overdue_day', nargs='+', type=int)

    def handle(self, *args, **options):
        time_period_list = options['overdue_day']
        if time_period_list:
            time_period = time_period_list[0]
        else:
            time_period = self.default_time_period

        now = datetime.datetime.now()
        out_date = now - datetime.timedelta(days=time_period)

        for model_cls_name in self.DELETE_MODEL_CLS_LIST:
            model_cls = class_name_to_class(model_cls_name)
            model_cls.objects.filter(update_time__lte=out_date, del_flag=YES).delete()




