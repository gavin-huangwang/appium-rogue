# -*- coding: utf-8 -*-

from utils.config import Config
from exception.exceptions import NotFoundLocatorError
from utils.deorators import locator_by
from base.action import ElementActions


class LoginPage:
    @locator_by()
    def img_guide_page(self):
        pass

    @locator_by()
    def btn_guide_start(self):
        pass

    @locator_by()
    def text_username(self):
        pass

    @locator_by()
    def test_password(self):
        pass

    @locator_by()
    def btn_login(self):
        pass

    @locator_by()
    def text_error_msg(self):
        pass

    @locator_by()
    def tv_forget_password(self):
        pass

    @locator_by()
    def tv_login_place_holder(self):
        pass

    def check_if_go_to_login_page(self):
        if ElementActions().is_element_present(self.img_guide_page()):
            ElementActions().swipe_right_to_left(count=2)
            ElementActions().click(self.btn_guide_start())
        return ElementActions().is_element_present(self.text_username())
