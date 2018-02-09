# -*- coding: utf-8 -*-

from functools import wraps
from page.sqb.login_page import loginPage
from page.sqb.home_page import homePage
from exception.exceptions import PageReachedError
from base.action import action
from utils.dataloader import load_framework_data

global_data = load_framework_data()


def go_to_login_page():
    """装饰器: 进入到登录页面"""
    def wrapper(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            if not loginPage.check_if_go_to_login_page():
                raise PageReachedError("Go to login page failed")
            f = func(*args, **kwargs)
            return f

        return _wrapper

    return wrapper


def go_to_home_page(username=None, password=None):
    """装饰器: 进入到登录页面"""
    def wrapper(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            if not loginPage.check_if_go_to_login_page():
                raise PageReachedError("Go to login page failed")
            if username and password:
                _username = username
                _password = password
            else:
                _username = global_data.testLogin.username
                _password = global_data.testLogin.password
            action.input_text(loginPage.text_username(), _username, True)
            action.input_text(loginPage.text_password(), _password, True)
            action.click(loginPage.btn_login())
            if not action.is_element_present(homePage.tv_cash_logo()):
                raise PageReachedError("Go to home page failed")
            f = func(*args, **kwargs)
            return f

        return _wrapper

    return wrapper
