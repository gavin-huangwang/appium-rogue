# -*- coding: utf-8 -*-

import pytest
import unittest
from base.action import ElementActions
from page.sqb.login_page import LoginPage
import utils.log
import logging


class BasePageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LoginPage()
        cls.logger = logging.getLogger(__name__)


class TestLogin(BasePageTest):
    def test_valid_login(self):
        if not self.login_page.check_if_go_to_login_page():
            self.assertTrue(False, "进入首页失败，请检查")
        self.logger.info("sadsdasdsd")
        ElementActions().input_text(self.login_page.text_username(), '1041116666', True)
        ElementActions().input_text(self.login_page.text_password(), '123456', True)
        ElementActions().click(self.login_page.btn_login())
        ElementActions().sleep(3)
        self.assertFalse(ElementActions().is_element_present(self.login_page.btn_login()))
