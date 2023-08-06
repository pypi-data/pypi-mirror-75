# -*- coding: utf-8 -*- 
# @Time : 2019-11-04 10:27 
# @Author : DollarKillerx
# @Description : 随机

import uuid
import random
import timek
import encryptanddecode


def get_uuid() -> str:
    """
    返回uuid
    :return:uuid
    """
    return str(uuid.uuid4())


def get_simple_uuid():
    """
    返回简单uuid (去-)
    :return: 返回uuid (去-)
    """
    return get_uuid().replace('-', '')


def super_random() -> str:
    """
    返回超级随机数
    :return: 随机数
    """
    t = timek.timek()
    return encryptanddecode.sha1_encoding(str(random.randint(1, 10000)) + str(t))
