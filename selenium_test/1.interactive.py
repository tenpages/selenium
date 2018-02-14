#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

browser = webdriver.Chrome()
browser.get("http://www.linkedin.com")
input_str=browser.find_element_by_xpath("//input[@type='text'][@class='login-email']")
input_str.send_keys("==your mail here==")
input_str=browser.find_element_by_name("session_password")
input_str.send_keys("==your pswd here==")
time.sleep(1)
input_str.send_keys(Keys.RETURN)
print("logged in")

time.sleep(5)
print("redirecting")

input_str=browser.find_element_by_xpath	("//input[@role='combobox'][@type='text']")
print('found')
input_str.clear()
input_str.send_keys('Lisa')
input_str.send_keys(Keys.RETURN)