#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 22:37:11 2017

@author: caper911
"""

import itchat
import re
from pandas import DataFrame

itchat.login()

friends = itchat.get_friends(update=True)[0:]
#print(friends)

male = female = other = 0

#friends[0]是自己的信息，所以要从friends[1]开始
for i in friends[1:]:
    sex = i["Sex"]
    if sex == 1:
        male += 1
    elif sex == 2:
        female += 1
    else:
        other +=1
#计算朋友总数
total = len(friends[1:])
#打印出自己的好友性别比例
# print("男性好友： %.2f%%" % (float(male)/total*100) + "\n" +
# "女性好友： %.2f%%" % (float(female) / total * 100) + "\n" +
# "不明性别好友： %.2f%%" % (float(other) / total * 100))


def get_varInfriends(var):
    varialbe = []
    for i in friends:
        value = i[var]
        varialbe.append(value)
    return varialbe

#调用函数得到各变量，并把数据存到csv文件中，保存到桌面
NickName = get_varInfriends("NickName")
Sex = get_varInfriends('Sex')
Province = get_varInfriends('Province')
City = get_varInfriends('City')
Signature = get_varInfriends('Signature')


## 拼接省份和城市
for i in range(1,len(City)):
    City[i] = Province[i] + City[i]
    i += 1    

reg = re.compile('<[^>]*>')  

for i in range(1,len(Signature)):
    Signature[i] = Signature[i].strip()
    Signature[i] = Signature[i].replace('\n','')
    Signature[i] = reg.sub('',Signature[i])  
    i += 1 

data = {'NickName': NickName, 'Sex': Sex, 'City': City,'Signature': Signature}
frame = DataFrame(data)
frame.to_csv('data.csv', index=True)
print("数据生成成功!")
    
