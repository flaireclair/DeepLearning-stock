# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import codecs
import re
import numpy as np

# for linuxOS
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

two_weekly_list = []
dif_four_two_list = []
dif_four_two_list_plus = []
dif_four_two_list_minus = []


def dif_fourday_twoweekly() :
    tmp_weekly = None
    two_weekly_plus = []
    two_weekly_minus = []
    i = 0
    
    for tmp_2week in td[::-1] :
        if i == 10 :
            break
        if tmp_weekly == None :
            tmp_weekly = float(tmp_2week[3].replace('u', '').replace(',', ''))
            continue
        tmp_2week_int = float(tmp_2week[3].replace('u', '').replace(',', ''))
        judge_pm = tmp_2week_int - tmp_weekly
        tmp_weekly = tmp_2week_int
        print(judge_pm)
        if judge_pm >= 0 :
            two_weekly_plus.append(judge_pm)
        else :
            two_weekly_minus.append(judge_pm)
        i += 1

    plus_sum = None
    minus_sum = None
    for plus in two_weekly_plus :
        if plus_sum == None :
            plus_sum = float(plus)
            continue
        plus_sum += plus
    for minus in two_weekly_minus :
        if minus_sum == None :
            minus_sum = float(minus)
            continue
        minus_sum += minus

    two_weekly = float((plus_sum / (plus_sum + (minus_sum * -1))) * 100)

    print(two_weekly)
    
    if two_weekly <= 30 :
        two_weekly_list.append(two_weekly)

        dif_four_two  = float(td[5][3].replace('u', '').replace(',', '')) - float(td[14][3].replace('u', '').replace(',', ''))

        if dif_four_two >= 0 :
            dif_four_two_list_plus.append(dif_four_two)
        else :
            dif_four_two_list_minus.append(dif_four_two)
            
        print(dif_four_two)
        dif_four_two_list.append(dif_four_two)

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

#f = open('get_1month_stock_data.txt', 'w')

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
#print (title)
#f.write('{}\n'.format(title.encode('utf-8')))

pri_len = len(name)
i = 0

while i < pri_len :
    
    print_ = (u"brand : {:<4}, name : {:->6}, ratio : {:<5}, sales_volume : {:>11}\n".format(brand[i], name[i], ratio[i], sales_vol[i]))
    #print(print_.replace(u"-", u"　").replace(u"±", u"　"))
    #f.write(print_.replace(u"-", u"　").replace(u"±", u"　").encode('utf-8'))
    i += 1

#print(u"銘柄数 : " + str(pri_len))
#f.write(u"銘柄数 : {}\n".format(pri_len).encode('utf-8'))

brand_num = 0
for b_num in brand :
    #try :
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
        #f.write(u"\n")
        #print(name[brand_num])
        #f.write('{}\n'.format(name[brand_num].encode('utf-8')))
        for tmp_table in tr_1mon_table :
            tr_1mon_tbody = tmp_table.find_all("tbody")
            tr_1mon_thead = tmp_table.find_all("thead")
        for tmp_thead in tr_1mon_thead :
            tr_thead = tmp_thead.find_all("th")
        for tmp_tr_thead in tr_thead :
            th_title.append(tmp_tr_thead.string.replace("\r", "").replace("\n", ""))
        #print(u"{0[0]:7}  :  {0[1]}  :  {0[2]}  :  {0[3]}  :  {0[4]}  :  {0[5]}  :  {0[6]}".format(th_title))
        #f.write(u"{0[0]:7}  :  {0[1]}  :  {0[2]}  :  {0[3]}  :  {0[4]}  :  {0[5]}  :  {0[6]}\n".format(th_title).encode('utf-8'))
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
                elif stock_num >= 15 :
                    print((u"{0[3]}".format(td[stock_num])).replace("u", "").replace(',', ''))
                #f.write((u"{0:10} : {1}\n".format(th[stock_num], td[stock_num])).replace("u", "").encode('utf-8'))
                stock_num += 1
            #dif_fourday_twoweekly()
        brand_num += 1
    #except :
        # for debug
        #break

        #pass
#f.close

#print("two_weekly_list\n")
#print('{}\n'.format(two_weekly_list))
#print("dif_four_two_list\n")
#print('{}\n'.format(dif_four_two_list))
#print("dif_four_two_list_plus\n")
#print('{}\n'.format(dif_four_two_list_plus))
#print("dif_four_two_list_minus\n")
#print('{}\n'.format(dif_four_two_list_minus))
#print("dif_four_two_plus_num\n")
#print('{}\n'.format(len(dif_four_two_list_plus)))
#print("dif_four_two_minus_num\n")
#print('{}\n'.format(len(dif_four_two_list_minus)))
