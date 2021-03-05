import requests
from PIL import Image
from bs4 import BeautifulSoup as bs
import os
OUTPUT_DICT = "Results"
os.makedirs(OUTPUT_DICT,exist_ok =True)
class InternetHaberParser:

    @staticmethod
    def get_image(news_html,category):

        html_url = news_html.findAll("div", class_="news-detail-featured-img img mb-sm")[0].findAll("a", href=True)[0][
            "href"]
        if len(html_url) <1 :
            return None
        try:

            path = os.path.join(OUTPUT_DICT, "images")
            os.makedirs(path, exist_ok=True)
            path = os.path.join(path, category)
            os.makedirs(path, exist_ok=True)
            img = Image.open(requests.get(html_url, stream=True).raw)
            #print(html_url)
            #print(html_url.replace("/", "slash"))
            img.save(os.path.join(path, html_url.replace("/", "_slash_").replace(":", "_ikinokta_")))
            return os.path.join(path, html_url)
        except Exception as e:
            print (e)
            return None

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
    def parse_html(url,category):
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

            image_path = InternetHaberParser.get_image(news_html,category)
            if image_path is not None:

                # image.show()

                date = InternetHaberParser.get_date(news_html)
                print("Tarih: ",date)
                content = InternetHaberParser.get_content(news_html)
                #print("Content: ",content)

                summary = InternetHaberParser.get_summary(news_html)
                print("Summary: ",summary)
                title = InternetHaberParser.get_title(news_html)
                print("title: ",title)
                print(50*"*")
                return {"title":title, "summary":summary, "content":content, "image_path":image_path, "date":date }
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
