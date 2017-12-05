# -*- coding: utf-8 -*-

import pytest
import unittest
from base.action import ElementActions
from page.sqb.base_page import BasePageTest
from page.sqb.login_page import LoginPage


class TestLogin(BasePageTest):
    def test_valid_login(self):
        # data = self.login_page.img_guide_page()
        # data1= LoginPage.img_guide_page()
        if self.login_page.check_if_go_to_login_page():
            self.assertTrue(False, "进入首页失败，请检查")
        ElementActions().input_text(self.login_page.text_username, '1041116666', True)
        ElementActions().input_text(self.login_page.test_password, '123456', True)
        ElementActions().click(self.login_page.btn_login)
        self.assertFalse(ElementActions.is_element_present(self.login_page.btn_login))
