# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

# アクセスするURL
url = "http://www.nikkei.com/markets/kabu/nidxprice/"

html = requests.get(url)

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(html.text, "html.parser")
tr = soup.find_all("tr")

i = 2
while i <= 5 :
    url_tmp = "https://www.nikkei.com/markets/kabu/nidxprice/?StockIndex=NAVE&Gcode=00&hm=%d" % i
    html_tmp = requests.get(url_tmp)
    soup_tmp = BeautifulSoup(html_tmp.text, "html.parser")
    tr += soup_tmp.find_all("tr")
    i += 1

brand = []
name = []
ratio = []
sales_vol = []

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
            for info_r in span[5] :
                ratio.append(info_r.string)
            for info_v in td[7] :
                sales_vol.append(info_v.string)
        
        if string_ in "tr3" :
            td = tag.find_all("td")
            span = tag.find_all("span")
            for info_b in td[0] :
                brand.append(info_b.string)
            for info_n in td[1] :
                name.append(info_n.string)
            for info_r in span[5] :
                ratio.append(info_r.string)
            for info_v in td[7] :
                sales_vol.append(info_v.string)
    except :
        pass
    
title = soup.title.string

# タイトルを文字列を出力
print (title)

pri_len = len(name)
i = 0
#print(ratio)

while i < pri_len :
    
    print_ = (u"brand : {:<4}, name : {:->6}, ratio : {:<5}, sales_volume : {:>11}".format(brand[i], name[i], ratio[i], sales_vol[i]))
    print(print_.replace(u"-", u"　").replace(u"±", u"　"))
    i += 1

print(u"銘柄数 : " + str(pri_len))

brand_num = 0
for b_num in brand :
    try :
        url_1mon = "https://www.nikkei.com/nkd/company/history/dprice/?scode=%s&ba=1" % b_num
        html_1mon = requests.get(url_1mon)
        soup_1mon = BeautifulSoup(html_1mon.text, "html.parser")
        tr_1mon_table = soup_1mon.find_all("table")
        tr_1mon = []
        tr_1mon_tbody = []
        th = []
        td = [[] for i in range(25)]
        stock_num = 0
        print(name[brand_num])
        for tmp_table in tr_1mon_table :
            tr_1mon_tbody = tmp_table.find_all("tbody")
        for tmp_tbody in tr_1mon_tbody :
            tr_1mon.append(tmp_tbody.find_all("tr"))
        for tmp_tr_list in tr_1mon :
            for tmp_tr in tmp_tr_list :
                th_1mon = tmp_tr.find_all("th")
                for tmp_th in th_1mon :
                    th.append(tmp_th.string.replace("\r", "").replace("\n", "").replace(" ", ""))
                td_1mon = (tmp_tr.find_all("td"))
                for tmp_td in td_1mon :
                    td[stock_num].append(tmp_td.string)
                print((u"{0} : {1}".format(th[stock_num], td[stock_num])).replace("u", ""))
                stock_num += 1
        brand_num += 1
    except :
        pass
