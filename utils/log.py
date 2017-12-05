# -*- coding: utf-8 -*-
import time


class Log:
    @staticmethod
    def e(msg, list_msg=[]):
        Log.show_list(msg, list_msg, Log.e)

    @staticmethod
    def w(msg, list_msg=[]):
        Log.show_list(msg, list_msg, Log.w)

    @staticmethod
    def i(msg, list_msg=[]):
        Log.show_list(msg, list_msg, Log.i)

    @staticmethod
    def d(msg, list_msg=[]):
        Log.show_list(msg, list_msg, Log.d)

    @staticmethod
    def show_list(msg, list_msg, f):
        temp = msg + "[ " + "\t".join(list_msg) + " ]"
        f(temp)


def get_now_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
