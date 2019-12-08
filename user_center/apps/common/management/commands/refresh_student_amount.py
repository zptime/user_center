#!/usr/bin/python
# -*- coding=utf-8 -*-

from user_center.apps.student.agents import *
from django.core.management.base import BaseCommand, CommandError

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        school_list = School.objects.all()
        for school in school_list:
            logger.info('refresh student ammount school_id=%d' % school.id)
            refresh_student_amount(school.id)