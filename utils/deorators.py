# -*- coding: utf-8 -*-

from functools import wraps

from environment import env
from exception.exceptions import NotFoundLocatorError
from environment import env


def locator(page=None, name=None):
    def wrapper(func):
        @wraps(func)
        def _wrapper(self):
            func(self)
            locator_config = env.locator_config
            dict_key = func.__qualname__
            if page is not None and name is not None:
                dict_key = page + "." + name
            if dict_key in locator_config:
                locator_dict = locator_config.get(dict_key)
                return locator_dict
            else:
                raise NotFoundLocatorError("NotFoundLocatorError occurs: locator -> {} not found".format(dict_key))

        return _wrapper

    return wrapper
