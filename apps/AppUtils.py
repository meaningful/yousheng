#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---------------------------------------------
    File  Name : AppUtils
    Author : agony
    Date : 2018/8/19
    Description: 工具类
---------------------------------------------
"""
import hashlib
from apps.BaseModels.BaseModelsORM.BaseORMViews import UserDBUtils
from time import strftime, localtime
from decimal import Decimal
from dateutil.relativedelta import *
from dateutil.parser import *
import time

_year = strftime("%Y", localtime())
_mon = strftime("%m", localtime())
_day = strftime("%d", localtime())
_hour = strftime("%H", localtime())
_min = strftime("%M", localtime())
_sec = strftime("%S", localtime())


class EncodeUtils(object):
    # Hash 加密字符串
    @classmethod
    def encode(cls, str_to_encode):
        hash_sha256 = hashlib.sha256()
        hash_sha256.update(bytes(str_to_encode, encoding='utf-8'))
        hash_result = hash_sha256.hexdigest()
        return hash_result


# 登陆工具类
class LoginUtils(object):
    @classmethod
    def doLogin(cls, name, password):
        user = UserDBUtils.isUserExist(name, EncodeUtils.encode(password))
        if user:
            return user
        else:
            return None


# 日期时间工具类
class DateUtils(object):

    @classmethod
    def get_current_time(cls):
        return _year + _mon + _day + _hour + _min + _sec

    @classmethod
    def get_current_Y(cls):
        localtime = time.asctime(time.localtime(time.time()))
        now = parse(localtime)
        return str(now)[0:5]

    @classmethod
    def get_current_YM(cls):
        localtime = time.asctime(time.localtime(time.time()))
        now = parse(localtime)
        return str(now)[0:7]

    @classmethod
    def get_last_YM(cls):
        # 当前时间
        localtime = time.asctime(time.localtime(time.time()))
        now = parse(localtime)
        # 上个月的时间
        lastDate = now + relativedelta(months=-1)
        return str(lastDate)[0:7]


    @classmethod
    def getIntervalMonthDate(cls, intervalMonth):
        # 当前时间
        localtime = time.asctime(time.localtime(time.time()))
        now = parse(localtime)
        # 计算间隔日期
        intervalDate = now + relativedelta(months=intervalMonth)
        return str(intervalDate)[0:10]


# 数据计算工具类
class DataUtils(object):

    @classmethod
    def strNumToDeciaml(cls, strNum):
        return Decimal(strNum)

    # 数量  	count
    # 单价	unitPrice
    @classmethod
    def countSaleListPrice(cls, count, unitPrice):
        total = Decimal(count) * Decimal(unitPrice)
        return total.quantize(Decimal('0.00'))

    @classmethod
    def switchToPercent(cls, ratio):
        return ratio.quantize(Decimal('0.0000'))
