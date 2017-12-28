# -*- coding: utf-8 -*-

import xml.dom.minidom
import xml.sax
import functools
from enum import Enum


def run_once(func):
    cached = {}

    @functools.wraps(func)
    def wrapper(fp):
        if fp in cached:
            return cached[fp]
        ret = func(fp)
        cached[fp] = ret
        return ret

    return wrapper


@run_once
def load_device_config(dev_file_path):
    dom_tree = xml.dom.minidom.parse(dev_file_path)
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


@run_once
def load_locator_config(locator_file_path):
    locator_dict = {}
    dom_tree = xml.dom.minidom.parse(locator_file_path)
    collection = dom_tree.documentElement
    pages = collection.getElementsByTagName("page")
    for page in pages:
        page_name = page.getAttribute("pageName")
        node_list = page.childNodes
        for temp_node in node_list:
            if temp_node.nodeType == 1:
                node_data = temp_node.childNodes[0].data
                locator_name = page_name + "." + node_data.replace("\n", "").replace(" \r\n", "").strip()
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


class Locator(object):
    def __init__(self, name, location, timeout, by_type):
        self.name = name
        self.location = location
        self.timeout = timeout
        self.by_type = by_type

    def __str__(self):
        return '[Locator: %s, %s, %s, %s]' % (self.name, self.location, self.timeout, self.by_type)


class ByType(Enum):
    id = "id"
    xpath = "xpath"
    text = "text"
    clazz = "class"
