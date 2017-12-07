# -*- coding: utf-8 -*-

import functools
import os
from utils.constant import BasePATH

try:
    import simplejson as json
except (ImportError, SyntaxError):
    import json
from exception.exceptions import NotFoundFileError


def run_once(func):
    cached = {}

    @functools.wraps(func)
    def wrapper(fn=None):
        if fn in cached:
            return cached[fn]
        ret = func(fn)
        cached[fn] = ret
        return ret

    return wrapper


@run_once
def load_framework_data(file_name=None):
    data = {}
    fn = 'data.json'
    if file_name is not None:
        fn = file_name + '.json'
    fp = os.path.join(BasePATH.BASE_DATA_FILE_PATH, fn)
    if os.path.isfile(fp):
        with open(fp, 'r') as f:
            temp_data = json.load(f, encoding="utf-8")
            data.update(temp_data)
    else:
        raise NotFoundFileError("NotFoundFileError occurs: File -> {} not found".format(fp))
    return Bunch(data)


class Bunch(dict):
    def __getattr__(self, item):
        try:
            object.__getattribute__(self, item)
        except AttributeError:
            try:
                value = super(Bunch, self).__getitem__(item)
            except KeyError:
                raise AttributeError('attribute named %s not found' % item)
            else:
                if isinstance(value, dict):
                    return Bunch(value)
                return value

    def __setattr__(self, key, value):
        super(Bunch, self).__setitem__(key, value)
