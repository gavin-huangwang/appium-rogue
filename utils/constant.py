# -*- coding: utf-8 -*-

import os


class Framework:
    CASE_DIR = 'cases'


class App:
    SQB = 'sqb'
    CRM = "crm"


class Device:
    XIAOMI = 'xiaomi'
    HUAWEI = 'huawei'
    SAMSUNG = 'samsung'
    IPHONE6S = 'iphone6s'


class Platform:
    ANDROID = 'android'
    IOS = 'ios'


class BasePATH:
    BASE_DEVICE_CONFIG_PATH = str(
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "files/devices"))) + "/"

    BASE_LOCATOR_CONFIG_PATH = str(
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "files/locator"))) + "/"
