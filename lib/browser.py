# coding = utf-8

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
from time import sleep as wait
import configinfo
import lib.logUntil

log = lib.logUntil.Log()


class browser(object):
    """
    二次封装，selenium常用操作方法
    """

    def __init__(self, browserName='chrome', executable_path=None, remoteAddress=None):
        """
        实例化浏览器，
        :param   browserName 指定浏览器类型 chrome firefox ie
        :param   executable_path 驱动路径
        :param   remoteAddress 远程执行路径地址
        :Usage:
        browser = browser('chrome') # 本地执行
        path = os.path.abspath('./driver/chromedriver.exe')
        browser = browser('chrome',executable_path=path) # 本地执行，指定驱动位置
        browser = browser('chrome',remoteAddress='http://127.0.0.1:4444/wd/hub') # 远程执行，指定远程地址
        """
        # 加载driver下的驱动
        driver_path = configinfo.driver_path
        os.environ['PATH'] = os.environ['PATH'] + ';' + driver_path

        if remoteAddress is not None:
            desired_capabilities = {'platform': 'ANY', 'version': '',
                                    'javascriptEnabled': True}
            if browserName.lower() == 'chrome':
                desired_capabilities['browserName'] = 'chrome'
            elif browserName.lower() == 'firefox':
                desired_capabilities['browserName'] = 'firefox'
                desired_capabilities['marionette'] = False
            elif browserName.lower() == 'ie':
                desired_capabilities['browserName'] = 'internet explorer'
            else:
                log.error('无此浏览器驱动或者指定浏览器类型错误')
                raise NameError('请指定浏览器类型：chrome firefox ie')

            self.driver = webdriver.Remote(command_executor=remoteAddress,
                                           desired_capabilities=desired_capabilities)
            log.info(browserName + '成功远程启动')
        else:
            # 加载指定路径的驱动
            if executable_path is not None:
                dir_path = os.path.abspath(executable_path)
                if os.path.isfile(dir_path):
                    dir_path = os.path.dirname(dir_path)
                os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path
                log.info(dir_path + '目录下驱动加载成功')
            if browserName.lower() == 'chrome':
                self.driver = webdriver.Chrome()
            elif browserName.lower() == 'firefox':
                self.driver = webdriver.Firefox()
            elif browserName.lower() == 'ie':
                self.driver = webdriver.Ie()
            else:
                log.error('无此浏览器驱动或者指定浏览器类型错误')
                raise NameError('请指定浏览器类型：chrome firefox ie')
            log.info(browserName + '成功启动')

    def get(self, url):
        """ 打开网页
        @:param url 网址
        :Usage:
        browser.get('www.xxxx.com')
        """
        self.driver.get(url)

    def open_win(self, url):
        """
        打开另一个浏览器窗口
        :param url: url地址
        :Usage:
        browser.open_win('http://www.xxx.com')
        """
        js = 'window.open("' + url + '")'
        self.driver.execute_script(js)
        log.info('成功打开网址' + url)

    def close(self):
        """
        关闭当前窗口
        :Usage:
        browser.close()
        """
        self.driver.close()

    def quit(self):
        """退出浏览器
        :Usage:
        browser.quit()
        """
        self.driver.quit()

    def max_window(self):
        """
        最大化浏览器
        :Usage:
        browser.max_window()
        """
        self.driver.maximize_window()

    def set_window_size(self, w, h):
        """
        设置浏览器大小
        :param w: 浏览器宽度
        :param h: 浏览器高度
        :Usage:
        browser.set_window_size(400,800)
        """
        self.driver.set_window_size(w, h)

    def implicitly_wait(self, secsonds):
        """
        隐性等待,等待元素出现
        :param secsonds:
        :Usage:
        browser.implicitly_wait(30)
        """
        self.driver.implicitly_wait(secsonds)

    def wait(self, s):
        """
        固定等待s秒
        :param s: s秒
        :Usage:
        browser.wait(5)
        """
        import time
        time.sleep(s)

    def wait_element(self, located, seconds=5):
        """
        等待元素对象出现
        也可以使用此方法获取元素
        注意：如果元素隐藏，对此方法无影响
        :param located: 元素 (By.id,value)
        :param seconds: 时间
        :return 返回等待出现的元素
        :Usage:
        located=(By.id,value)
        browser.wait_element(located,30)
        """
        try:
            element = WebDriverWait(self.driver, seconds, 1).until(EC.presence_of_element_located(located))
            return element
        except TimeoutException:
            log.warning(str(seconds) + '秒内没有等待到' + str(located) + '元素出现')

    def wait_element_display(self, located, seconds=5):
        """
        等待元素对象出现，并可见,元素的 is_displayed为True
        也可以使用此方法获取元素
        :param located:
        :param seconds:
        :return:
        """
        try:
            element = WebDriverWait(self.driver, seconds, 1).until(EC.visibility_of_element_located(located))
            return element
        except TimeoutException:
            log.warning(str(seconds) + '秒内没有等待到可见元素出现' + str(located))

    def find_element(self, locator):
        """
        查找元素对象
        :param locator: 元素定位 (By.id,'id_name')
        :Usage:
        locator=(By.id,'id_name')
        browser.find_element(locator)
        """
        try:
            self.wait_element(locator, 3)
            return self.driver.find_element(*locator)
        except NoSuchElementException:
            log.error('无法获取元素' + locator)
            assert False, '无法获取元素' + str(locator)

    def input(self, located, value):
        """
        输入框输入值
        :param located: （By.ID,'id'） By等位元素
        :param value:    'selenium' 输入值
        :return:
        :Usage:
        located=(By.id,'id_name')
        browser.input(located,'自动化测试培训')
        """
        if self.find_element(located).is_displayed():
            self.find_element(located).send_keys(str(value))
            log.info(str(located) + '输入' + str(value) + '成功')
        else:
            log.error('元素不可见，无法输入' + str(located))

    def click(self, located):
        """
        单击
        :param located: 元素（By.ID,'id'）
        :return:
        """

        if self.find_element(located).is_displayed():
            self.find_element(located).click()
            log.info(str(located) + '单击成功')
        else:
            log.error('元素不可见，无法单击' + str(located))

    def right_click(self, located):
        """
        在元素上右击
        :param located: (By,id,'id')
        :return:
        """
        element = self.find_element(located)
        ActionChains(self.driver).context_click(element).perform()
        log.info('右击元素' + str(located))

    def move_to_element(self, located):
        """
        鼠标移动到元素上
        :param located: (By,id,'id')
        """
        element = self.find_element(located)
        ActionChains(self.driver).move_to_element(element).perform()
        log.info('鼠标移动到元素上' + str(located))

    def double_click(self, located):
        """
        在元素上双击
        :param located: (By,id,'id')
        :return:
        """
        element = self.find_element(located)
        ActionChains(self.driver).double_click(element).perform()
        log.info('双击元素' + str(located))

    def get_attribute(self, located, attribute):
        """
        获取元素的属性值
        :param located: (By,id,'id')
        :param attribute: 属性
        :return:
        """
        if self.find_element(located).is_displayed():
            self.find_element(located).get_attribute(attribute)
        else:
            log.warning(str(located) + '元素不可见，无法获取' + attribute + '值，')

    def get_text(self, located):
        if self.find_element(located).is_displayed():
            return self.find_element(located).text
        else:
            log.warning(str(located) + '元素不可见，无法获取text值')

    def switch_to_frame(self, frame):
        """
        :param frame: id/name/index 属性
        :Usage:
        driver.switch_to_frame('frame_name')
        driver.switch_to_frame(1)
        driver.switch_to_frame(driver.find_elements_by_tag_name("frame")[0])
        """
        try:
            self.driver.switch_to.frame(frame)
        except NoSuchFrameException:
            log.error('无法找到你需要' + frame)
            assert False, '无法找到你需要' + str(frame)

    def switch_to_frame_out(self):
        """
        从frame切换回主页面
        :Usage:
        driver.switch_to_frame_out('frame_name')
        """
        self.driver.switch_to.default_content()
        log.info('从frame切换回主页面')

    def switch_to_window(self, winB):
        """
        :param winB:
            1.切换窗口的标题
            2.切换窗口的序号
            3.切换页面的元素
        :return: True 切换成功
        :Usage:
        driver.switch_to_window('win_name')
        driver.switch_to_window(2) # 切换到第二个窗口
        located=(By.ID,'id') # 确定切换页面的元素
        driver.switch_to_window(located) # 切换到页面中存在id=‘id’ 的元素
        """
        result = False
        handles = self.driver.window_handles
        current_handle = self.driver.current_window_handle
        if isinstance(winB, tuple):
            for handle in handles:
                self.driver.switch_to.window(handle)
                self.wait(3)
                try:
                    self.driver.find_element(*winB)
                except NoSuchElementException:
                    pass
                else:
                    result = True
                    break
            if not result:
                log.warning('无获取【' + str(winB) + '】元素，没有找到对应的窗口,切换回原窗口')
                self.driver.switch_to.window(current_handle)
                self.wait(2)
        elif isinstance(winB, str):
            for handle in handles:
                self.driver.switch_to.window(handle)
                self.wait(2)
                if winB in self.driver.title:
                    result = True
                    break
            if not result:
                log.warning('标题【' + winB + '】错误，没有找到对应的窗口,切换回原窗口')
                self.driver.switch_to.window(current_handle)
                self.wait(2)
        elif isinstance(winB, int):
            if winB <= len(handles):
                self.driver.switch_to.window(winB - 1)
                self.wait(2)
                result = True
            else:
                log.warning('没有' + str(winB) + '个窗口')
        return result

    def exec_js(self, js):
        """
        执行JS语句
        :param js:
        :return:
        """
        js_value = self.driver.execute_script(js)
        log.info('执行' + js)
        return js_value

    def scroll_top(self, high):
        """
        向下滚动浏览器滚动条
        :param high: 滚动条距离顶部的距离
        """
        js = 'document.body.scrollTop=' + str(high)
        self.driver.execute_script(js)
        wait(2)
        log.info('向下滚动' + str(high) + '距离的浏览器滚动条')

    def scroll_page(self):
        """
        浏览器上下滚动条向下滚动一页
        :return:
        """
        js = 'return(document.body.scrollTop=document.body.scrollTop+document.documentElement.clientHeight-5);'
        self.driver.execute_script(js)
        wait(2)
        log.info('向下翻页')

    def alert_accept(self):
        """
        确认alert弹窗
        :return: 返回alert文本信息
        """
        WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        log.info('确认alert弹窗')
        return alert_text

    def alert_dismiss(self):
        """
        取消alert弹窗
        :return: 返回alert文本信息
        """
        WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.dismiss()
        log.info('取消alert弹窗')
        return alert_text

    def select(self, element, arg):
        """
        选择下拉框的值
        :param element: 下拉框的元素
        :param arg: 需要选择的值
                        1       ：index定位，从0开始
                        'value' ：根据值定位
                        'text'  ：根据文本定位
        :return:
        """
        from selenium.webdriver.support.select import Select
        select_element = Select(element)
        try:
            if isinstance(arg, int):
                select_element.select_by_index(arg)
            else:
                try:
                    select_element.select_by_value(arg)
                except NoSuchElementException:
                    select_element.select_by_visible_text(arg)
        except NoSuchElementException:
            log.error('下拉框 无此选项' + str(arg))
            raise (NoSuchElementException, '下拉框 无此选项')
        log.info('下拉框 选择值' + str(arg))


if __name__ == '__main__':
    from selenium.webdriver.common.by import By

    dr = browser()
    dr.get('http://sahitest.com/demo/selectTest.htm')
    ele = dr.find_element((By.ID, 's1Id'))
    dr.select(ele, 2)
    dr.select(ele, 'o1')
    dr.wait(10)
    dr.quit()
