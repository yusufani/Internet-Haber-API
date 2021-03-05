#!/usr/bin/env python
# coding: utf-8

# In[2]:
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from InternetHaberParser import *
import requests
import csv
OUTPUT_DICT = "Results"
os.makedirs(OUTPUT_DICT,exist_ok =True)

sections = [
            "https://www.internethaber.com/dunya",
            "https://www.internethaber.com/spor",
            "https://www.internethaber.com/ekonomi",
            "https://www.internethaber.com/saglik",
            "https://www.internethaber.com/magazin",
            "https://www.internethaber.com/politika",
            "https://www.internethaber.com/egitim",
            "https://www.internethaber.com/bilim-teknoloji"
            ]
sections = [
            "https://www.internethaber.com/egitim",
            "https://www.internethaber.com/bilim-teknoloji"
            ]

# %%
# In[7]:



for section in sections:
    urls = []
    category = section.split("/")[-1]
    for i in range(1, 90):
        try:
            newurl = section + "?page={}".format(i)
            print("News taken from page : ", newurl)

            # Url'nin içerisindeki bütün html dosyasını indiriyoruz.
            html = requests.get(newurl).text
            soup = bs(html, "lxml")

            # Yukarıdaki şemadada görüldüğü gibi bütün makaleler bu element'in içerisinde yer alıyor.
            # Bizde bütün makaleleri buradan tags adında bir değişkene topluyoruz.
            class_name_for_news = "col-md-8 order-1 order-md-2"
            class_name_for_each_new = "news-list left-image mb-md"
            if category == "egitim":
                class_name_for_news = "col-12 col-lg mw0 category-wrapper"
                class_name_for_each_new  = "news-list left-image left-image-big mb-md"
                tags = soup.find("div", class_=class_name_for_news).find_all("div",class_=class_name_for_each_new)
                for div in tags:
                    urls.append(div.find("a",href=True)["href"])
            else:
                tags = soup.find("div", class_=class_name_for_news)

                # Sırayla bütün makalelere girip, href'in içerisindeki linki urls adlı listemize append ediyoruz.
                for a in tags.find_all('a', href=True, class_=class_name_for_each_new):
                    print(a["href"])
                    urls.append(a['href'])
            
            #print(urls)
        except IndexError as ie:
            print("Böyle bir sayfa yok.", ie)
        except Exception as e:
            print(e)

    urls = list(set(urls))
    bigdata = []

    for idx, val in enumerate(urls):
        if (idx+1)%50 == 0:
            print("Code waiting for query limit... ")
            time.sleep(75)
            print("Code counting...")
        print("News Count : ", idx+1)
        fields = InternetHaberParser.parse_html(val,category)
        if fields is not None:
            fields["category"] = category
            fields["link"] = val
            bigdata.append(fields)

    # %%

    keys = bigdata[0].keys()
    with open(os.path.join(OUTPUT_DICT, "result_" + bigdata[0]["category"] + ".csv"), 'w', newline='',
              encoding='utf-8')   as output_file:
        dict_writer = csv.DictWriter(output_file, keys, delimiter="~", quoting=csv.QUOTE_ALL)
        dict_writer.writeheader()
        dict_writer.writerows(bigdata)