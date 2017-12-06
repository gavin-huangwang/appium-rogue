# -*- coding: utf-8 -*-

from exception.exceptions import NotFoundLocatorError
from utils.deorators import locator
from base.action import action


class HomePage:
    @locator()
    def tv_cash_logo(self):
        pass

    @locator()
    def tv_cash(self):
        pass

    @locator()
    def tv_account_book(self):
        pass

    @locator()
    def tv_report(self):
        pass

    @locator()
    def tv_home(self):
        pass

    @locator()
    def tv_service(self):
        pass

    @locator()
    def tv_personal(self):
        pass
