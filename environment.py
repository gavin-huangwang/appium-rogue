# -*- coding: utf-8 -*-

import os
from utils.constant import App, Device, Platform, BasePATH
from utils.loader import load_device_config, load_locator_config

default_config = [App.SQB, Device.XIAOMI, Platform.ANDROID]


class _Env:
    @property
    def device_config(self):
        return load_device_config(BasePATH.BASE_DEVICE_CONFIG_PATH + default_config[1] + '.xml')

    @property
    def locator_config(self):
        return load_locator_config(
            BasePATH.BASE_LOCATOR_CONFIG_PATH + default_config[0] + '_' + default_config[2] + '.xml')

    @property
    def app_name(self):
        return default_config[0]

    @property
    def device_name(self):
        return default_config[1]

    @property
    def platform_name(self):
        return default_config[2]


env = _Env()
