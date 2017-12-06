# -*- coding: utf-8 -*-

import pytest
import unittest
from base.action import action
from page.sqb.login_page import LoginPage
from page.sqb.home_page import HomePage
import utils.log
import logging
import threading


class BasePageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LoginPage()
        cls.home_page = HomePage()
        cls.logger = logging.getLogger(__name__)


class TestLogin(BasePageTest):
    def test_valid_login(self):
        if not self.login_page.check_if_go_to_login_page():
            self.assertTrue(False, "进入首页失败，请检查")
        action.input_text(self.login_page.text_username(), '10411116666', True)
        action.input_text(self.login_page.text_password(), '123456', True)
        action.click(self.login_page.btn_login())
        self.assertTrue(action.is_element_present(self.home_page.tv_cash_logo()))

    def test_invalid_login(self):
        if not self.login_page.check_if_go_to_login_page():
            self.assertTrue(False, "进入首页失败，请检查")
        action.input_text(self.login_page.text_username(), '10411112345', True)
        action.input_text(self.login_page.text_password(), '123456', True)
        action.click(self.login_page.btn_login())
        self.assertTrue(action.is_element_present(self.home_page.tv_cash_logo()))
