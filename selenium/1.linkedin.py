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

input_str=browser.find_element_by_xpath("//input[@role='combobox'][@type='text']")
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
	#break #for test purpose

print("%d links collected."%len(links))

profile={}
profile_cnt=0
for link in links:
	browser.get("https://www.linkedin.com"+link)

	time.sleep(3)
	for i in range(0,3):
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(1)

	current_profile={}
	
	#photo
	top_card=browser.find_element_by_css_selector("div[class='pv-top-card-section__photo-wrapper EntityPhoto-circle-8']")
	soup_top_card=BeautifulSoup(top_card.get_attribute("innerHTML"),"lxml")
	divs=soup_top_card.div.div
	try:
		current_profile['photo']=re.findall('background-image: url\("(\S*)"\);',divs['style'])[0]
	except:
		current_profile['photo']=""
	
	#top_card information: name, headline, position and edu
	top_card=browser.find_element_by_css_selector("div[class='pv-top-card-section__information mt3 ember-view']")
	soup_top_card=BeautifulSoup(top_card.get_attribute("innerHTML"),"lxml")
	divs=soup_top_card.find_all('div')
	current_profile['name']=divs[0].h1.string
	current_profile['headline']=soup_top_card.h2.string
	
	experiences=divs[2].find_all('h3')
	for experience in experiences:
		current_profile[re.findall('\S*__(\S*)',experience['class'][0])[0]]=experience.string.strip()
	
	#experience
	try:
		profile_detail=browser.find_element_by_id("experience-section")
		try:
			button=profile_detail.find_element_by_css_selector("button[class='pv-profile-section__see-more-inline link']")
			button.send_keys(Keys.RETURN)
			time.sleep(5)
		except:
			button=""
		profile_detail=browser.find_element_by_id("experience-section")
		soup_profile_detail=BeautifulSoup(profile_detail.get_attribute("innerHTML"),"lxml")
		lis=soup_profile_detail.ul.find_all('li')
		experience_his={}
		cnt=1
		for li in lis:
			his_tmp={}
			#print(li)
			if ('pv-profile-section__sortable-item' not in li['class']) and ('pv-profile-section__card-item' not in li['class']):
				continue
			his_tmp['position']=li.a.find_all('div')[1].h3.string
			h4s=li.a.find_all('div')[1].find_all('h4')
			for span in h4s[0].find_all('span'):
				if 'pv-entity__secondary-title' in span['class']:
					his_tmp['company_name']=span.string
					break
			for span in h4s[1].find_all('span'):
				if not span.attrs.__contains__('class'):
					his_tmp['time_span']=span.string
					break
			if len(h4s)>3:
				for span in h4s[3].find_all('span'):
					if not span.attrs.__contains__('class'):
						his_tmp['company_location']=span.string
						break
			experience_his[cnt]=his_tmp
			cnt+=1
		print(cnt)
		current_profile['experience']=experience_his
	except:
		experience_his=""

	#education
	try:
		profile_detail=browser.find_element_by_id("education-section")
		try:
			button=profile_detail.find_element_by_css_selector("button[class='pv-profile-section__see-more-inline link']")
			button.send_keys(Keys.RETURN)
			time.sleep(5)
		except:
			button=""
		profile_detail=browser.find_element_by_id("education-section")
		soup_profile_detail=BeautifulSoup(profile_detail.get_attribute("innerHTML"),"lxml")
		lis=soup_profile_detail.ul.find_all('li')
		education_his={}
		cnt=1
		for li in lis:
			his_tmp={}
			if ('pv-profile-section__sortable-item' not in li['class']) and ('pv-profile-section__card-item' not in li['class']):
				continue
			school=li.div.a.find_all('div')[1]
			his_tmp['school_name']=school.div.h3.string
			school_detail=school.div.find_all('p')
			for p in school_detail:
				name=""
				value=""
				for span in p.find_all('span'):
					#print(span)
					if span.attrs.__contains__('class'):
						if 'visually-hidden' in span['class']:
							name=span.string.lower().replace(' ','_')
						else:
							value=span.string
				his_tmp[name]=value

			education_his[cnt]=his_tmp
			cnt+=1
		#print(cnt)
		current_profile['education']=education_his
	except:
		education_his=""

	#volunteering
	try:
		profile_detail=browser.find_element_by_css_selector("section[class='pv-profile-section volunteering-section ember-view']")
		try:
			button=profile_detail.find_element_by_css_selector("button[class='pv-profile-section__see-more-inline link']")
			button.send_keys(Keys.RETURN)
			time.sleep(5)
		except:
			button=""
		profile_detail=browser.find_element_by_css_selector("section[class='pv-profile-section volunteering-section ember-view']")
		soup_profile_detail=BeautifulSoup(profile_detail.get_attribute("innerHTML"),"lxml")
		lis=soup_profile_detail.ul.find_all('li')
		volunteering_his={}
		cnt=1
		for li in lis:
			his_tmp={}
			if ('pv-profile-section__sortable-item' not in li['class']) and ('pv-profile-section__card-item' not in li['class']):
				continue
			organization=li.a.find_all('div')[1]
			his_tmp['position']=organization.h3.string
			volunteering_detail=organization.find_all('h4')
			for h4 in volunteering_detail:
				name=""
				value=""
				for span in h4.find_all('span'):
					#print(span)
					if span.attrs.__contains__('class'):
						if 'visually-hidden' in span['class']:
							name=span.string.lower().replace(' ','_')
						else:
							value=span.string.strip()
				his_tmp[name]=value

			volunteering_his[cnt]=his_tmp
			cnt+=1
		#print(cnt)
		current_profile['volunteering']=volunteering_his
	except:
		volunteering_his=""

	#acquaintance via recommendations
	try:
		cnt=1
		acquaintance={}
		profile_detail=browser.find_element_by_tag_name("artdeco-tabs")
		#Received
		try:
			button=profile_detail.find_element_by_tag_name("artdeco-tabpanel").find_element_by_tag_name("button")
			button.send_keys(Keys.RETURN)
		except:
			button=""
		time.sleep(3)
		try:
			lis=BeautifulSoup(profile_detail.find_element_by_tag_name('ul').get_attribute("innerHTML"),"lxml").find_all('li')
			for li in lis:
				acquaintance[cnt]=li.div.a.div.h3.string
				cnt+=1
		except:
			#no recommendation
			lis=""
		#Given
		tabs=profile_detail.find_elements_by_tag_name("artdeco-tab")
		tabs[0].send_keys(Keys.ARROW_RIGHT)
		time.sleep(3)
		try:
			button=profile_detail.find_elements_by_tag_name("artdeco-tabpanel")[1].find_element_by_tag_name("button")
			button.send_keys(Keys.RETURN)
		except:
			button=""
		time.sleep(3)
		try:
			lis=BeautifulSoup(profile_detail.find_elements_by_tag_name('ul')[1].get_attribute("innerHTML"),"lxml").find_all('li')
			for li in lis:
				acquaintance[cnt]=li.div.a.div.h3.string
				cnt+=1
		except:
			#no recommendation
			lis=""
		current_profile['acquaintance']=acquaintance
	except:
		acquaintance={}

	profile[profile_cnt]=current_profile
	profile_cnt+=1

	#break #for test purpose

with open("profiles.json","w") as f:
	json.dump(profile,f)
