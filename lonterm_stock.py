# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import codecs
import re
import numpy as np

# for linuxOS
#sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def import_init() :
    
    # アクセスするURL
    url = "https://kabuoji3.com/stock/"

    headers = {'User-Agent':'Mozilla/5.0'}
    html = requests.get(url, headers=headers)
    
    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html.content, "html.parser")
    tr = soup.find_all("tr")
    
    i = 2
    while i <= 33 :
        url_tmp = "https://kabuoji3.com/stock/?page=%d" % i
        html_tmp = requests.get(url_tmp, headers=headers)
        soup_tmp = BeautifulSoup(html_tmp.content, "html.parser")
        tr += soup_tmp.find_all("tr")
        i += 1
    
    title = soup.title.string

    two_weekly_list = []
    dif_four_two_list = []
    dif_four_two_list_plus = []
    dif_four_two_list_minus = []

    return tr, title, two_weekly_list, dif_four_two_list, dif_four_two_list_plus, dif_four_two_list_minus, headers

def oneday_stock(tr) :
    
    brand = []
    name = []
    start = []
    high = []
    low = []
    finish = []
    for tag in tr :
        try:
            #string_ = tag.get("class").pop(0)
            td = tag.find_all("td")
            if td[1].string == u"東証1部" :
                for info_b in td[0] :
                    brand.append(re.sub('[^0-9]', '', info_b.string))
                    name.append(re.sub('[0-9]', '', info_b.string))
                for info_s in td[2] :
                    start.append(info_s.string)
                for info_h in td[3] :
                    high.append(info_h.string)
                for info_l in td[4] :
                    low.append(info_l.string)
                for info_f in td[5] :
                    finish.append(info_f.string)
        except :
            continue
            #break
    return brand, name, start, high, low, finish

def print_brand_stock(title, brand, name, start, high, low, finish) :
    # if write out, add element 'f'
    # タイトルを文字列を出力
    print (title)
    #f.write('{}\n'.format(title.encode('utf-8')))
    
    pri_len = len(brand)
    i = 0
    
    while i < pri_len :
        print_ = (u"brand : {}, name : {:->25}, start : {:<6}, high : {:<6}, low : {:<6}, finish : {:<6}".format(brand[i], name[i], start[i], high[i], low[i], finish[i]))
        print(print_.replace('-', u'　'))
        #f.write('{}\n'.format(print_.replace(u"-", u"　").replace(u"±", u"　").encode('utf-8')))
        i += 1
        
    print(u"銘柄数 : " + str(pri_len))
    #f.write(u"銘柄数 : {}\n".format(pri_len).encode('utf-8'))

def onemonth_stock(brand, name, t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m, headers) : 
    # if write out, add element 'f'
    brand_num = 0
    for b_num in brand :
        #try :
            url_long = "https://kabuoji3.com/stock/%s/" % b_num
            html_long = requests.get(url_long, headers=headers)
            soup_long = BeautifulSoup(html_long.content, "html.parser")
            tr_long = soup_long.find_all("tr")
            tr_thead = []
            tr_long_tbody = []
            tr_long_thead = []
            th_title = []
            th_with_days = []
            td = [[] for i in range(25)]
            stock_num = 0
            print("")
            #f.write(u"\n")
            print(name[brand_num])
            #f.write('{}\n'.format(name[brand_num].encode('utf-8')))
            for tmp_table in tr_long_table :
                tr_long_tbody.append(tmp_table.find_all("tbody"))
                tr_long_thead.append(tmp_table.find("thead"))
            print(tr_long_tbody)
            for tmp_thead in tr_long_thead :
                tr_thead.append(tmp_thead.find_all("th"))
            for tmp_tr_thead in tr_thead :
                for tmp_tmp_tr_thead in tmp_tr_thead :
                    th_title.append(tmp_tmp_tr_thead.string)
            print(u"{0[0]:7}  :  {0[1]}  :  {0[2]}  :  {0[3]}  :  {0[4]}  :  {0[5]}  :  {0[6]}".format(th_title))
            #f.write(u"{0[0]:7}  :  {0[1]}  :  {0[2]}  :  {0[3]}  :  {0[4]}  :  {0[5]}  :  {0[6]}\n".format(th_title).encode('utf-8'))
            print(tr_long_tbody)
            for tmp_tbody in tr_long_tbody :
                for tmp_tmp_tbody in tmp_tbody :
                    tr_long.append(tmp_tmp_tbody.find_all("tr"))
                for tmp_tr_list in tr_long :
                    for tmp_tr in tmp_tr_list :
                        td_long = (tmp_tr.find_all("td"))
                        print(td_long)
                        for tmp_td in td_long :
                            td[stock_num].append(tmp_td.string)
                    print((u"{0[0]} : {0[1]:^6} : {0[2]:^6} : {0[3]:^6} : {0[4]:^6} : {0[5]:^8} : {0[6]:^10}".format(td[stock_num])).replace("u", ""))
                    #f.write((u"{0:10} : {1}\n".format(th[stock_num], td[stock_num])).replace("u", "").encode('utf-8'))
                    stock_num += 1
            t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m = dif_fourday_twoweekly(td, t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m)
            brand_num += 1
        #except :
            # for debug
            #break
            
            #pass
    return t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m

