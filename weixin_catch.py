#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 22:37:11 2017

@author: caper911
"""

import itchat
import re
from pandas import DataFrame
from wordcloud import WordCloud, ImageColorGenerator
import jieba
import PIL.Image as Image
import numpy as np
import matplotlib.pyplot as plt
import os


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

friend_text = "男性好友：" + "%.2f%%" % (float(male)/total*100) + "\n" \
            + "女性好友：" + "%.2f%%" % (float(female) / total * 100) + "\n"\
            + "不明性别好友：" + "%.2f%%" % (float(other) / total * 100)

itchat.send( friend_text , toUserName='filehelper')

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
text = ''
for i in range(1,len(Signature)):
    Signature[i] = Signature[i].strip()
    Signature[i] = Signature[i].replace('\n','')
    Signature[i] = reg.sub('',Signature[i])  
    text = text +' ' +Signature[i]
    i += 1 

data = {'NickName': NickName, 'Sex': Sex, 'City': City,'Signature': Signature}
frame = DataFrame(data)
frame.to_csv('data.csv', index=True)
print("数据生成成功!")

print(text)

####jieba
##wordcloud

##cut_text = " ".join(jieba.cut(text))  

#cut_for_search  
cut_text = " ".join(jieba.cut_for_search(text))

#print(cut_text)

d = os.path.dirname(__file__) # 获取当前文件路径
color_mask = np.array(Image.open(os.path.join(d,'jpg.png')))   # 设置图片

cloud = WordCloud(
  background_color='#F0F8FF',      # 参数为设置背景颜色,默认颜色则为黑色
  font_path="FZLTKHK--GBK1-0.ttf", # 使用指定字体可以显示中文，或者修改wordcloud.py文件字体设置并且放入相应字体文件
  max_words=1100,  # 词云显示的最大词数
  font_step=10,    # 步调太大，显示的词语就少了
  mask=color_mask,  #设置背景图片
  random_state= 15, # 设置有多少种随机生成状态，即有多少种配色方案
  min_font_size=13,  #字体最小值
  max_font_size=220, #字体最大值
  )

cloud.generate(cut_text)
image_colors = ImageColorGenerator(color_mask)       # 从背景图片生成颜色值
plt.show(cloud.recolor(color_func=image_colors))     # 绘制时用背景图片做为颜色的图片
plt.imshow(cloud)                                    # 以图片的形式显示词云
plt.axis('off')                                      # 关闭坐标轴
plt.show()                                           # 展示图片
cloud.to_file(os.path.join(d, 'pic.jpg'))            # 图片大小将会按照 mask 保存