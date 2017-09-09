#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 09:04:54 2017

@author: caper911
"""


# url = http://npd.nsfc.gov.cn/fundingProjectSearchAction!search.action


#RatiNo
#ProName
#ItemClassification
#ClaimCode
#ProLeader
#OfficialTitle
#SupportOrganization
#DurationofResearch
#Subsidy

import re
import requests
from bs4 import BeautifulSoup

head = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11'}

cookies = {'JSESSIONID' : 'D715D4CE2EF12A4A3BBBBF1FC90ED1A9'}

cookies1 = {'JSESSIONID':'6C5AB7A32CC675B21311F8D7BDFB62B5'}
data = { 'pageSize':'21','currentPage':'1',
        'fundingProject.projectNo':'',
        'fundingProject.name':'',
        'fundingProject.person':'',
        'fundingProject.org':'',
        'fundingProject.applyCode':'',
        'fundingProject.grantCode':'',
        'fundingProject.subGrantCode':'',
        'fundingProject.helpGrantCode':'',
        'fundingProject.keyword':'',
        'fundingProject.statYear':'',
        'checkCode':'请输入验证码'}

#==============================================================================
url = r'http://npd.nsfc.gov.cn/fundingProjectSearchAction!search.action'
html_total = requests.post(url, data = data,cookies = cookies1,headers = head)
#print(html_total.text)

###
#get the total recode number
num_soup = BeautifulSoup(html_total.text,'html.parser')
total_recode_num_string = num_soup.find('p', id='num')
pattern=re.compile('[0-9]+')
total_recode_num = re.findall(pattern,total_recode_num_string.text)

print('total_recode_number:' + total_recode_num[0])


###
#get all the project id 
id_number_set = set()

i=1
pattern=re.compile('\d{8}')

while i < 5:
    data['currentPage'] = str(i)
    htmltotal = requests.post(url, data = data,cookies = cookies1,headers = head)    
    items = re.findall(pattern,htmltotal.text)
    for item in items:
        id_number_set.add(item)
    i = i+1

    
#print(id_number_set)

Targeturl = r'http://npd.nsfc.gov.cn/projectDetail.action?pid='
Project_list = []
for itemnum in id_number_set: 
    Targeturl = Targeturl + itemnum
    
    html = requests.get(Targeturl , cookies = cookies,headers = head)
    #print(html.text)
    
    if html.status_code!=200:
        print('catching id:'+ itemnum +' failure!')
        Targeturl = r'http://npd.nsfc.gov.cn/projectDetail.action?pid='
        continue
    
    soup = BeautifulSoup(html.text,'html.parser')


    # get the title
    Title = soup.find('h2', class_='title')
    Title = Title.get_text()
    Project_dict = {}
    Project_dict['title'] = str(Title)

    p_list = soup.find('div', id='right').find_all('p') 
    
    for p in p_list:
        Strlen = len(p.get_text())
        if( p.get_text()[0] == '批'):
            #print(p.get_text()[0:3] + ':' + p.get_text()[3:Strlen])
            Project_dict[p.get_text()[0:3]] = p.get_text()[3:Strlen]
        elif( p.get_text()[0:3] == '项目名'):
             #print(p.get_text()[0:4] + ':' + p.get_text()[4:Strlen])
            Project_dict[p.get_text()[0:4]] = p.get_text()[4:Strlen]
        elif( p.get_text()[0:3] == '项目类'):
            #print(p.get_text()[0:4] + ':' + p.get_text()[4:Strlen])
             Project_dict[p.get_text()[0:4]] = p.get_text()[4:Strlen]
        elif( p.get_text()[0:3] == '申请代'):
            #print(p.get_text()[0:4] + ':' + p.get_text()[4:Strlen])
            Project_dict[p.get_text()[0:4]] = p.get_text()[4:Strlen]
        elif( p.get_text()[0:3] == '项目负'):
            #print(p.get_text()[0:5] + ':' + p.get_text()[5:Strlen])
            Project_dict[p.get_text()[0:5]] = p.get_text()[5:Strlen]
        elif( p.get_text()[0:3] == '负责人'):
            #print(p.get_text()[0:5] + ':' + p.get_text()[5:Strlen])
            Project_dict[p.get_text()[0:5]] = p.get_text()[5:Strlen]
        elif( p.get_text()[0:3] == '依托单'):
            #print(p.get_text()[0:4] + ':' + p.get_text()[4:Strlen])
            Project_dict[p.get_text()[0:4]] = p.get_text()[4:Strlen]
        elif( p.get_text()[0:3] == '研究期'):
            #print(p.get_text()[0:4] + ':' + p.get_text()[4:Strlen])
            Project_dict[p.get_text()[0:4]] = p.get_text()[4:Strlen]
        elif( p.get_text()[0:3] == '资助经'):
            #print(p.get_text()[0:4] + ':' + p.get_text()[4:Strlen])
            Project_dict[p.get_text()[0:4]] = p.get_text()[4:Strlen]
        elif( p.get_text()[0:3] == '中文主'):
            #print(p.get_text()[0:5] + ':' + p.get_text()[5:Strlen])
            Project_dict[p.get_text()[0:5]] = p.get_text()[5:Strlen]
    
    Targeturl = r'http://npd.nsfc.gov.cn/projectDetail.action?pid='
    Project_list.append(Project_dict)
    print('catching id:'+ itemnum +' success!')
    
print(Project_list)

