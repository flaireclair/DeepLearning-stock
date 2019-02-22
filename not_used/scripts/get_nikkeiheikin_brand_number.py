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
    url = "http://www.nikkei.com/markets/kabu/nidxprice/"
    
    html = requests.get(url)
    
    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html.text, "html.parser")
    tr = soup.find_all("tr")
    
    i = 2
    while i <= 5:
        url_tmp = "https://www.nikkei.com/markets/kabu/nidxprice/?StockIndex=NAVE&Gcode=00&hm=%d" % i
        html_tmp = requests.get(url_tmp)
        soup_tmp = BeautifulSoup(html_tmp.text, "html.parser")
        tr += soup_tmp.find_all("tr")
        i += 1

    return tr

def get_brand_and_name(tr) :
    
    brand = []
    name = []
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
            #break
    return brand, name

def print_brand_number(brand, name, f) :
    i = 0
    for b_num in brand :
        print("brand_num : {0:^5} name : {1}".format(b_num, name[i]))
        f.write('{}\n'.format(b_num))
        i += 1
    print("brand_num : {}".format(len(brand)))
    
def main() :
    tr = import_init()
    f = open('get_brand_nikkei.txt', 'w')
    brand, name = get_brand_and_name(tr)
    print_brand_number(brand, name, f)
    f.close()

if __name__ == '__main__' :
    main()
