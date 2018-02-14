from selenium import webdriver

import time

browser = webdriver.Chrome()
browser.get("http://www.taobao.com")
input_str=browser.find_element_by_id('q')
input_str=send_keys("ipad")
time.sleep(1)
input_str.clear()
input_str.send_keys("Macbook pro")
button = browser.find_element_by_class_name('btn-search')
button.click()
