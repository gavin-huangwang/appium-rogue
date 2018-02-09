# -*- coding: utf-8 -*-

import pytest
import unittest
from base.action import action
from page.sqb.login_page import loginPage
from page.sqb.home_page import homePage
import utils.log
from utils.dataloader import load_framework_data
from utils.appiumbase import AppiumTestCase
from ..page_decorator import go_to_home_page
import logging


class BasePageTest(AppiumTestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger(__name__)
        cls.data = load_framework_data()


class TestLogin(BasePageTest):
    @go_to_home_page()
    def test_decorator_valid_login(self):
        """测试装饰器正常登录"""
        pass

    @go_to_home_page(username='10411113333', password='111111')
    def test_decorator_invalid_login(self):
        """测试装饰器异常登录"""
        pass
