# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
#import codecs
import re
#import numpy as np
import pandas as pd

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
            td = tag.find_all("td")
            if td[1].string == u"東証1部" :
                for info_b in td[0] :
                    brand.append(re.match('\d+', info_b.string).group())
                    name.append(re.sub('{}'.format(re.match('\d+', info_b.string).group()), '', info_b.string))
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
    #print (u'{}'.format(title).encode('utf-8'))
    #f.write('{}\n'.format(title.encode('utf-8')))
    
    pri_len = len(brand)
    i = 0
    
    while i < pri_len :
        print_ = (u"{}, {:->25}, start : {:<6}, high : {:<6}, low : {:<6}, finish : {:<6}".format(brand[i], name[i], start[i], high[i], low[i], finish[i]))
        print(print_.replace('-', u'　'))
        #f.write("{}\n".format(brand[i]).encode('utf-8'))
        #f.write('{}\n'.format(print_.replace(u"-", u"　").replace(u"±", u"　").encode('utf-8')))
        i += 1
        
    print(u"銘柄数 : " + str(pri_len))
    #f.write(u"銘柄数 : {}\n".format(pri_len).encode('utf-8'))

def onemonth_stock(year, brand, name, t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m, headers) : 
    # if write out, add element 'f'
    brand_num = 0
    for b_num in brand :
        for _ in range(3) :
            try :
                url_long = "http://kabuoji3.com/stock/%s/%s/" % (b_num, year)
                html_long = requests.get(url_long, headers=headers)
                soup_long = BeautifulSoup(html_long.content, "html.parser")
                tr_long = soup_long.find_all('tr')

                tr_long_thead = None
                tr_long_tbody = []
                th_title = []

                print("")
                #f.write(u"\n")
                print(name[brand_num])
                for tmp_table in tr_long :
                    if tmp_table.find("td") is not None :
                        tr_long_tbody.append(tmp_table.find_all("td"))
                    if tr_long_thead == None :
                        tr_long_thead = (tmp_table.find_all("th"))
                for tmp_tr_thead in tr_long_thead :
                    th_title.append(tmp_tr_thead.string)
                print(u"{0[0]:7}  :  {0[1]}  :  {0[2]}  :  {0[3]}  :  {0[4]}  :  {0[5]}  :  {0[6]}".format(th_title))
                #f.write(u"{0[0]:7}  :  {0[1]}  :  {0[2]}  :  {0[3]}  :  {0[4]}  :  {0[5]}  :  {0[6]}\n".format(th_title).encode('utf-8'))

                td = [[] for i in range(300)]
                stock_num = 0
                
                #f.write('{}\n'.format(name[brand_num].encode('utf-8')))
                for tmp_tbody in tr_long_tbody :
                    for tmp_td in tmp_tbody :
                        td[stock_num].append(tmp_td.string)
                    print((u"{0[0]} : {0[1]:^6} : {0[2]:^6} : {0[3]:^6} : {0[4]:^6} : {0[5]:^8} : {0[6]:^10}".format(td[stock_num])).replace("u", ""))
                    #f.write((u"{0[6]}".format(td[stock_num])).replace("u", "").encode('utf-8'))
                    stock_num += 1

                td = list(filter(lambda none : none != [], td))
                df = pd.DataFrame(td, columns=['date', 'start price', 'highest price', 'cheapest price', 'closing price', 'yield', 'fixed closing price'])
                df.to_csv("/home/gyuho/Git/DeepLearning-stock/stock_data/{0}_tousyou1bu_all/all_stock_data_with_date/all_stock_data_with_date_{1}.csv".format(year, brand[brand_num]))
                t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m = dif_fourday_twoweekly(td, t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m)
                brand_num += 1
                print('brand_num : {}'.format(brand_num))

            except :
                # for debug
                #break
                #continue
                if _ == 2 :
                    brand_num += 1
                pass
            else :
                break
        else :
            continue
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
        print('前日比 : {}'.format(judge_pm))
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

    print('二週足 : {}'.format(two_weekly))
    
    if two_weekly <= 30 :
        two_weekly_list.append(two_weekly)

        dif_four_two  = float(td[-20][4].replace('u', '').replace(',', '')) - float(td[-10][4].replace('u', '').replace(',', ''))

        if dif_four_two >= 0 :
            dif_four_two_list_plus.append(dif_four_two)
        else :
            dif_four_two_list_minus.append(dif_four_two)
            
        print('二週足と四週目の差 : {}'.format(dif_four_two))
        dif_four_two_list.append(dif_four_two)

    return two_weekly_list, dif_four_two_list, dif_four_two_list_plus, dif_four_two_list_minus

def print_two_weekly(t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m) :
    
    print("二週足が30以下のもの\n")
    print('{}\n'.format(t_w_l))
    print("二週足と四週目の差\n")
    print('{}\n'.format(d_f_t_l))
    print("二週足と四週目の差のうち、プラス\n")
    print('{}\n'.format(d_f_t_l_p))
    print("二週足と四週目の差のうち、マイナス\n")
    print('{}\n'.format(d_f_t_l_m))
    print('二週足と四週目の差のうち、プラスの数 : {}\n'.format(len(d_f_t_l_p)))
    print('二週足と四週目の差のうち、マイナスの数 : {}\n'.format(len(d_f_t_l_m)))

def column(matrix, i, j):
    row = []
    for num in matrix :
        row.append([num[i], num[j]])
    return row

    
def main() :
    print('何年のデータがほしい？')
    year = input('>> ')
    tr, title, t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m, headers = import_init()
    #f = open('mothers_stock_number.txt', 'w')
    brand, name, start, high, low, finish = oneday_stock(tr)
    print_brand_stock(title, brand, name, start, high, low, finish) # if write out, add element 'f'
    t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m = onemonth_stock(year, brand, name, t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m, headers) # if write out, add element 'f'
    print_two_weekly(t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m)
    #f.close

if __name__ == '__main__' :
    main()
