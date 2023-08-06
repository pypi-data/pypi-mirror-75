# -*- coding: utf-8 -*-
# @Time : 2020-08-05
# @Author : DollarKillerx
# @Description : async用到的包
import threading


class Queue:
    def __init__(self):
        self.ov = False
        self.list = []
        self.lock = threading.Lock()

    def append(self, data):
        self.lock.acquire()  # lock
        if not self.ov:
            self.list.append(data)
        self.lock.release()  # unlock

    def over(self):
        self.lock.acquire()  # lock
        self.ov = True
        self.lock.release()  # unlock

    def is_over(self):
        self.lock.acquire()  # lock
        over = self.ov
        self.lock.release()  # unlock
        return over

    def get(self):
        result = None
        self.lock.acquire()  # lock
        if len(self.list) != 0:
            result = self.list[0]
            self.list = self.list[1:]
        self.lock.release()  # unlock
        return result
