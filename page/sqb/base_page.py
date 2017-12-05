# -*- coding: utf-8 -*-

import unittest
from .login_page import LoginPage
from base.action import ElementActions


class BasePageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LoginPage()

    @staticmethod
    def check_if_go_to_login_page():
        if ElementActions().is_element_present(LoginPage.img_guide_page()):
            ElementActions().swipe_right_to_left(count=4)
            ElementActions().click(LoginPage.btn_guide_start())
        return ElementActions.is_element_present(LoginPage.text_username())
