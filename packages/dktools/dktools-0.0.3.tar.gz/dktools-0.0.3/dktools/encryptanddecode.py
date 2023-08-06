# -*- coding: utf-8 -*- 
# @Time : 2019-11-04 09:57 
# @Author : DollarKillerx
# @Description : 加密解密
import hashlib


def md5_encoding(data: str) -> str:
    """
    md5编码
    :param data: 需编码内容
    :return: data:str
    """
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


def sha1_encoding(data: str) -> str:
    """
    使用sha1加密算法,返回加密后str
    :param data: 需编码内容
    :return: data:str
    """
    return hashlib.sha1(data.encode(encoding='UTF-8')).hexdigest()
