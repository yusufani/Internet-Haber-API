import requests
from PIL import Image
from bs4 import BeautifulSoup as bs
import os
import time
OUTPUT_DICT = "Results"
os.makedirs(OUTPUT_DICT,exist_ok =True)
class InternetHaberParser:
    @staticmethod
    def get_image(news_html,category,last_index):

        html_url = news_html.findAll("div", class_="news-detail-featured-img img mb-sm")[0].findAll("a", href=True)[0][
            "href"]
        if len(html_url) <1 :
            return None,None
        try:
            path = os.path.join(OUTPUT_DICT, "images")
            os.makedirs(path, exist_ok=True)
            path = os.path.join(path, category)
            os.makedirs(path, exist_ok=True)
            img = Image.open(requests.get(html_url, stream=True).raw)
            #print(html_url)
            #print(html_url.replace("/", "slash"))
            im_name =os.path.join(path, category+"_"+str(last_index)+".jpg")
            img.save(im_name)
            return im_name,html_url
        except Exception as e:
            print (e)
            return None,None

    @staticmethod
    def get_summary(news_html):
        summary = news_html.findAll("h2", class_="news-detail__description")[0]
        return summary.text

    @staticmethod
    def get_content(news_html):
        data = news_html.find_all("div", class_="content-text")[0]
        content = ""
        for i in data.find_all("p"):
            content += i.text
        return content

    @staticmethod
    def get_date(news_html):
        return news_html.find_all("time")[0]["datetime"]

    @staticmethod
    def get_title(news_html):
        title = news_html.findAll("h1", class_="news-detail__title")[0]
        return title.text
    @staticmethod
    def delete_unnecessary_whitespaces(text):
        return " ".join(text.strip().split())
    @staticmethod
    def parse_html(url,category,last_index):
        try:
            
            print("Parsing html : ",url )
            print("Category of html : ",category)
            # Url içerisindeki html'i indiriyoruz.
            # print(url)
            html = requests.get(url).text
            # print(html)
            soup = bs(html, "html.parser")
            # Belirlediğimiz element'in altındaki bütün p'leri seçiyoruz.
            news_html = soup.findAll("div", class_="news-detail")[0]

            image_path,image_link = InternetHaberParser.get_image(news_html,category,last_index)
            if image_path is not None:

                # image.show()

                date = InternetHaberParser.get_date(news_html)
                #print("Tarih: ",date)
                content = InternetHaberParser.get_content(news_html)
                content = InternetHaberParser.delete_unnecessary_whitespaces(content)
                #print("Content: ",content)

                summary = InternetHaberParser.get_summary(news_html)
                summary = InternetHaberParser.delete_unnecessary_whitespaces(summary)

                print("Summary: ",summary)
                title = InternetHaberParser.get_title(news_html)
                title = InternetHaberParser.delete_unnecessary_whitespaces(title)

                #print("title: ",title)
                print(50*"*")
                return {"title":title, "summary":summary, "content":content, "image_path":image_path, "date":date,"image_link":image_link }
            else:
                return None

        # Link boş ise verilen hata üzerine Boş Data mesajını dönüyor.
        except IndexError as e:
            print(e)
            print("Boş Data")

        # Eğer link haftalık özet ise özet kısmı olmadığından oraya haftalık özet yazıp, sonuçlar o şekilde dönüyor.
        except AttributeError as ae:
            print(ae)
            print("AttributeError")
        except requests.exceptions.RequestException as e: 
            print("Code waiting for block. ")
            time.sleep(120)
            print("Code contuining..")
            return InternetHaberParser.parse_html(url,category)
            
