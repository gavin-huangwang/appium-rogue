# -*- coding: utf-8 -*-
import pytest
from configparser import ConfigParser
import os
import unittest
import utils.log
import logging
from xml.dom.minidom import parse
import xml.dom.minidom
import xml.sax
from enum import Enum

BASE_DEVICE_CONFIG_PATH = str(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "files/devices"))) + "/"
BASE_LOCATOR_CONFIG_PATH = str(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "files/locator"))) + "/"

logger = logging.getLogger(__name__)


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Config(object):
    def __init__(self, dev_file=None, locator_file=None, is_android=True):
        if dev_file.endswith(".xml"):
            self.dev_file = BASE_DEVICE_CONFIG_PATH + dev_file
        else:
            self.dev_file = BASE_DEVICE_CONFIG_PATH + dev_file + ".xml"

        if locator_file.endswith(".xml"):
            self.locator_file = BASE_LOCATOR_CONFIG_PATH + locator_file
        else:
            self.locator_file = BASE_LOCATOR_CONFIG_PATH + locator_file + ".xml"
        self._device_config = self.load_device_config()
        self._locator_config = self.load_locator_config()
        self._is_android = is_android

    @property
    def is_android(self):
        return self._is_android

    @is_android.setter
    def is_android(self, value):
        self._is_android = value

    @property
    def device_config(self):
        return self._device_config

    @device_config.setter
    def device_config(self, value):
        self._device_config = value

    @property
    def locator_config(self):
        return self._locator_config

    @locator_config.setter
    def locator_config(self, value):
        self._locator_config = value

    def load_device_config(self):
        dom_tree = xml.dom.minidom.parse(self.dev_file)
        collection = dom_tree.documentElement
        host = collection.getElementsByTagName("host")[0].childNodes[0].data
        port = collection.getElementsByTagName("port")[0].childNodes[0].data
        implicitly = collection.getElementsByTagName("implicitlyWait")[0].childNodes[0].data
        capabilities = {}
        capabilities_node = collection.getElementsByTagName("capabilities")[0].childNodes
        for temp_capability in capabilities_node:
            if temp_capability.nodeType == 1:
                capabilities[temp_capability.nodeName] = temp_capability.childNodes[0].data
        timeout = collection.getElementsByTagName("timeout")[0].childNodes[0].data
        wait = collection.getElementsByTagName("wait")[0].childNodes[0].data
        is_record = False if collection.getElementsByTagName("screenrecord")[0].childNodes[
                                 0].data.lower() == 'false' else True
        config = DevConfig(host, port, implicitly, capabilities, timeout, wait, is_record)
        return config

    def load_locator_config(self):
        locator_dict = {}
        dom_tree = xml.dom.minidom.parse(self.locator_file)
        collection = dom_tree.documentElement
        pages = collection.getElementsByTagName("page")
        for page in pages:
            page_name = page.getAttribute("pageName")
            node_list = page.childNodes
            for temp_node in node_list:
                if temp_node.nodeType == 1:
                    node_data = temp_node.childNodes[0].data
                    locator_name = page_name + "." + node_data
                    locator_dict[locator_name] = Locator(node_data, temp_node.getAttribute("location"),
                                                         int(temp_node.getAttribute("timeout")),
                                                         temp_node.getAttribute("type"))
        return locator_dict


class DevConfig(object):
    def __init__(self, host, port, implicitly, capabilities, timeout, wait, is_record):
        self._host = host
        self._port = port
        self._implicitly = implicitly
        self._capabilities = capabilities
        self._timeout = timeout
        self._wait = wait
        self._is_record = is_record

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def implicitly(self):
        return self._implicitly

    @implicitly.setter
    def implicitly(self, value):
        self._implicitly = value

    @property
    def capabilities(self):
        return self._capabilities

    @capabilities.setter
    def capabilities(self, value):
        self._capabilities = value

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    @property
    def wait(self):
        return self._wait

    @wait.setter
    def wait(self, value):
        self._wait = value

    @property
    def is_record(self):
        return self._is_record

    @is_record.setter
    def is_record(self, value):
        self._is_record = value


class ByType(Enum):
    id = "id"
    xpath = "xpath"
    text = "text"
    clazz = "class"


class Locator(object):
    def __init__(self, name, location, timeout, by_type):
        self.name = name
        self.location = location
        self.timeout = timeout
        self.by_type = by_type

        # @property
        # def name(self):
        #     return self._name
        #
        # @name.setter
        # def name(self, value):
        #     self._name = value
        #
        # @property
        # def location(self):
        #     return self._location
        #
        # @location.setter
        # def location(self, value):
        #     self._location = value
        #
        # @property
        # def timeout(self):
        #     return self._timeout
        #
        # @timeout.setter
        # def timeout(self, value):
        #     self._timeout = value
        #
        # @property
        # def by_type(self):
        #     return self._by_type
        #
        # @by_type.setter
        # def by_type(self, value):
        #     self._by_type = value
