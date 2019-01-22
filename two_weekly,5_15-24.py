# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import codecs
import re
import numpy as np

# for linuxOS
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

# アクセスするURL
url = "http://www.nikkei.com/markets/kabu/nidxprice/?StockIndex=N500"

html = requests.get(url)

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(html.text, "html.parser")
tr = soup.find_all("tr")

i = 2
while i <= 10 :
    url_tmp = "https://www.nikkei.com/markets/kabu/nidxprice/?StockIndex=N500&Gcode=00&hm=%d" % i
    html_tmp = requests.get(url_tmp)
    soup_tmp = BeautifulSoup(html_tmp.text, "html.parser")
    tr += soup_tmp.find_all("tr")
    i += 1

brand = []
name = []
ratio = []
sales_vol = []

f = open('get_1month_stock_data.txt', 'w')

for tag in tr :
    try:
        string_ = tag.get("class").pop(0)
        if string_ in "tr2" :
            td = tag.find_all("td")
            span = tag.find_all("span")
            for info_b in td[0] :
                brand.append(info_b.string)
            for info_n in td[1] :
                name.append(info_n.string)
        
        if string_ in "tr3" :
            td = tag.find_all("td")
            span = tag.find_all("span")
            for info_b in td[0] :
                brand.append(info_b.string)
            for info_n in td[1] :
                name.append(info_n.string)
    except :
        pass


brand_num = 0
for b_num in brand :

    url_1mon = "https://www.nikkei.com/nkd/company/history/dprice/?scode=%s&ba=1" % b_num
    html_1mon = requests.get(url_1mon)
    soup_1mon = BeautifulSoup(html_1mon.text, "html.parser")
    tr_1mon_table = soup_1mon.find_all("table")
    tr_1mon = []
    tr_1mon_tbody = []
    th_title = []
    th_with_days = []
    th = []
    td = [[] for i in range(25)]
    stock_num = 0
    print("")
    print(name[brand_num])
    for tmp_table in tr_1mon_table :
        tr_1mon_tbody = tmp_table.find_all("tbody")
        tr_1mon_thead = tmp_table.find_all("thead")
    for tmp_thead in tr_1mon_thead :
        tr_thead = tmp_thead.find_all("th")
    for tmp_tr_thead in tr_thead :
        th_title.append(tmp_tr_thead.string.replace("\r", "").replace("\n", ""))
    
    for tmp_tbody in tr_1mon_tbody :
        tr_1mon.append(tmp_tbody.find_all("tr"))
    for tmp_tr_list in tr_1mon :
        for tmp_tr in tmp_tr_list :
            th_1mon = tmp_tr.find_all("th")
            for tmp_th in th_1mon :
                th_with_days.append(tmp_th.string.replace("\r", "").replace("\n", "").replace(" ", ""))
            td_1mon = (tmp_tr.find_all("td"))
            for tmp_td in td_1mon :
                td[stock_num].append(tmp_td.string)
            result_replace = re.sub('[^0-9, /]', '', th_with_days[stock_num])
            tmp_num = re.match('[0-9]+', result_replace)
            if tmp_num.group() == '1' :
                appendance = re.sub('1/', '2019/1/', result_replace)
            elif tmp_num.group() == '2' :
                appendance = re.sub('2/', '2019/2/', result_replace)
            elif tmp_num.group() == '12' :
                appendance = re.sub('12/', '2018/12/', result_replace)
            th.append(appendance)
            if stock_num == 5 :
                print((u"{0[3]}".format(td[stock_num])).replace("u", "").replace(',', ''))
                f.write((u"{0[3]}\n".format(td[stock_num])).replace("u", "").replace(',', '').encode('utf-8'))
            elif stock_num >= 15 :
                print((u"{0[3]}".format(td[stock_num])).replace("u", "").replace(',', ''))
                f.write((u"{0[3]}\n".format(td[stock_num])).replace("u", "").replace(',', '').encode('utf-8'))
            stock_num += 1
    brand_num += 1
f.close
