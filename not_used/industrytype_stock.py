# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import codecs
import re
import numpy as np

# for linuxOS
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def import_init() :

    url = "https://www.nikkei.com/markets/kabu/nidxprice/"

    html = requests.get(url)

    soup = BeautifulSoup(html.content, "html.parser")
    find_heat_map_container = soup.find("div", attrs={"class":"highcharts-container"})
    find_heat_map = find_heat_map_container.find("div", attrs={"id":"highcharts-0"})

    i = 0
    while i <=35 :
        find_heat_map_industry = find_heat_map.find("div", attrs={"industriesprofileindex":"{}".format(i)})
        print(find_heat_map_industry.string)
        i += 1
    
def main() :
    import_init()
    
if __name__ == "__main__" :
    main()
