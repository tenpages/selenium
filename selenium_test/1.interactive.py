#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup

import time

browser = webdriver.Chrome()
browser.get("http://www.linkedin.com")
browser.maximize_window()

input_str=browser.find_element_by_xpath("//input[@type='text'][@class='login-email']")
input_str.send_keys("13300180080@fudan.edu.cn")#("==your mail here==")
input_str=browser.find_element_by_name("session_password")
input_str.send_keys("665991")#("==your pswd here==")
time.sleep(1)
input_str.send_keys(Keys.RETURN)
print("logged in")

print("redirecting")
time.sleep(5)

input_str=browser.find_element_by_xpath	("//input[@role='combobox'][@type='text']")
print('found')
input_str.clear()
input_str.send_keys('lisa sasa')
input_str.send_keys(Keys.RETURN)

print("redirecting")
time.sleep(5)

links=[]
cnt=1

while (1):
	print("Page %d" % cnt)
	time.sleep(3)
	cnt+=1
	try:
		input_str=browser.find_element_by_css_selector("ul[class='search-results__list list-style-none']")
	except NoSuchElementException:
		print("no such person")
		break
	soup=BeautifulSoup(input_str.get_attribute("innerHTML"), "lxml")
	for li in soup.body.find_all('li'):
		for tag in li.find('div').find_all('div'):
			if "search-result__info" in tag['class']:
				links.append(tag.a['href'])
				break
	try:
		button=browser.find_element_by_xpath("//button[@class='next']")
		button.click()
	except NoSuchElementException:
		print("fin")
		break

print("%d links collected."%len(links))

for link in links:
	browser.get("https://www.linkedin.com"+link)
	time.sleep(3)
