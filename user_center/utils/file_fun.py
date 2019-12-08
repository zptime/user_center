# -*- coding: utf-8 -*-

import os
import datetime
import uuid
import logging

from object_storage import ObjectStorage
from file_storage import FileStorage
from django.conf import settings

logger = logging.getLogger(__name__)

SUPPORTED_IMAGE_FILE_EXTENDS = ['.jpg', '.jpeg', '.png', '.bmp']
OBJECT_STORAGE_OBJ = None


def get_storage_obj(dir_name=""):
    global OBJECT_STORAGE_OBJ
    if OBJECT_STORAGE_OBJ is None:
        if settings.DATA_STORAGE_USE_S3:
            OBJECT_STORAGE_OBJ = ObjectStorage()
        else:
            OBJECT_STORAGE_OBJ = FileStorage(dir_name)
    return OBJECT_STORAGE_OBJ


def clean_overdue_files(dir_path=settings.TMP_DIR):
    try:
        now = datetime.datetime.now()
        due_date = now - datetime.timedelta(hours=settings.DATA_STORAGE_TMP_FILE_EXPIRED_HOURS)
        files_in_dir = os.listdir(dir_path)
        for file_path in files_in_dir:
            abs_file_path = os.path.join(dir_path, file_path)
            if os.path.isfile(abs_file_path):
                mtimestamp = os.path.getmtime(abs_file_path)
                mtime = datetime.datetime.fromtimestamp(mtimestamp)
                if mtime < due_date:
                    os.remove(abs_file_path)
                    logger.info("clean tmp file: %s" % abs_file_path)
    except Exception as ex:
        logging.exception("Clean files in %s with exception:%s" % (dir_path, ex))


def gen_path(prefix='', suffix='.xlsx', dir_path=settings.TMP_DIR):
    # clean_overdue_files()
    random_num = uuid.uuid4().hex
    file_name = "%s%s%s" % (prefix, random_num, suffix)
    if len(dir_path) > 0:
        file_path = os.path.join(dir_path, file_name)
        return file_path
    else:
        return file_name


def gen_s3_file_path(suffix, abs=True):
    if abs:
        return gen_path(suffix=suffix, dir_path=settings.AWS_STORAGE_BUCKET_NAME)
    else:
        return gen_path(suffix=suffix, dir_path='')


def get_image_url(path, domain=""):
    url = ""
    if not path:
        return url
    path = get_storage_obj().get_relative_url(path)
    if settings.DATA_STORAGE_USE_S3_HOST_URL and settings.DATA_STORAGE_USE_S3:
        url = 'http://' + settings.AWS_S3_HOST + ":" + str(settings.AWS_S3_PORT) + path
    else:
        url = domain + path
    return url


def get_file_name_from_url(file_url):
    file_name = file_url.split('/')[-1]
    return file_name


def get_timestr(dt, dt_format='%Y-%m-%d %H:%M:%S'):
    return dt.strftime(dt_format)
