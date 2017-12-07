# -*- coding: utf-8 -*-

import logging
import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from utils.constant import Platform
from environment import env
from exception.exceptions import *
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


# @singleton
class _ElementActions:
    def __init__(self):
        self.driver = ''
        self.width = ''
        self.height = ''
        self.touch_action = ''
        self.dev_config = ''
        self.implicitly_wait = ''
        self.is_android = ''

    def reset(self, driver: webdriver.Remote):
        """
        单例模式,所以当driver变动的时候,需要重置一下driver
        :param driver: 
        :return: 
        """
        self.driver = driver
        self.width = self.driver.get_window_size()['width']
        self.height = self.driver.get_window_size()['height']
        self.touch_action = TouchAction(self.driver)
        self.dev_config = env.device_config
        self.implicitly_wait = env.device_config.implicitly
        self.set_implicitly_wait(self.implicitly_wait)
        self.is_android = True if env.platform_name == Platform.ANDROID else False
        return self

    @staticmethod
    def sleep(second):
        """
        阻塞等待
        :param second: 秒 
        :return: 
        """
        return time.sleep(second)

    def back_press(self):
        """
        模拟物理返回键
        :return: 
        """
        self._send_key_event('KEYCODE_BACK')

    def set_number_by_soft_keyboard(self, nums):
        """
        模仿键盘输入数字,nums支持list
        :param nums: 输入的数字
        :return: 
        """
        list_nums = list(nums)
        for num in list_nums:
            self._send_key_event('KEYCODE_NUM', num)

    def swipe_left_to_right(self, count=1):
        """
        从左往右边滑动
        :param count: 次数，默认1次 
        :return: 
        """
        for x in range(count):
            self.sleep(1)
            self.driver.swipe(self.width * 1 / 10, self.height / 2, self.width * 9 / 10, self.height / 2, 1500)

    def swipe_right_to_left(self, count=1):
        """
        从右往左边滑动
        :param count: 次数，默认1次 
        :return: 
        """
        for x in range(count):
            self.sleep(1)
            self.driver.swipe(self.width * 9 / 10, self.height / 2, self.width / 10, self.height / 2, 1500)

    def swipe_up_to_down(self, count=1):
        """
        从上向下滑动
        :param count: 滑动次数
        :return: 
        """
        for x in range(count):
            self.sleep(1)
            self.driver.swipe(self.width / 2, self.height * 2 / 5, self.width / 2, self.height * 4 / 5, 1500)

    def swipe_down_to_up(self, count=1):
        """
        从下向上滑动
        :param count: 滑动次数
        :return: 
        """
        for x in range(count):
            self.sleep(1)
            self.driver.swipe(self.width / 2, self.height * 4 / 5, self.width / 2, self.height * 2 / 5, 1500)

    def swipe_by_coordinate(self, start_x, start_y, end_x, end_y, duration=1500):
        """
        
        :param start_x: 起点坐标X
        :param start_y: 起点坐标Y
        :param end_x: 终点坐标X
        :param end_y: 终点坐标Y
        :param duration: 间隔，默认是1500毫秒
        :return: 
        """
        self.touch_action.press(start_x, start_y).wait(duration).move_to(end_x, end_y).release().perform()

    def click(self, locator, count=1):
        """
        点击元素
        :param locator: locator 
        :param count: 点击次数
        :return: 
        """
        el = self._find_element(locator)
        if count == 1:
            el.click()
        else:
            try:
                for x in range(count):
                    self.touch_action.tap(el).perform()
            except:
                pass

    def long_press(self, locator, duration):
        """
        长按元素
        :param locator: locator
        :param duration: 点击时长(秒)
        :return: 
        """
        ele = self._find_element(locator)
        self.touch_action.long_press(ele, duration * 1000).perform()

    def get_text(self, locator):
        """获取元素text值"""
        ele = self._find_element(locator)
        if ele is None:
            return None
        return ele.get_attribute("text")

    def input_text(self, locator, value, clear_first=False):
        """
        输入文本内容
        :param locator: locator 
        :param value: 内容
        :param clear_first: 是否先清除
        :return: 
        """
        if clear_first:
            self._find_element(locator).clear()
        self._find_element(locator).send_keys(value)

    def is_text_present(self, text, is_retry=True, retry_time=5):
        """
        检查页面是否存在指定的text
        :param text: text内容
        :param is_retry: 是否重试，默认重试
        :param retry_time: 尝试时间，默认是5
        :return: 
        """
        try:
            if is_retry:
                return WebDriverWait(self.driver, retry_time).until(
                    lambda driver: self._find_text_in_page(text))
            else:
                return self._find_text_in_page(text)
        except:
            ("页面中未找到 %s 文本" % text)
            return False

    def is_element_present(self, locator, is_need_display=True):
        """
        判断元素是否可见/存在
        :param locator: locator
        :param is_need_display: 是否必须可见
        :return: 
        """
        ele = self._find_element(locator)
        if ele is None:
            return False
        else:
            return ele.is_displayed()

    def is_element_checked(self, locator):
        """
        判断元素是否勾选，比如checkbox
        :param locator: locator 
        :return: 
        """
        ele = self._find_element(locator)
        if ele is None:
            raise NotFoundElementError("未能找到元素{}".format(locator))
        return True if ele.get_attribute("checked").lower() == 'true' else True

    def is_element_selected(self, locator):
        """
        判断元素是否选中，比如选中tab栏位被选中
        :param locator: locator 
        :return: 
        """
        ele = self._find_element(locator)
        if ele is None:
            raise NotFoundElementError("未能找到元素{}".format(locator))
        return True if ele.get_attribute("selected").lower() == 'true' else True

    def check_element(self, locator):
        """勾选元素-已经做判断"""
        if not self.is_element_checked(locator):
            self.click(locator)

    def uncheck_element(self, locator):
        """反勾选元素-已经做判读"""
        if self.is_element_checked(locator):
            self.click(locator)

    def select_element(self, locator):
        """选中元素-已经做判断"""
        if not self.is_element_selected(locator):
            self.click(locator)

    def unselect_element(self, locator):
        """反选中元素-已经做判读"""
        if self.is_element_selected(locator):
            self.click(locator)

    def _find_element(self, locator):
        """
        查找元素，如果有多个只返回第一个
        :param locator: locator
        :return: 返回Element/List<Element>/None
        """
        timeout = locator.timeout
        self.set_implicitly_wait(timeout)
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: self._get_element_by_locator(driver, locator) is not None)
            self.set_implicitly_wait(self.implicitly_wait)
            return self._get_element_by_locator(self.driver, locator)
        except Exception as e:
            logger.error("未能找到 %s 元素" % locator)
            self.set_implicitly_wait(self.implicitly_wait)
            return None

    def _find_elements(self, locator):
        """
        查找多个元素
        :param locator: locator 
        :return: 返回Elements/List<Elements>/None
        """
        timeout = locator.timeout
        self.set_implicitly_wait(timeout)
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: self._get_element_by_locator(driver, locator, False).__len__() > 0)
            self.set_implicitly_wait(self.implicitly_wait)
            return self._get_element_by_locator(self.driver, locator, False)
        except Exception as e:
            logger.error("未能找到 %s 元素" % locator)
            self.set_implicitly_wait(self.implicitly_wait)
            return None

    def hide_keyboard(self):
        """
        隐藏键盘
        :return: 
        """
        self.driver.hide_keyboard()

    def set_implicitly_wait(self, implicitly_wait):
        """
        设置隐式等待时间（隐式等待和显示等待都存在时，超时时间取二者中较大的）
        :param implicitly_wait: 隐式等待时间
        :return: 
        """
        self.driver.implicitly_wait(implicitly_wait)

    @staticmethod
    def _get_element_by_locator(driver, locator, is_single=True):
        """
        通过locator获取元素
        :param driver: driver
        :param locator: locator
        :param is_single: 是否只返回一个元素或者是list
        :return: 
        """
        location = locator.location
        by_type = locator.by_type
        if by_type == 'text':
            xpath_value = '//*[@text=\"%s\"]' % location
            return driver.find_element(By.XPATH, xpath_value) if is_single else driver.find_elements(By.XPATH,
                                                                                                     xpath_value)
        else:
            return driver.find_element(by_type, location) if is_single else driver.find_elements(by_type, location)

    def _send_key_event(self, arg, num=0):
        """
        模拟实体按键 https://developer.android.com/reference/android/view/KeyEvent.html
        :param arg: event_list key
        :param num: 当为 KEYCODE_NUM 时用到对应数字
        :return: 
        """
        event_list = {'KEYCODE_HOME': 3, 'KEYCODE_BACK': 4, 'KEYCODE_MENU': 82, 'KEYCODE_NUM': 7}
        if arg == 'KEYCODE_NUM':
            self.driver.press_keycode(int(event_list[arg]) + int(num))
        elif arg in event_list:
            self.driver.press_keycode(int(event_list[arg]))


action = _ElementActions()
