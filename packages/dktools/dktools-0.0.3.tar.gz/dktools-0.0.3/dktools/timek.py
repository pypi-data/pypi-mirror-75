# -*- coding: utf-8 -*- 
# @Time : 2019-11-04 10:46 
# @Author : DollarKillerx
# @Description : time

import time


def get_original() -> object:
    """
    返回原始时间
    :return: 原始时间
    """
    return time.time()


def get_time() -> int:
    """
    返回毫米时间戳
    :return: 毫秒时间戳
    """
    t = time.time()
    return int(round(t * 1000))


def get_microsecond() -> int:
    """
    返回纳秒时间戳
    :return: 纳秒时间戳
    """
    t = time.time()
    return int(round(t * 1000000))


def get_time_string() -> str:
    """
    返回格式化时间
    :param
    :return: 格式化时间
    """

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(get_original()))


def get_time_tostring(t: int) -> str:
    """
        返回格式化时间
        :param time: 秒级时间戳
        :return: 格式化时间
        """

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

# if __name__ == '__main__':
# print(get_time())
# print(get_microsecond())
# ta_dt = time.strptime("2018-09-06 21:54:46", '%Y-%m-%d %H:%M:%S')  # 日期时间转结构体
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))))
# print(get_original())
# time = get_original()
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(get_original())))
# print(get_time_string(get_original()))
# print(get_time_string(1514774430))
# t = time.time()
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(t))))
# print(get_time_string())
# print(get_time_tostring(get_original()))
