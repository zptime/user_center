from user_center.apps.account.models import Account
from django.core.management.base import BaseCommand, CommandError
from django.db import models
from user_center.apps.common import agents
from user_center.utils import file_fun
import os
import logging


logger = logging.getLogger(__name__)
class Command(BaseCommand):
    def handle(self, *args, **options):
        account_list = Account.objects.all()
        for account in account_list:
            code = account.code
            if code.find(" ") >= 0:
                account.code = code.replace(" ", "")
                account.save()
                logger.info('fix src_code=%s dst_code=%s school=%d' % (code, account.code, account.school_id or 0))
            if code.find(u" ") >= 0:
                account.code = code.replace(u" ", "")
                account.save()
                logger.info('fix src_code=%s dst_code=%s school=%d' % (code, account.code, account.school_id or 0))
            if code.find("\t") >= 0:
                account.code = code.replace("\t", "")
                account.save()
                logger.info('fix src_code=%s dst_code=%s school=%d' % (code, account.code, account.school_id or 0))
        logger.info('complete')
