from selenium import webdriver
from lib.browser import browser
from selenium.webdriver.common.by import By

browser = browser('chrome', remoteAddress='http://127.0.0.1:4444/wd/hub')
browser.get('http://www.baidu.com')
browser.click((By.LINK_TEXT, '新闻'))
browser.wait(5)
browser.quit()
