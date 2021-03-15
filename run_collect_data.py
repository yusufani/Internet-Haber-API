#!/usr/bin/env python
# coding: utf-8

# In[2]:
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from InternetHaberParser import *
import requests
import csv
from multiprocessing import Process
import multiprocessing
import glob

CONTINUE_FROM_PAGE_INDEXES = True
OUTPUT_DICT = "Results"
SAVE_AFTER_PAGE = 100  # 1 page consist of 14 news
os.makedirs(OUTPUT_DICT, exist_ok=True)

sections = [
    "https://www.internethaber.com/saglik",
    "https://www.internethaber.com/magazin",
    "https://www.internethaber.com/spor",
    "https://www.internethaber.com/ekonomi",
    "https://www.internethaber.com/politika",
    "https://www.internethaber.com/egitim",
    "https://www.internethaber.com/bilim-teknoloji",
    "https://www.internethaber.com/dunya",
]


# %%
# In[7]:


def check_file(tags, category):
    if tags is None:
        print(10 * "\n*")
        print(10 * ("WARNING can not detect a news in the page . Finishing category ", category, "\n"))
        print(10 * "\n*")
        return False
    return True


def get_news_urls(page_url, news_urls, category):
    try:
        # Url'nin içerisindeki bütün html dosyasını indiriyoruz.
        html = requests.get(page_url).text
        soup = bs(html, "lxml")

        if category == "egitim":
            class_name_for_news = "col-12 col-lg mw0 category-wrapper"
            class_name_for_each_new = "news-list left-image left-image-big mb-md"
            tags = soup.find("div", class_=class_name_for_news)
            if check_file(tags, category):
                tags = tags.find_all("div", class_=class_name_for_each_new)
                for div in tags:
                    news_urls.append(div.find("a", href=True)["href"])
            else:
                return False, news_urls
        else:
            class_name_for_news = "col-md-8 order-1 order-md-2"
            class_name_for_each_new = "news-list left-image mb-md"
            tags = soup.find("div", class_=class_name_for_news)
            if check_file(tags, category):
                for a in tags.find_all('a', href=True, class_=class_name_for_each_new):
                    print(a["href"])
                    news_urls.append(a['href'])
            else:
                return False, news_urls
        return True, news_urls
    except IndexError as ie:
        print("Böyle bir sayfa yok.", ie)
        return False, news_urls
    except Exception as e:
        print(e)
        return False, news_urls

def get_last_image_index(category):
    folder = os.path.join(OUTPUT_DICT,"images")
    folder = os.path.join(folder,category)
    if os.path.exists(folder):
        min_i = 0 
        for i in os.listdir(folder):
            index = int(i.replace(".","_").split("_")[1])
            if min_i < index:
                min_i = index
        return min_i
    else:
        return 1





def parse_data_from_news(urls, category):
    urls = list(set(urls))  # If any duplicates
    print("Number of urls will parsed : ", len(urls))

    last_index = get_last_image_index(category) +1

    output = []
    for idx, val in enumerate(urls):
        if (idx + 1) % 500 == 0:
            print("Code waiting for query limit... ")
            time.sleep(45)
            print("Code counting...")
        print("News Count : ", idx + 1, "/", len(urls))
        fields = InternetHaberParser.parse_html(val, category,last_index)
        if fields is not None:
            last_index+=1
            fields["category"] = category
            fields["link"] = val
            output.append(fields)

    keys = output[0].keys()
    filename = os.path.join(OUTPUT_DICT, "result_" + output[0]["category"] + ".csv")
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='',
              encoding='utf-8')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys, delimiter="\t", quoting=csv.QUOTE_ALL)
        if not file_exists:
            dict_writer.writeheader()
        dict_writer.writerows(output)


def get_category(section):
    return section.split("/")[-1]


def main(section, page_idx=0, news_urls=[]):
    category = get_category(section)
    continue_parsing = True
    try:
        while continue_parsing:
            page_url = section + "?page={}".format(page_idx)
            print("News taken from page : ", page_url)
            continue_parsing, news_urls = get_news_urls(page_url, news_urls, category)
            if len(news_urls) == 0:
                print("WARNING : NOT FOUND ANY NEWS")
            elif page_idx % SAVE_AFTER_PAGE == 0 or not continue_parsing:  # Save news
                print(
                    f"Collected {str(SAVE_AFTER_PAGE)} pages and {str(len(news_urls))} news urls Category= {category}. Parsing news ...")
                parse_data_from_news(news_urls, category)
                news_urls = []
                print(f"{str(SAVE_AFTER_PAGE)} pages and {str(len(news_urls))}  news parsed. Continuing collecting news ...")
            page_idx += 1
    except requests.exceptions.RequestException as e:
        print("Code waiting for block. ")
        time.sleep(120)
        print("Code contuining..")
        main(section, page_idx - 1, news_urls)


def read_index_of_output_files(path):
    indexes = {}

    for file in glob.glob(os.path.join(path, "*.csv")):
        category_name = file.split(os.sep)[-1].replace(".", "_").split("_")[1]
        df = pd.read_csv(file, encoding="utf-8", sep="\t").drop_duplicates()
        number_of_news_each_page = 14
        if category_name == "egitim":
            number_of_news_each_page = 20
        indexes[category_name] = int(len(df) / number_of_news_each_page) + 1
    return indexes


if __name__ == '__main__':


    if CONTINUE_FROM_PAGE_INDEXES:
        print("Continuing from old page indexes. Calculating indexes ...")
        # If code encounter any problem you can continue from page indexes.Do not forget the set CONTUINE variable
        indexes = read_index_of_output_files(OUTPUT_DICT)
        print(indexes)

    processes = []
    for section in sections:
        print('registering process %s' % section)
        if CONTINUE_FROM_PAGE_INDEXES:
            processes.append(Process(target=main, args=(section, indexes[get_category(section)])))
        else:
            processes.append(Process(target=main, args=(section,)))
    for process in processes:
        process.start()
    for process in processes:
        process.join()
