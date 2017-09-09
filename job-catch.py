#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 21:55:50 2017

@author: caper911
爬取招聘网站--实习僧
"""

import requests
from bs4 import BeautifulSoup

TargetUrl = r'http://www.shixiseng.com/interns'

#the keyword of searching
Keyword = 'Python'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11'}

TargetUrl = TargetUrl+'?k='+Keyword

html = requests.get(TargetUrl,headers=headers)
#print(html.text)

html_soup = BeautifulSoup(html.text,'lxml')

job_name = html_soup.find('div',class_='names cutom_font').text
                         
print(job_name)                

