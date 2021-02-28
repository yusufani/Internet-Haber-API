#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import datetime
from progressbar import *
from IPython.display import clear_output


# # Makalelerin Linklerinin Çekilmesi

# In[6]:


sections = ["https://www.internethaber.com/spor",
            "https://www.internethaber.com/ekonomi",
            "https://www.internethaber.com/dunya",
            "https://www.internethaber.com/saglik",
            "https://www.internethaber.com/magazin",
            "https://www.internethaber.com/politika",
            "https://www.internethaber.com/egitim",
            "https://www.internethaber.com/saglik",
            "https://www.internethaber.com/kultur-ve-sanat",
            "https://www.internethaber.com/bilim-teknoloji"
           ]

#%%
sections = ["https://www.internethaber.com/spor"]
# In[7]:


urls = []
#Öncelikle bir Kategori seçiyoruz.
for section in sections:
    #Kategorinin içerisinde sırayla 100 sayfa gezineceğiz.
    for i in range(1,2):
        try:
            #Öncelikle URL'imizi oluşturuyoruz. Örneğin;
            #https://www.dunyahalleri.com/category/kultur-sanat/page/25
            newurl = section+"?page={}".format(i)
            print("News taken from page : " , newurl)

            #Url'nin içerisindeki bütün html dosyasını indiriyoruz.
            html = requests.get(newurl).text
            soup = bs(html, "lxml")

            #Yukarıdaki şemadada görüldüğü gibi bütün makaleler bu element'in içerisinde yer alıyor.
            #Bizde bütün makaleleri buradan tags adında bir değişkene topluyoruz.
            tags = soup.findAll("div", class_="col-md-8 order-1 order-md-2")[0]

            #Sırayla bütün makalelere girip, href'in içerisindeki linki urls adlı listemize append ediyoruz.
            for a in tags.find_all('a', href=True,class_="news-list left-image mb-md"):
                print(a["href"])
                urls.append((section.split("/")[-1],a['href']))
        except IndexError as ie:
            print("Böyle bir sayfa yok.",ie)
            break
        except Exception as e :
            print(e.message)


# In[5]:


urldata = pd.DataFrame(urls)
urldata.columns = ["Category","Link"]
urldata.head()


# In[7]:


urldata = urldata.drop_duplicates()


# In[8]:


urldata.to_csv('urldata.csv')


# # Linklerdeki Verilerin Çekilmesi

# In[68]:


def get_image(news_html):
    html_url = news_html.findAll("div",class_="news-detail-featured-img img mb-sm")[0].findAll("a",href=True)[0]["href"]

    print(html_url)

    print("Image url " , html_url)


def get_title(news_html):
    pass


def GetData(url):
    try:
        #Url içerisindeki html'i indiriyoruz.
        #print(url)
        html = requests.get(url).text
        #print(html)
        soup = bs(html, "html.parser")

        #Belirlediğimiz element'in altındaki bütün p'leri seçiyoruz.
        news_html = soup.findAll("div", class_="news-detail")[0]

        image = get_image(news_html)
        title = get_title(news_html)
        content = get_content(news_html)
        date = get_date(news_html)
        summary = get_summary(news_html)


        '''
        #Body_text adındaki metni tek bir string üzerinde topluyoruz.
        body_text_big = ""
        for i in body_text:
            body_text_big = body_text_big +i.text

        #Başlığı ve zamanı'da element isimlerinden bu şekilde seçip, metinlerini alıyoruz.
        header = soup.find("h1", class_="entry-title h1").text
        timestamp = soup.find("span", class_="updated").text
        
        #Özetin bulunduğu element'in metin kısmını alıyoruz.
        summarized = soup.find("div", class_="tldr-sumamry").text
        return ((url,header,body_text_big,summarized,timestamp))
        '''
    #Link boş ise verilen hata üzerine Boş Data mesajını dönüyor.
    except IndexError:
        return ("Boş Data")

    #Eğer link haftalık özet ise özet kısmı olmadığından oraya haftalık özet yazıp, sonuçlar o şekilde dönüyor.
    except AttributeError:
        print("AttributeError")
        return ((url,header,body_text_big,"Haftalık Özet",timestamp))


# In[73]:

bigdata = []
for idx,link in enumerate(urldata.Link):
    #clear_output(wait=True)
    print("News Count : ",idx)
    bigdata.append(GetData(link))

# In[109]:


bigdatax = pd.DataFrame(bigdata)
bigdatax.drop([5,6,7],axis=1,inplace=True)
bigdatax.drop(bigdatax[bigdatax[0]=="B"].index,axis=0,inplace=True)
bigdatax.columns = ["Link","Başlık","Body_text","Summarized_Text","TimeStamp"]
bigdatax = bigdatax.loc[bigdatax.Link.drop_duplicates().index]
bigdatax.index = range(0,len(bigdatax))
bigdatax.head()


# In[108]:


def Düzeltici(x):
    if x[:20] == "Haber ÖzetiTam Sürüm":
        return x[20:]
    else:
        return x


# In[110]:


bigdatax.Body_text = bigdatax.Body_text.apply(Düzeltici)


# In[120]:


droplist =[]
for i in range(0,len(bigdatax)):
    if bigdatax.loc[i].Body_text[:35] == 'Türkiye ve dünyadan güncel haberler':
        droplist.append(i)
    else:
        continue


# In[124]:


bigdatax.drop(droplist,axis=0,inplace=True)


# In[127]:


bigdatax.to_excel("DunyaHalleri.xlsx", encoding="utf-16")


# In[ ]:




