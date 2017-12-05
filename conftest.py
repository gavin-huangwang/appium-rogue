# -*- coding: utf-8 -*-

import pytest
from appium import webdriver
from base.action import ElementActions
from utils.config import Config


@pytest.fixture(autouse=True)
def init_drive():
    dev_conf = Config().device_config
    req_url = "http://%s:%s/wd/hub" % (dev_conf.host, dev_conf.port)
    driver = webdriver.Remote(req_url, dev_conf.capabilities)
    yield ElementActions(driver).reset(driver)
    driver.quit()
