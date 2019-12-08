#!/usr/bin/python
# -*- coding: utf-8 -*-
import string
import urllib2
import urllib
import base64
import hmac
import hashlib
import datetime
import logging
import random
import uuid
from django.conf import settings
from constant import *
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from urlparse import urlparse
from err_code import *
import os
import json
import re
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import time


logger = logging.getLogger(__name__)


def gen_signature(key):
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    h = hmac.new(key=key, msg=timestamp, digestmod=hashlib.sha256)
    signature = base64.encodestring(h.digest()).strip()
    return timestamp, signature


# 请求第三方网站数据
def send_http_request(url, method="POST", form_data_dict='', centent_type="form"):
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)

    # build a request
    data = None
    if centent_type == "json" and form_data_dict:
        data = form_data_dict
    else:
        data = urllib.urlencode(form_data_dict)
    request = urllib2.Request(url, data=data)

    # add any other information you want
    if centent_type == "json":
        request.add_header("Content-Type", 'application/json')
    else:
        request.add_header("Content-Type", 'application/x-www-form-urlencoded')
    # overload the get method function with a small anonymous function...
    request.get_method = lambda: method

    try:
        connection = opener.open(request, timeout=settings.REQUEST_CONNECTION_TIMEOUT_SECONDS)
    except urllib2.HTTPError, e:
        # connection = e
        raise Exception(u"无法连接到网站")

    # check. Substitute with appropriate HTTP code.
    if connection.code == 200:
        data = connection.read()
        return data
    else:
        # handle the error case. connection.read() will still contain data
        # if any was returned, but it probably won't be of any use
        raise Exception(u"请求网站返回值不是200")


def try_send_http_request(domain_list, path, method="POST", form_data_dict=None):
    random.shuffle(domain_list)
    for domain in domain_list:
        url = domain + path
        try:
            return send_http_request(url, method, form_data_dict)
        except Exception as ex:
            logger.error("Connect [%s] error, Try another url", url)
            continue
    logger.error("Have try all domain of this service but not found an available one")
    raise Exception(u"无法连接到网站")


def string_is_null(s):
    if s is None or len(s.strip())==0:
        return True
    else:
        return False


def xor_crypt_string(data, key=settings.PASSWORD_CRYPT_KEY, encode=False, decode=False):
    from itertools import izip, cycle
    import base64
    if decode:
        data = base64.decodestring(data)
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))
    if encode:
        return base64.encodestring(xored).strip()
    return xored


def str_to_datetime(date_str, is_end=False):
    date_format = DATE_FORMAT_DAY
    try:
        date_list = date_str.split('-')
        if len(date_list) < 0:
            return None
        year = int(date_list[0])
        month = int(date_list[1])
        if len(date_list) == 3:
            day = int(date_list[2])
        elif len(date_list) == 2:
            day = 1
            date_format = DATE_FORMAT_MONTH
        else:
            raise Exception("只支持【年月】和【年月日】两种日期格式")

        date = datetime.datetime(year, month, day)

        if is_end:
            if date_format == DATE_FORMAT_DAY:
                date = date + datetime.timedelta(seconds=SECONDS_PER_DAY-1)
            else:
                raise Exception("只支持【年月日】作为过滤条件查询")
        return date
    except Exception as ex:
        logger.exception(ex.message)
        raise Exception("日期格式转换失败")


def datetime_to_str(date, date_format=DATE_FORMAT_DAY):
    try:
        date_str = date.strftime('%Y-%m-%d')
        if date_format == DATE_FORMAT_MONTH:
            date_str = date.strftime('%Y-%m')
        elif date_format == DATE_FORMAT_TIME:
            date_str = date.strftime('%Y-%m-%d %H:%M:%S')
        return date_str
    except Exception as ex:
        # logger.warn("datetime_to_str fail")
        return ""


def str_to_int(s):
    try:
        return int(s)
    except Exception as ex:
        # logger.warn("str_to_int fail")
        return -1


