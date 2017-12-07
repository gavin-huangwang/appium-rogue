# -*- coding: utf-8 -*-

import pytest
import unittest
from base.action import action
from page.sqb.login_page import LoginPage
from page.sqb.home_page import HomePage
import utils.log
from utils.dataloader import load_framework_data
from utils.appiumbase import AppiumTestCase
import logging


class BasePageTest(AppiumTestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LoginPage()
        cls.home_page = HomePage()
        cls.logger = logging.getLogger(__name__)
        cls.data = load_framework_data('data')


class TestLogin(BasePageTest):
    def test_valid_login(self):
        if not self.login_page.check_if_go_to_login_page():
            self.assertTrue(False, "进入首页失败，请检查")
        action.input_text(self.login_page.text_username(), self.data.testLogin.username, True)
        action.input_text(self.login_page.text_password(), self.data.testLogin.password, True)
        action.click(self.login_page.btn_login())
        self.assertTrue(action.is_element_present(self.home_page.tv_cash_logo()))

    def test_invalid_login(self):
        if not self.login_page.check_if_go_to_login_page():
            self.assertTrue(False, "进入首页失败，请检查")
        action.input_text(self.login_page.text_username(), self.data.testInvalidLogin.username, True)
        action.input_text(self.login_page.text_password(), self.data.testInvalidLogin.password, True)
        action.click(self.login_page.btn_login())
        self.assertTrue(action.is_element_present(self.home_page.tv_cash_logo()))
