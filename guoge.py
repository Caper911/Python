#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 21:52:32 2017

@author: caper911
"""

import requests
import pymongo
from lxml import etree

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11'}

client = pymongo.MongoClient('localhost',27017)
guoge = client['guoge']
question = guoge['question']

TargetUrl = r'http://www.guokr.com/ask/highlight/?page=' 

for i in range(1,101):
    TargetUrl = TargetUrl + str(i)
    print(TargetUrl)
    html = requests.get(TargetUrl,headers = headers)
    #print(html.text[1:10])
    html_text = etree.HTML(html.text)
    result = etree.tostring(html_text)
    #print(result)
    
    #print(type(html_text))
    item_dict = {}
    item_list = []
    j = 0
    for content in html_text.xpath('/html/body/div[3]/div[1]/ul[2]/li'):
        item_dict['title'] = content.xpath('//div[2]/h2/a/text()')[j]
        item_dict['Focus'] = content.xpath('//div[@class="ask-hot-nums"]/p[1]/span/text()')[j]
        item_dict['answer'] = content.xpath('//div[1]/p[2]/span/text()')[j].replace('\n','').strip()
        item_dict['link'] = content.xpath('//div[2]/h2/a/@href')[j]
        item_dict['content'] = content.xpath('//div[2]/p/text()')[j].replace('\n','').strip()
       
        print(item_dict)
        item_list.append(item_dict)
        question.insert_one(item_dict)
        item_dict = {}
        
        j += 1
    print("第"+ str(i) +"页抓取完成!")
    TargetUrl = TargetUrl = r'http://www.guokr.com/ask/highlight/?page=' 
    i += 1
