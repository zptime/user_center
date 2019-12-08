# -*- coding=utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from user_center.utils.public_fun import xor_crypt_string
from user_center.apps.school.models import School
from user_center.apps.common.models import Image


class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if (not username) or (not password):
            raise ValueError('UserManager create user param error')

        user = self.model(
            username=username,
        )
        user.encoded_pwd = xor_crypt_string(data=password, encode=True)
        user.set_password(password)
        if kwargs:
            if kwargs.get('email', ""):
                user.email = kwargs['email']
            elif kwargs.get('full_name', ""):
                user.full_name = kwargs['full_name']
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        if not password:
            password = "Fh12#$"
        account = self.create_user(username=username, password=password)
        account.is_superuser = True
        account.is_admin = True
        account.save(using=self._db)
        return account


class Account(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True, db_index=True, verbose_name=u'账号')
    code = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u'学籍号')  # 学生
    mobile = models.CharField(default="", max_length=30, blank=True, null=True, verbose_name=u'手机号')  # 学生、教师、家长
    parent_mobile = models.CharField(default="", max_length=30, blank=True, null=True, verbose_name=u'家长手机号') # 学生

    type = models.IntegerField(default=0, choices=((0, u"未设置"), (1, u"学生"), (2, u"教师"), (4, u"家长")), verbose_name=u'用户类型')
    school = models.ForeignKey(School, blank=True, null=True, verbose_name=u'当前所在学校', on_delete=models.PROTECT)
    role = models.CharField(default="", max_length=254, blank=True, verbose_name=u'角色')

    is_admin = models.BooleanField(default=False, verbose_name=u'是否后台管理员')
    is_active = models.BooleanField(default=True, verbose_name=u'有效')
    encoded_pwd = models.CharField(max_length=128, verbose_name=u'加密密码')

    need_change_pwd = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否需要修改密码')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    # 暂时不使用
    id_card = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u'身份证号')
    tmp_code = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u'学籍号（L）/员工号')
    full_name = models.CharField(max_length=30, blank=True, verbose_name=u'姓名')
    sex = models.CharField(default=u"未设置", blank=True, max_length=30, choices=((u"未设置", u"未设置"), (u"男", u"男"),
                                                                   (u"女", u"女")), verbose_name=u'性别')
    email = models.CharField(default="", max_length=254, blank=True,  verbose_name=u'邮箱')
    is_mobile_login = models.IntegerField(default=0, blank=True, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否允许手机登录')
    is_email_login = models.IntegerField(default=0, blank=True, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否允许邮箱登陆')
    address = models.CharField(default="", blank=True, max_length=128, verbose_name=u'地址')
    company = models.CharField(default="", blank=True,  max_length=30, verbose_name=u'单位')
    image = models.ForeignKey(Image, blank=True, null=True, verbose_name=u'图片', on_delete=models.PROTECT)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.full_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.full_name

    class Meta:
        db_table = "account"
        verbose_name_plural = u"用户表"
        verbose_name = u"用户表"

    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin