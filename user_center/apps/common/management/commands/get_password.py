#!/usr/bin/python
# coding=utf-8

from user_center.utils.public_fun import xor_crypt_string
from user_center.apps.account.models import Account
from django.core.management.base import BaseCommand
from django.db.models import Q


class Command(BaseCommand):
    help = "decode user password"

    def add_arguments(self, parser):
        parser.add_argument('--username', nargs='+')

    def handle(self, *args, **options):
        username = options['username']
        if not username:
            print "please input username"
        else:
            username = username[0]

        account = Account.objects.filter(Q(username=username) | Q(mobile=username) | Q(code=username)).first()
        if account:
            encoded_pwd = account.encoded_pwd
            pwd = xor_crypt_string(data=encoded_pwd, decode=True)
            print pwd
        else:
            print "there's no user: %s" % username

