# -*- coding: utf-8 -*-

"""

@author: caper911
"""

import requests
from lxml import etree 
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rc('xtick', labelsize=10) #设置坐标轴刻度显示大小
mpl.rc('ytick', labelsize=10) 
#WenQuanYi Micro Hei


code = '002668'


Url = "http://quotes.money.163.com/fund/zycwzb_"+ code +".html"

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11'}

main_info_html = requests.get(Url , headers = headers)

main_info_text = etree.HTML(main_info_html.text)

Share_name = main_info_text.xpath('/html/body/div/div[4]/h2/small/a')[0].text
Share_worth = main_info_text.xpath('/html/body/div/div[4]/div/div/h3/big')[0].text
Share_manager = main_info_text.xpath('/html/body/div/div[4]/ul[1]/li[7]/span/a')[0].text
                                  
print('#######################')
print('基金名称:' + Share_name )
print('最新净值：' + Share_worth )
print('基金经理:' + Share_manager)

TargetUrl = "http://quotes.money.163.com/fund/zycwzb_"+ code +".html"

info_html = requests.get(TargetUrl , headers = headers)

info_text = etree.HTML(info_html.text)

table_name = []

#//*[@id="scrollTable"]/div[3]/table/thead/tr/th
table_info = info_text.xpath('//*[@id="scrollTable"]/div[3]/table/thead/tr/th/text()')[0]
table_name.append(table_info)
   
#//*[@id="scrollTable"]/div[3]/table/tbody/tr[1]/td
for i in range(1,6):    
    table_info = info_text.xpath('//*[@id="scrollTable"]/div[3]/table/tbody/tr['+str(i)+']/td')[0].text
    table_name.append(table_info)


#//*[@id="scroll_table_1"]/tbody/tr[1]/th

table_info = info_text.xpath('//*[@id="scroll_table_1"]/tbody/tr[1]/th')
table_info_1 = info_text.xpath('//*[@id="scroll_table_1"]/tbody/tr[2]/td')
table_info_2 = info_text.xpath('//*[@id="scroll_table_1"]/tbody/tr[3]/td')
table_info_3 = info_text.xpath('//*[@id="scroll_table_1"]/tbody/tr[4]/td')
table_info_4 = info_text.xpath('//*[@id="scroll_table_1"]/tbody/tr[5]/td')
table_info_5 = info_text.xpath('//*[@id="scroll_table_1"]/tbody/tr[6]/td')

table_info_list = []
table_info_dict = {}

x_names = []
y_names = []

for i in range(0,len(table_info)):
    table_info_dict[table_name[0]] = table_info[i].text
    x_names.append(table_info[i].text)
    table_info_dict[table_name[1]] = float(table_info_1[i].text.replace(',',''))
    table_info_dict[table_name[2]] = float(table_info_2[i].text.replace(',',''))
    table_info_dict[table_name[3]] = float(table_info_3[i].text.replace(',',''))
    table_info_dict[table_name[4]] = float(table_info_4[i].text.replace(',',''))
    table_info_dict[table_name[5]] = float(table_info_5[i].text.replace(',',''))
    y_names.append(table_info_dict[table_name[1]])
    table_info_list.append(table_info_dict)
    table_info_dict = {}               

    

print('\n基金编号:'+ str(code) + ' 主要财务指标抓取完成！')                           
print(table_name)
#print(table_info_list)


x = range(len(x_names))

plt.plot(x, y_names, 'ro-')

plt.xticks(x, x_names,rotation=30)
plt.margins(0.05)
plt.subplots_adjust(bottom=0.15)
plt.title(table_name[1]+'走势图')
plt.show()


# =============================================================================
# http://quotes.money.163.com/hk/service/cwsj_service.php?symbol=00700&start=2006-06-30&end=2016-12-31&type=cwzb
# http://quotes.money.163.com/hk/service/cwsj_service.php?symbol=00700&start=2006-06-30&end=2016-12-31&type=lrb
# http://quotes.money.163.com/hk/hk/service/cwsj_service.php?symbol=00700&start=2006-12-31&end=2016-12-31&type=fzb
# http://quotes.money.163.com/ hk/service/cwsj_service.php?symbol=00700&start=2006-06-30&end=2016-12-31&type=llb
# http://blog.csdn.net/c406495762/article/details/77801899
# =============================================================================


