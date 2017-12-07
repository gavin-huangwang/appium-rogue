# -*- coding: utf-8 -*-

import argparse
import os
import sys
from os.path import isdir, join
import pytest
from utils.constant import Platform
import environment
from utils.constant import Framework


def list_dirs(path):
    """列出path目录下的文件夹"""
    ret = []
    for ele in os.listdir(path):
        p = ele if path == "." else join(path, ele)
        if isdir(p) and not ele.startswith(".") and not ele.startswith("_"):
            ret.append(p)
    return ret


def ignores(parent, *sub):
    """根据要执行的sub目录，反向生成要忽略的目录"""
    dirs = list_dirs(parent)
    for path in sub:
        current = path.pop(0)
        current = current if parent == "." else join(parent, current)
        dirs.remove(current)
        if path:  # 进入子目录递归
            yield from ignores(current, path)
    else:
        yield dirs


def dpath_to_lists(dpath):
    """将目录字符串转换成list对象"""
    return list(map(lambda s: s.strip().strip("/").split("/"), dpath.split(",")))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", dest="app_name", action="store", default="sqb", type=str, help="app名称，比如sqb")
    parser.add_argument("--dev", dest="dev_name", action="store", default="xiaomi", type=str, help="设备名称，例如xiaomi")
    parser.add_argument("--android", dest="is_android", action="store_true", default=True, help="是否是android")
    parser.add_argument("--no_android", dest="is_android", action="store_false", default=False, help="是否是iOS")
    parser.add_argument("--suites", dest="suites", action="store", type=str,
                        help="用于指定执行哪些目录下的用例（可包含子目录），多个目录用`,`分割, eg: --suites app,infrastructure")
    parser.set_defaults(is_android=True)

    args, other_args = parser.parse_known_args()
    # config = Config(args.dev_file, args.locator_file, args.is_android)

    if args.app_name != environment.default_config[0]:
        environment.default_config[0] = args.app_name

    if args.dev_name != environment.default_config[1]:
        environment.default_config[1] = args.dev_file

    platform = Platform.ANDROID if args.is_android else Platform.IOS
    if platform != environment.default_config[2]:
        environment.default_config[2] = Platform.IOS

    sys.argv = [sys.argv[0]]
    sys.argv.extend(other_args)

    if args.suites:
        data = dpath_to_lists(args.suites)
        for ds in ignores(Framework.CASE_DIR, *dpath_to_lists(args.suites)):
            for d in ds:
                opt = "--ignore={}".format(d)
                sys.argv.append(opt)

    pytest.main()
