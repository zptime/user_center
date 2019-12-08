# -*- coding: utf-8 -*-
from user_center.settings.production import *

# TMP_PATH = os.path.abspath(os.path.join(PROJECT_ROOT, 'tmp'))

DEBUG = TEMPLATE_DEBUG = True
SECRET = '42'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'user_center',
        'TEST': {
            'NAME': 'user_center'
        },

        'USER': 'root',
        'PASSWORD': '111111',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# ***************** 存储设置（data app）***************************
DATA_STORAGE_USE_S3 = True   # 是否采用S3对象存储
DATA_STORAGE_USE_S3_HOST_URL = True  # 若该参数为真，文件URL使用S3 HOST做为域名
# *********************************************************************


