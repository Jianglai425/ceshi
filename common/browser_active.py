import time

import allure
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select


class BrowserType:
    Chrome = 'Chrome'
    Edge = 'Edge'


class SelectType:
    Index = 1
    Value = 2
    Text = 3


class BrowserActive:
    """
    浏览器操作类，所有和浏览器操作有关的放在这个类里。
    """

    def __init__(self, browser_type: str = None, url: str = None, maximize_window: bool = True, wait: int = 10,
                 driver=None) -> None:
        """
        初始化，并且打开浏览器进入网页，或者是通过接受浏览器对象来对源对象进行类型转换。
        :param browser_type: 浏览器的类型，目前支持谷歌浏览器和微软浏览器。
        :param url: 第一个访问的路径，带不带协议名都可。
        :param maximize_window: 浏览器窗口是否最大化，默认会进行最大化。
        :param wait: 隐式等待时间。
        :param driver: 这个参数只在浏览器对象类型转化的时候用，初始化时不用填。类型转化时在此参数传入源浏览器对象内的驱动进行类型转化。
        """
        if driver is None:
            dr = {"Chrome": webdriver.Chrome, "Edge": webdriver.Edge}
            self._browser = dr.get(browser_type)()
            if maximize_window:
                self._browser.maximize_window()
            self._browser.implicitly_wait(wait)
            with allure.step("进入网页"):
                if url.startswith(("http://", "https://")):
                    self._browser.get(url)
                else:
                    self._browser.get("http://" + url)
        else:
            self._browser = driver

    def switch_window(self, url):
        handles = self._browser.window_handles
        for i in range(len(handles)):
            self._browser.switch_to.window(handles[i])
            if self._browser.current_url == url:
                break

    def switch_frame(self, path_type, path):
        self._browser.switch_to.frame(self._browser.find_element(path_type, path))

    def show_down(self):
        self._browser.quit()

    def get_webdriver(self):
        return self._browser

    def save_screenshot(self, name):
        allure.attach(self._browser.get_screenshot_as_png(),
                      name + "%s-%.0f.png" % (time.strftime('%Y-%m-%d %H:%M：%S', time.localtime()), time.time()),
                      allure.attachment_type.PNG)


class ElementActive(BrowserActive):
    """
    元素操作类，继承浏览器操作类，所有对页面元素的操作放在这个类里。
    """

    def click(self, path):
        """
        鼠标单次点击
        :param path: 坐标
        :return: 无
        """
        self._browser.find_element(*path).click()

    def send_key(self, path, value, clear: bool = False):
        """
        输入值，是否清除原有值由传入的参数决定
        :param path: 元素坐标
        :param value: 需要填入的值
        :param clear: 是否清除原有值，清除传入True，默认不清除
        :return: 无
        """
        if clear:
            self._browser.find_element(*path).clear()
        self._browser.find_element(*path).send_keys(value)

    def select(self, path, value_type, value):
        """
        对select元素进行操作
        :param path: 元素坐标
        :param value_type: 传入值根据什么选择，是select的value值还是index值还是显示的文本，只有三个选项（Index,Value,Text）。
        :param value: 传入的值
        :return:
        """
        e = Select(self._browser.find_element(*path))
        select_type = {1: e.select_by_index, 2: e.select_by_value, 3: e.select_by_visible_text}
        # noinspection PyArgumentList
        select_type.get(value_type)(value)

    def move_element(self, path):
        """
        移动到某一个元素上。
        :param path 元素坐标
        :return:
        """
        ActionChains(self._browser).move_to_element(self._browser.find_element(*path)).perform()

    def scroll(self):
        self._browser.execute_script("document.documentElement.scrollTop=10000")

    def find_element(self, path):
        return self._browser.find_element(*path)


if __name__ == '__main__':
    pass
