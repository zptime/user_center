# coding=utf-8
import json
import logging
from urlparse import urlparse, urljoin

import requests
from django.conf import settings

from user_center.apps.service.models import Service
from user_center.utils.err_code import ERR_FAIL
from user_center.utils.gen_response import response200

logger = logging.getLogger(__name__)
INTERACT_SYSTEM_NAME = 'interact'
NETAGENT_SYSTEM_NAME = 'netagent'


def get_interact_sys_address():
    if hasattr(settings, 'INTERACT_INFORMAL_DOMAIN') and settings.INTERACT_INFORMAL_DOMAIN:
        domain = settings.INTERACT_INFORMAL_DOMAIN
    else:
        this_service = Service.objects.filter(code__contains=INTERACT_SYSTEM_NAME).first()
        parsed_uri = urlparse(this_service.intranet_url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain


def get_netagent_sys_address():
    if hasattr(settings, 'NETAGENT_INFORMAL_DOMAIN') and settings.NETAGENT_INFORMAL_DOMAIN:
        domain = settings.NETAGENT_INFORMAL_DOMAIN
    else:
        this_service = Service.objects.filter(code__in=[NETAGENT_SYSTEM_NAME, ]).first()
        parsed_uri = urlparse(this_service.intranet_url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain


def get_netagent_log_address():
    if hasattr(settings, 'NETAGENT_LOG_DOMAIN') and settings.NETAGENT_LOG_DOMAIN:
        domain = settings.NETAGENT_LOG_DOMAIN
    else:
        this_service = Service.objects.filter(code__in=[NETAGENT_SYSTEM_NAME, ]).first()
        parsed_uri = urlparse(this_service.intranet_url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain


def sendsms(mobile):
    """
        发送短信
    """
    payload = {
        'pkg_name': 'applications.mail.services',
        'function_name': 'send_message',
        'parameter': json.dumps({
            'mobile': mobile,
        }, ensure_ascii=False)
    }

    try:
        logger.info('sendsms to netagent:')
        logger.info(payload)
        remote_response = _netagent_remote_call(payload)
    except Exception as e:
        logger.exception(e)
        return response200({'c': ERR_FAIL[0], 'm': ERR_FAIL[1], 'd': u'调用网络代理平台失败'})
    logger.info('netagent return response:')
    logger.info(remote_response)
    return remote_response


def get_interact_service_list(account_id):
    """
        到互动平台查询服务列表
    """
    payload = {
        'account_id': account_id,
    }

    try:
        logger.info('get_wx_service_list from interact:')
        logger.info(payload)
        remote_response = requests.post(
            urljoin(get_interact_sys_address(), '/api/mobile/service/list'),
            data=payload,
            timeout=10)
    except Exception as e:
        logger.exception(e)
        return response200({'c': ERR_FAIL[0], 'm': ERR_FAIL[1], 'd': u'调用互动平台失败'})
    logger.info('netagent return response:')
    logger.info(remote_response)
    return remote_response


def _netagent_remote_call(payload, files=None):
    if files:
        response = requests.post(
            urljoin(get_netagent_log_address(), '/api/internal/proxy'),
            data=payload,
            files=files,
            timeout=60)
    else:
        response = requests.post(
            urljoin(get_netagent_sys_address(), '/api/internal/proxy'),
            data=payload,
            timeout=10)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return json.loads(response.text)