def gen_file_reponse(file_path):
    wrapper = FileWrapper(open(file_path, 'rb'))
    response = HttpResponse(wrapper, content_type='application/vnd.ms-excel')
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Encoding'] = 'utf-8'
    response['Content-Disposition'] = 'attachment;filename=%s' % os.path.basename(file_path)
    return response


# 输入参数
# rows: 每页最大行数
# page: 请求第几页从1开始计数
# sidx: 排序的列名
# sord: 升序或降序（asc:升序）

# 输出参数
# total: 总页数
# page: 当前第几页
# records: 总记录数（行数）
# items: 请求数据元素列表

def paging(item_list, rows, page, sidx="", sord="asc"):
    # 计算记录数量和页数
    ret_items = []
    records = len(item_list)
    total = records/rows
    if records % rows > 0:
        total += 1
    if page > total:
        page = total

    # 排序
    if sidx:
        reverse = False
        if sord != "asc":
            reverse = True
        if item_list and sidx in item_list[0].keys():
            item_list.sort(key=lambda x: x[sidx], reverse=reverse)

    # compute start and end index
    start = (page-1)*rows
    end = start + rows
    if records > 0 and (start < 0 or end < start):
        logger.error("error start=%d, end=%d" % (start, end))
    else:
        ret_items = item_list[start:end]

    ret_val = dict(
        total=str(total),
        page=str(page),
        records=str(records),
        items=ret_items,
    )
    return ret_val


def paging_with_request(request, dictResp):
    rows = request.POST.get("rows", "")
    page = request.POST.get("page", "")
    sidx = request.POST.get("sidx", "")
    sord = request.POST.get("sord", "")
    if not rows or not page or dictResp["c"] != ERR_SUCCESS[0]:
        return dictResp
    item_list = dictResp["d"]
    dictResp["d"] = paging(item_list, int(rows), int(page), sidx, sord)
    return dictResp


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)


class RoundTripEncoder(json.JSONEncoder):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return {
                "_type": "datetime",
                "value": obj.strftime("%s %s" % (
                    self.DATE_FORMAT, self.TIME_FORMAT
                ))
            }
        return super(RoundTripEncoder, self).default(obj)


class RoundTripDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if '_type' not in obj:
            return obj
        type = obj['_type']
        if type == 'datetime':
            return datetime.datetime.strptime(obj['value'], '%Y-%m-%d %H:%M:%S')
            # return parser.parse(obj['value'])
        return obj

# 转换是否或者bool值对应的0,1：
def range_yes_no(arg):
    if isinstance(arg, (str, unicode)):
        if arg.isdigit():
            return arg
        else:
            if arg in BOOL_CHOICE:
                return BOOL_CHOICE[arg]
            else:
                raise Exception(u"未知的选项")


