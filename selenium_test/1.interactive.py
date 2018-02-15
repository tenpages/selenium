#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup

import time
import re
import json

search_name='lisa singh'
username="gu.datalab6@gmail.com"
password="gudatala"

browser = webdriver.Chrome()
browser.get("http://www.linkedin.com")
browser.maximize_window()

input_str=browser.find_element_by_xpath("//input[@type='text'][@class='login-email']")
input_str.send_keys(username)
input_str=browser.find_element_by_name("session_password")
input_str.send_keys(password)
time.sleep(1)
input_str.send_keys(Keys.RETURN)
print("logged in")

print("redirecting")
time.sleep(5)

input_str=browser.find_element_by_xpath	("//input[@role='combobox'][@type='text']")
print('found')
input_str.clear()
input_str.send_keys(search_name)
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
	break

print("%d links collected."%len(links))

profile={}
cnt=0
for link in links:
	browser.get("https://www.linkedin.com"+link)

	time.sleep(3)
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	current_profile={}

	top_card=browser.find_element_by_css_selector("div[class='pv-top-card-section__information mt3 ember-view']")
	soup_top_card=BeautifulSoup(top_card.get_attribute("innerHTML"),"lxml")
	divs=soup_top_card.find_all('div')
	current_profile['name']=divs[0].h1.string
	current_profile['headline']=soup_top_card.h2.string
	
	experiences=divs[2].find_all('h3')
	for experience in experiences:
		current_profile[re.findall('\S*__(\S*)',experience['class'][0])[0]]=experience.string.strip()

	profile[cnt]=current_profile
	cnt+=1	
	#break

with open("profiles.json","w") as f:
	json.dump(profile,f)
