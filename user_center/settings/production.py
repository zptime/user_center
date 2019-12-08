# -*- coding: utf-8 -*-

import os
from api import *

gettext_noop = lambda s: s

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# PROJECT_APP_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# PROJECT_ROOT = os.path.abspath(os.path.dirname(PROJECT_APP_ROOT))
# PUBLIC_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'public'))

SECRET_KEY = '-wm5q%nall)w7@!f^wc*c6&^93-k)#v=yd0(bny8pil!gj%-5a'

DEBUG = False
TEMPLATE_DEBUG = False

SITE_ID = 1
LOGIN_URL = '/'
ALLOWED_HOSTS = (
    '*'
)

ADMINS = (
    ('author', 'email'),
)
MANAGERS = ADMINS

# Application definition

ROOT_URLCONF = 'user_center.urls'
WSGI_APPLICATION = 'user_center.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cas_ng',
    'user_center.apps.account',
    'user_center.apps.api',
    'user_center.apps.common',
    'user_center.apps.parent',
    'user_center.apps.school',
    'user_center.apps.student',
    'user_center.apps.teacher',
    'user_center.apps.service',
    'user_center.apps.open',
    'user_center.apps.subject',
    'user_center.apps.weixinmp',

    # '{{ project_name}}.apps.accounts',
)

AUTH_USER_MODEL = 'account.Account'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
)

# Templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LOG_DIR = os.path.join(BASE_DIR, 'log')

TMP_DIR = os.path.join(BASE_DIR, 'tmp')

# Database

# Internationalization
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    'en', gettext_noop('English'),
)

TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# LOCALE_PATHS = os.path.join(PROJECT_ROOT, 'locale')

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfile')
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'CONN_MAX_AGE': 60,
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

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            # 'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'include_html': True,
        # },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOG_DIR, 'user_center.log'),
            # 'maxBytes': 1024 * 1024 * 5,  # 5 MB
            # 'backupCount': 10,
            'formatter': 'standard',
        },
        'open': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOG_DIR, 'open.log'),
            # 'maxBytes': 1024 * 1024 * 5,  # 5 MB
            # 'backupCount': 10,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'user_center.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 10,
            'formatter': 'standard',
        },
        'scprits_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'user_center.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 10,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        'user_center': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'user_center.apps.open': {
            'handlers': ['open', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'scripts': {
            'handlers': ['scprits_handler'],
            'level': 'INFO',
            'propagate': False
        },
    }
}

# ***************** 存储设置（data app）***************************
DATA_STORAGE_USE_S3 = True   # 是否采用S3对象存储
DATA_STORAGE_USE_S3_HOST_URL = False  # 若该参数为真，文件URL使用S3 HOST做为域名
DATA_STORAGE_INCLUDE_MODULES = []  # 备选："image", "ueditor", "upload_resumable"
DATA_STORAGE_TMP_FILE_EXPIRED_HOURS = 24 * 7    # 临时文件保留一周
# DATA_STORAGE_SAME_FILE_SAVE_ONCE = False  # 相同文件存储一次

# 文件存储使用参数
FILE_STORAGE_DIR_NAME = "media"
MEDIA_ROOT = os.path.join(BASE_DIR, FILE_STORAGE_DIR_NAME)

# S3存储（生产环境）
# AWS_ACCESS_KEY_ID = "9X99OHMSGA4ZJO0XZWIO"
# AWS_SECRET_ACCESS_KEY = "tm92ArANm1fFeYFC9lXWqgVtTuMPoMfPjRKLljkf"
# AWS_STORAGE_BUCKET_NAME = "teacher_source"

# S3存储（测试环境）
AWS_ACCESS_KEY_ID = "5NT2CU6KQE2Y34SGZTGT"
AWS_SECRET_ACCESS_KEY = "wfV2aMpXEiskrDnDPOoM1LU5ILgTJxMLdBDWBSIu"
AWS_STORAGE_BUCKET_NAME = "school_center_dev"

AWS_S3_HOST = "192.168.200.100"
AWS_S3_PORT = 8000
AWS_S3_USE_SSL = False
# *********************************************************************


PASSWORD_CRYPT_KEY = "58560e24317140589770c1af3bb2905c"
REQUEST_CONNECTION_TIMEOUT_SECONDS = 3
SESSION_COOKIE_NAME = "user_center_sessionid"
SESSION_COOKIE_AGE = 6 * 60 * 60
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

CAS_AUTH = True
CAS_VERSION = "3"
CAS_SERVER_URL = "http://test-sso.hbeducloud.com:88/sso/"
CAS_IGNORE_REFERER = True
CAS_CREATE_USER = False

APPKEY_EASY = '6ec1b164f7e047b0faad4e8c1f5e0a82'
APPSECRET_EASY = 'f198afbb3955'
TEMPLATEID_EASY = 3032443


# 更新时间点
SYS_AUTOUPDATE_TIME = {'MONTH':8, 'DAY':15}

# 检查是否更新成功，对未更新的年级再做一次且仅一次更新
SYS_AUTOUPDATE_TIME_LAST = {'MONTH':10, 'DAY':15}

# 可设置的更新和手动升级与回退的时间区间：
TIME_RANGE_DICT = {'START_TIME':(3,1),"DEADLINE":(9,30)}

app_domain = 'liukai.ngrok1.hbeducloud.com'
weixin_redirect_uri = 'http://%s/wx/access_token' % app_domain
