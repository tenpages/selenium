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
browser.get("http://www.pinterest.com/login/")
browser.maximize_window()

input_str=browser.find_element_by_xpath("//input[@type='email']")
input_str.clear()
input_str.send_keys(username)
input_str=browser.find_element_by_xpath("//input[@type='password']")
input_str.clear()
input_str.send_keys(password)
time.sleep(1)
input_str.send_keys(Keys.RETURN)
print("logged in")

print("redirecting")
time.sleep(5)

browser.get("https://www.pinterest.com/search/people/?q=%s&rs=filter" % search_name)
time.sleep(5)

for i in range(0,5):
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(2)

links=[]
cnt=1

try:
	search_page=browser.find_element_by_css_selector("div[class='SearchPageContent']")
	blocks=search_page.find_elements_by_tag_name('a')
	for a in blocks:
		links.append(BeautifulSoup(a.get_attribute("outerHTML"),"lxml").a['href'])
		cnt+=1
		#break #for test purpose
except NoSuchElementException:
	print("no result")

print("%d links collected."%len(links))

profile={}
profile_cnt=0
for link in links:
	try:
		browser.get("https://www.pinterest.com"+link)
	except:
		continue
	time.sleep(3)

	current_profile={}
	try:
		head=browser.find_element_by_css_selector("div[class='BrioProfileHeaderWrapper']")
	except:
		continue
	#name
	current_profile['name']=head.find_element_by_tag_name("h3").get_attribute("innerText")
	#photo
	current_profile['photo']=BeautifulSoup(head.find_element_by_tag_name("img").get_attribute("outerHTML"),'lxml').img['src']
	#shorttext
	findtext=head.find_elements_by_css_selector("div[class='_nv _ms _mt _mu _nx _5k _mv _n5 _n3 _mx']")[2].get_attribute("innerText")
	text=re.findall('([\S\s]*) / ([\S\s]*)',findtext)
	if not findtext=='':
		if len(text)!=0:
			current_profile['location']=text[0][0]
			current_profile['description']=text[0][1]
		else:
			current_profile['description']=findtext

	profile[profile_cnt]=current_profile
	profile_cnt+=1

with open("2.profiles.json","w") as f:
	json.dump(profile,f)
