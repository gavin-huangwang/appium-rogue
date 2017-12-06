# -*- coding: utf-8 -*-

import pytest
from appium import webdriver

from base.action import action
from base.appiumserver import AppiumServer
from environment import env
from exception.exceptions import StartServerTimeout


@pytest.fixture(autouse=True)
def init_drive():
    dev_conf = env.device_config
    req_url = "http://%s:%s/wd/hub" % (dev_conf.host, dev_conf.port)
    driver = webdriver.Remote(req_url, dev_conf.capabilities)
    yield action.reset(driver)
    driver.quit()


@pytest.fixture(scope="module", autouse=True)
def start_appium():
    appium_server = AppiumServer(env.device_config.host, env.device_config.port, env.device_config.timeout)
    if not appium_server.start_server():
        raise StartServerTimeout("在指定时间{}秒内未能启动appium server，请手动检查！".format(env.device_config.timeout))
