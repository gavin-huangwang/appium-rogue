# -*- coding: utf-8 -*-

from utils.config import Config
from functools import wraps
from exception.exceptions import NotFoundLocatorError


def locator_by(name=None):
    def wrapper(func):
        @wraps(func)
        def _wrapper():
            locator_config = Config().locator_config
            dict_key = func.__qualname__
            clazz_name = dict_key.split('.')[0]
            method_name = dict_key.split('.')[1]
            if name is not None:
                method_name = name
            dict_key = clazz_name + '.' + method_name
            if dict_key in locator_config:
                locator_dict = locator_config.get(dict_key)
                return locator_dict
            else:
                raise NotFoundLocatorError("exception occurs: {} not found in {}".format(method_name, clazz_name))

        return _wrapper

    return wrapper
