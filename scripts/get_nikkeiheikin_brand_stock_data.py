# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import codecs
import re
import numpy as np
import pandas as pd

# for linuxOS
#sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def import_year_all_or_only() :

    while True :
        print('何年のデータがほしい？')
        year = input('>> ')
        print('終値だけ？それとも全部？（終値のみ: 1, 全部: 2）')
        only_or_all = input('>> ')
        if only_or_all == '2' :
            is_all_stock = True
            break
        elif only_or_all == '1' :
            is_all_stock = False
            break
        else :
            print('ちゃんと入力してや')

    return year, is_all_stock

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

def import_nikkei_brandnum() :

    f = open('get_brand_nikkei.txt', 'r')
    brand_text = f.read()
    f.close()

    brand_nikkei = brand_text.split("\n")
    del brand_nikkei[-1]
    print(brand_nikkei)
    return brand_nikkei
    
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
    print (title)
    #f.write('{}\n'.format(title.encode('utf-8')))
    
    pri_len = len(brand)
    i = 0
    
    while i < pri_len :
        print_ = (u"{}, {:->25}, start : {:<6}, high : {:<6}, low : {:<6}, finish : {:<6}".format(brand[i], name[i], start[i], high[i], low[i], finish[i]))
        print(print_.replace('-', u'　'))
        #f.write('{}\n'.format(print_.replace(u"-", u"　").replace(u"±", u"　").encode('utf-8')))
        i += 1
        
    print(u"銘柄数 : " + str(pri_len))
    #f.write(u"銘柄数 : {}\n".format(pri_len).encode('utf-8'))

def onemonth_stock(year, is_all_stock, brand, name, headers, brand_nikkei) : # if write out, add element 'f'
    brand_num = 0
    nikkei_brand_num = 0
    print("{}\n{}\n".format(brand, brand_nikkei))
    for b_num in brand :
        is_already_add_stock = False
        for _ in range(3) :
            try :
                for nikkei in brand_nikkei :
                    if nikkei == b_num :
                        url_long = "http://kabuoji3.com/stock/%s/%s/" % (b_num, year)
                        html_long = requests.get(url_long, headers=headers)
                        soup_long = BeautifulSoup(html_long.content, "html.parser")
                        tr_long = soup_long.find_all('tr')
                        
                        tr_long_thead = None
                        tr_long_tbody = []
                        th_title = []
                        
                        print("")
                        #f.write(u"\n")
                        print(brand[brand_num])
                        print(name[brand_num])
                        #f.write('{}\n'.format(brand[brand_num].encode('utf-8')))
                        #f.write('{}\n'.format(name[brand_num].encode('utf-8')))
                        for tmp_table in tr_long :
                            if tmp_table.find("td") is not None :
                                tr_long_tbody.append(tmp_table.find_all("td"))
                            if tr_long_thead == None :
                                tr_long_thead = (tmp_table.find_all("th"))
                        for tmp_tr_thead in tr_long_thead :
                            th_title.append(tmp_tr_thead.string)
                        #print(u"{0[0]:7}  :  {0[1]}  :  {0[2]}  :  {0[3]}  :  {0[4]}  :  {0[5]}  :  {0[6]}".format(th_title))
                        #f.write(u"{0[0]:7}  :  {0[1]}  :  {0[2]}  :  {0[3]}  :  {0[4]}  :  {0[5]}  :  {0[6]}\n".format(th_title).encode('utf-8'))
                            
                        td = [[] for i in range(300)]
                        stock_num = 0
                        for tmp_tbody in tr_long_tbody :
                            for tmp_td in tmp_tbody :
                                td[stock_num].append(tmp_td.string)
                            #print((u"{0[0]} : {0[1]:^6} : {0[2]:^6} : {0[3]:^6} : {0[4]:^6} : {0[5]:^8} : {0[6]:^10}".format(td[stock_num])).replace("u", ""))
                            #f.write((u"{0[4]}\n".format(td[stock_num])).replace("u", "").encode('utf-8'))
                            stock_num += 1

                        td = list(filter(lambda none : none != [], td))
                        if is_all_stock :
                            df = pd.DataFrame(td, columns=['date', 'start price', 'highest price', 'cheapest price', 'closing price', 'yield', 'fixed closing price'])
                            df.to_csv("../stock_data/adopted_nikkeiheikin/{0}/all_stock_data_with_date/all_stock_data_with_date_{1}.csv".format(year, brand[brand_num]))
                        else :
                            df = pd.DataFrame(column(td, 0, 6), columns=['date', 'closing price'])
                            df.to_csv("../stock_data/adopted_nikkeiheikin/{0}/only_closing_stock_data_with_date/only_closing_stock_data_with_date_{1}.csv".format(year, brand[brand_num]))
                        
                        nikkei_brand_num += 1
                        print('nikkei_brand_num : {}'.format(nikkei_brand_num))

                    else :
                        pass
                else :
                    brand_num += 1
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

def column(matrix, i, j):
    row = []
    for num in matrix :
        row.append([num[i], num[j]])
    return row
    
def main() :
    year, is_all_stock = import_year_all_or_only()
    tr, title, t_w_l, d_f_t_l, d_f_t_l_p, d_f_t_l_m, headers = import_init()
    brand_nikkei = import_nikkei_brandnum()
    #f = open('get_2018_nikkeiheikin_stock_data.txt', 'w')
    brand, name, start, high, low, finish = oneday_stock(tr)
    print_brand_stock(title, brand, name, start, high, low, finish) # if write out, add element 'f'
    onemonth_stock(year, is_all_stock, brand, name, headers, brand_nikkei) # if write out, add element 'f'
    #f.close

if __name__ == '__main__' :
    main()
