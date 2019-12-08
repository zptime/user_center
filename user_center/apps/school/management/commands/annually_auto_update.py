#!/usr/bin/python
# coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from user_center.apps.school.school_agents import *
from user_center.apps.school.models import  *


class Command(BaseCommand):
    help = "annually auto-update the classes in all schools"

    def handle(self, *args, **options):
        school_list = School.objects.filter(del_flag=FLAG_NO)
        for school_obj in school_list:
            auto_upgrade_school_term(school_obj.id)
