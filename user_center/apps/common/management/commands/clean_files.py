#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.db import models
from user_center.apps.common import agents
from user_center.utils import file_fun
import os
import logging


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('clean over due object storage files')
        agents.clean_overdue_images()
        logger.info('clean tmp files')
        file_fun.clean_overdue_files()