def get_domain_name(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain


def convert_id_to_code(i):
    code = "%06d" % i
    return code


def convert_list_to_dict(src_list, key_name):
    ret_dict = {}
    for item in src_list:
        key = item.pop(key_name)
        if key not in ret_dict.keys():
            ret_dict[key] = []
        ret_dict[key].append(item)
    return ret_dict


def trans_to_CH(num):
    base = 10
    super_num = num/base
    lower_num = num%base
    super_num_str = ''
    lower_num_str = ''
    unit = ''
    if super_num > 1:
        super_num_str = NUM_CHINESE_SIMPLE[super_num-1]
        unit = NUM_CHINESE_SIMPLE[-1]
    elif 1 == super_num:
        unit = NUM_CHINESE_SIMPLE[-1]

    if lower_num - 1 >= 0:
        lower_num_str = NUM_CHINESE_SIMPLE[lower_num-1]
    else:
        lower_num_str = ''
    return super_num_str+unit+lower_num_str


def get_grade_name(grade_data, grade_num):
    if not grade_data:
        raise Exception(u"年级信息未设置")
    else:
        found = FLAG_NO
        if grade_num:
            for item in grade_data:
                if grade_num == item[0]:
                    found = FLAG_YES
                    return item[1]
            if not found:
                raise Exception(u"grade No:%d 没有对应年级" % grade_num)


def convert_list_to_dict(src_list, key_name):
    ret_dict = {}
    for item in src_list:
        key = item.pop(key_name)
        if key not in ret_dict.keys():
            ret_dict[key] = []
        ret_dict[key].append(item)
    return ret_dict


def len_of_value(value):
    if value is None:
        return 0
    elif isinstance(value, unicode):
        try:
            value = str(value)
            return len(value)
        except Exception:
            return len(value) * 2
    elif isinstance(value, str):
        return len(value)
    else:
        return len(str(value))


def reset_excel_column_with(ws):
    for column_cells in ws.columns:
        length = 5  # 最小宽度
        row_count = 0
        for cell in column_cells:
            # 只计算前5行
            row_count += 1
            if row_count > 5:
                break
            new_length = len_of_value(cell.value) + 1
            if new_length > length:
                length = new_length
        ws.column_dimensions[column_cells[0].column].width = length


def gen_unique_name():
    s = str(uuid.uuid1())
    s = s.replace("-", "")
    s = s[:30]
    return s


def clean_string(s):
    # 去掉字符串中间和两边的空格
    if not s:
        return s
    x = s.split()
    y = ''.join(x)
    return y


def check_idcard(id_number):
    area_dict = {11: "北京", 12: "天津", 13: "河北", 14: "山西", 15: "内蒙古", 21: "辽宁", 22: "吉林", 23: "黑龙江", 31: "上海", 32: "江苏",
                 33: "浙江", 34: "安徽", 35: "福建", 36: "江西", 37: "山东", 41: "河南", 42: "湖北", 43: "湖南", 44: "广东", 45: "广西",
                 46: "海南", 50: "重庆", 51: "四川", 52: "贵州", 53: "云南", 54: "西藏", 61: "陕西", 62: "甘肃", 63: "青海", 64: "宁夏", 65: "新疆",
                 71: "台湾", 81: "香港", 82: "澳门", 91: "外国"}
    id_code_list = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_code_list = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]
    if len(id_number) != 18:
        return False, "Length error"
    if not re.match(r"^\d{17}(\d|X|x)$", id_number):
        return False, "Format error"
    if int(id_number[0:2]) not in area_dict:
        return False, "Area code error"
    try:
        datetime.date(int(id_number[6:10]), int(id_number[10:12]), int(id_number[12:14]))
    except ValueError as ve:
        return False, "Datetime error: {0}".format(ve)
    # if check_code_list[sum([a * b for a, b in zip(id_code_list, [int(a) for a in id_number[0:-1]])]) % 11] != id_number.upper()[-1]:
    #     return False, "Check code error"
    return True, area_dict[int(id_number[0:2])].decode("utf-8")


slash_replace_str = ("/", "%2F")  # 替换url中的/
question_replace_str = ("?", "%3F")  # 替换url中的?
equal_replace_str = ("=", "%3D")  # 替换url中的=
and_replace_str = ("&", "%26")  # 替换url中的&
url_replace_list = (slash_replace_str, question_replace_str, equal_replace_str, and_replace_str)


def convert_from_url_path(s):
    # print s
    for url_replace in url_replace_list:
        s = s.replace(url_replace[0], url_replace[1])
    # print s
    # if s.isalnum():
    #     return s
    # else:
    #     return None
    return s


def convert_to_url_path(s):
    for url_replace in url_replace_list:
        s = s.replace(url_replace[1], url_replace[0])
    return s


def get_timestamp():
    curtime = time.time()
    timestamp = int(curtime)
    return timestamp


def get_randstr(length=16):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


class AES_Obj():
    def __init__(self):
        self.key = 'D8fc69MF2x45GpC7'
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        length = 16
        count = len(text)
        if (count % length != 0):
            add = length - (count % length)
        else:
            add = 0
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')


def wxtoken_compose(account_id):
    return AES_Obj().encrypt('%s,%s' % (account_id, str(int(time.time()))))


def wxtoken_decompose(wxtoken):
    try:
        token_decode = AES_Obj().decrypt(wxtoken).split(',')
        account_id = int(token_decode[0])
        timestamp = int(token_decode[1])
        timestamp_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(timestamp)))
        return account_id, timestamp, timestamp_str
    except Exception as e:
        raise Exception(u'微信登录token非法')