def dif_fourday_twoweekly(td, two_weekly_list, dif_four_two_list, dif_four_two_list_plus, dif_four_two_list_minus) :

    tmp_weekly = None
    two_weekly_plus = []
    two_weekly_minus = []
    i = 0
    
    for tmp_2week in td[::-1] :
        if i == 10 :
            break
        i += 1
        if tmp_weekly == None :
            tmp_weekly = float(tmp_2week[4])
            continue
        tmp_2week_float = float(tmp_2week[4])
        judge_pm = tmp_2week_float - tmp_weekly
        tmp_weekly = tmp_2week_float
        print(judge_pm)
        if judge_pm >= 0 :
            two_weekly_plus.append(judge_pm)
        else :
            two_weekly_minus.append(judge_pm)

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

    if plus_sum == None :
        plus_sum = 0
    if minus_sum == None :
        minus_sum = 0
    
    two_weekly = float((plus_sum / (plus_sum + (minus_sum * -1))) * 100)

    print(two_weekly)
    
    if two_weekly <= 30 :
        two_weekly_list.append(two_weekly)

        dif_four_two  = float(td[5][4].replace('u', '').replace(',', '')) - float(td[15][4].replace('u', '').replace(',', ''))

        if dif_four_two >= 0 :
            dif_four_two_list_plus.append(dif_four_two)
        else :
            dif_four_two_list_minus.append(dif_four_two)
            
        print(dif_four_two)
        dif_four_two_list.append(dif_four_two)

    return two_weekly_list, dif_four_two_list, dif_four_two_list_plus, dif_four_two_list_minus

def print_two_weekly(t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m) :
    
    print("two_weekly_list\n")
    print('{}\n'.format(t_w_l))
    print("dif_four_two_list\n")
    print('{}\n'.format(d_f_t_l))
    print("dif_four_two_list_plus\n")
    print('{}\n'.format(d_f_t_l_p))
    print("dif_four_two_list_minus\n")
    print('{}\n'.format(d_f_t_l_m))
    print('dif_four_two_plus_num : {}\n'.format(len(d_f_t_l_p)))
    print('dif_four_two_minus_num : {}\n'.format(len(d_f_t_l_m)))

def main() :
    tr, title, t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m, headers = import_init()
    #f = open('get_1month_stock_data.csv', 'w')
    brand, name, start, high, low, finish = oneday_stock(tr)
    print_brand_stock(title, brand, name, start, high, low, finish) # if write out, add element 'f'
    t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m = onemonth_stock(brand, name, t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m, headers) # if write out, add element 'f'
    print_two_weekly(t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m)
    #f.close

if __name__ == '__main__' :
    main()
