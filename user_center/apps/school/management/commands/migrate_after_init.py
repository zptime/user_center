#!/usr/bin/python
# coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from user_center.apps.school.school_agents import *
from user_center.apps.school.class_agents import *
from user_center.apps.school.title_agents import *
from user_center.apps.teacher.agents import *
from user_center.apps.student.agents import *
from user_center.apps.school.models import *
from user_center.apps.teacher.models import *
import time

class Command(BaseCommand):

    def handle(self, *args, **options):
        school_list = School.objects.filter(del_flag=FLAG_NO)
        for school_obj in school_list:
            print school_obj.name_full
            init_school(school_obj)
            init_class(school_obj)
            init_title(school_obj.id)
            init_teacher_title(school_obj.id)
            init_teacher_master_class(school_obj.id)
            refresh_teacher_amount(school_obj.id)
            refresh_student_amount(school_obj.id)
            time.sleep(2)
