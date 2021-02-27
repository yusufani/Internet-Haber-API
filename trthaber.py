'''
Example Queries for trt haber : https://github.com/prosman/TRT-Haber-Api
http://www.trthaber.com/xml_mobile.php?tur=xml_genel&selectEx=okunmaadedi,yorumSay&id=HABERID_BURAYA_GELECEK&commentList=show
http://www.trthaber.com/xml_mobile.php?tur=xml_genel&selectEx=okunmaadedi,yorumSay&id=HABERID_BURAYA_GELECEK&commentList=show
### HABER LİSTELERİ
Ana Sayfa Manşet
http://www.trthaber.com/xml_mobile.php?tur=xml_genel&kategori=&adet=20&selectEx=yorumSay,okunmaadedi,anasayfamanset,kategorimanset
Son Dakika Haberleri
http://www.trthaber.com/xml_mobile.php?tur=xml_genel&kategori=sondakika&adet=20&selectEx=yorumSay,okunmaadedi,anasayfamanset,kategorimanset
Spor Haberleri
http://www.trthaber.com/xml_mobile.php?tur=xml_genel&kategori=spor&adet=20&selectEx=yorumSay,okunmaadedi,anasayfamanset,kategorimanset
Gündem Haberleri
http://www.trthaber.com/xml_mobile.php?tur=xml_genel&kategori=gundem&adet=20&selectEx=yorumSay,okunmaadedi,anasayfamanset,kategorimanset
Ekonomi Haberleri
http://www.trthaber.com/xml_mobile.php?tur=xml_genel&kategori=ekonomi&adet=20&selectEx=yorumSay,okunmaadedi,anasayfamanset,kategorimanset
Dünya Haberleri
http://www.trthaber.com/xml_mobile.php?tur=xml_genel&kategori=dunya&adet=20&selectEx=yorumSay,okunmaadedi,anasayfamanset,kategorimanset
Sağlık Haberleri
http://www.trthaber.com/xml_mobile.php?tur=xml_genel&kategori=saglik&adet=20&selectEx=yorumSay,okunmaadedi,anasayfamanset,kategorimanset
Yaşam Haberleri
http://www.trthaber.com/xml_mobile.php?tur=xml_genel&kategori=yasam&adet=20&selectEx=yorumSay,okunmaadedi,anasayfamanset,kategorimanset
Spor Haberleri
http://www.trthaber.com/xml_mobile.php?tur=xml_genel&kategori=spor&adet=20&selectEx=yorumSay,okunmaadedi,anasayfamanset,kategorimanset
Kültür Sanat Haberleri
http://www.trthaber.com/xml_mobile.php?tur=xml_genel&kategori=kultur-sanat&adet=20&selectEx=yorumSay,okunmaadedi,anasayfamanset,kategorimanset
Eğitim Haberleri
http://www.trthaber.com/xml_mobile.php?tur=xml_genel&kategori=egitim&adet=20&selectEx=yorumSay,okunmaadedi,anasayfamanset,kategorimanset
Türkiye Haberleri
http://www.trthaber.com/xml_mobile.php?tur=xml_genel&kategori=turkiye&adet=20&selectEx=yorumSay,okunmaadedi,anasayfamanset,kategorimanset
'''
# %%

import requests


# %%
class TrtAPI:
    def __init__(self):
        self.arguments = {"comment_count": "yorumSay", "read_count": "okunmaadedi", "headline_count": "anasayfamanset",
                          "category_headline": "kategorimanset"}

    def make_query(self, category, news_count=20, arguments=None):

        query = "http://www.trthaber.com/xml_mobile.php?tur=xml_genel&kategori={}&adet={}&selectEx=".format(category,
                                                                                                            news_count)
        if arguments is None:
            args = self.arguments.values()
        else:
            args = [self.arguments[key] for key in arguments]
        query += ",".join(args)
        return requests.get(query).text


# %%
from xml.dom import minidom

'''
  <haber>
        		<haber_manset><![CDATA[Başkentte 326 eğitim tesisi açılacak]]></haber_manset>
        		<haber_resim>https://trthaberstatic.cdn.wp.trt.com.tr/resimler/1474000/cocuk-kitap-1475375.jpg</haber_resim>
                <haber_link>haber/gundem/baskentte-326-egitim-tesisi-acilacak-558731.html</haber_link>
        		<haber_id>558731</haber_id>
        		<haber_video></haber_video>
        		<haber_aciklama><![CDATA[Ankara Valisi Vasip Şahin, 326 eğitim tesisi açılışının yapılacağını duyurdu.]]></haber_aciklama>
        		<haber_metni><![CDATA[<p>
	<a href="https://www.trthaber.com/etiket/ankara/" target="_blank">Ankara</a> Valisi Vasip Şahin, sosyal meyda hesabından başkentte açılacak eğitim tesisleriyle ilgili paylaşım yaptı.</p>
<p>
	Vali Şahin, 2019-2020 yıllarında yapımı tamamlanan eğitim tesislerinin saat 13.00'te açılışının yapılacağını açıkladı.</p>
<p>
	Vasip Şahin, paylaşımında, "Sayın Cumhurbaşkanımız tarafından, video konferans yöntemiyle üç ayrı noktadaki okullarımıza bağlanarak toplu açılışları yapılacak olan 326 eğitim tesisi Ankara’ya hayırlı olsun" sözlerine yer verdi. </p>
<p>
	 </p>
<blockquote class="twitter-tweet">
	<p dir="ltr" lang="tr">
		Sayın Cumhurbaşkanımız tarafından, video konferans yöntemiyle üç ayrı noktadaki okullarımıza bağlanarak toplu açılışları yapılacak olan 326 eğitim tesisi Ankara’ya hayırlı olsun. <a href="https://t.co/aeisvSQnwI">https://t.co/aeisvSQnwI</a></p>
	— Vasip Şahin (@vasipsahin) <a href="https://twitter.com/vasipsahin/status/1363965548204339201?ref_src=twsrc%5Etfw">February 22, 2021</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script><p>
	 </p>
<p>
	Açılacak eğitim tesislerinin arasında anaokulu, ilkokul, ortaokul, atölye, spor salonu, bilim ve sanat merkezi, güzel sanatlar lisesi de bulunuyor.</p>
]]></haber_metni>
        		<haber_kategorisi>Eğitim</haber_kategorisi>
        		<haber_tarihi>Tue, 2021-02-23 01:26:00</haber_tarihi>
                <manset_resim>https://trthaberstatic.cdn.wp.trt.com.tr/resimler/1474000/cocuk-kitap-1475375.jpg</manset_resim>
                <izles_id></izles_id>   
                <yorumSay><![CDATA[0]]></yorumSay><okunmaadedi><![CDATA[0]]></okunmaadedi><anasayfamanset><![CDATA[0]]></anasayfamanset><kategorimanset><![CDATA[1]]></kategorimanset>     
                    
        	</haber>

'''
class Parser:
    @staticmethod
    def parse(query):
        xmldoc = minidom.parseString(query)
        itemlist = xmldoc.getElementsByTagName('haber')
        print("Number of news taken : ", len(itemlist))
        for haber in itemlist:
            headline = Parser.get_news_headline(haber)
            print(headline)
    @staticmethod
    def get_news_headline(data):
        headline = data.getElementsByTagName('haber_manset')[0].firstChild.nodeValue
        return headline
    @staticmethod
    def get_news_image(data):
        pass
    @staticmethod
    def get_news_link(data):
        "https: // www.trthaber.com /"
        pass
    @staticmethod
    def get_news_id(data):
        pass
    @staticmethod
    def get_news_summary(data):
        pass
    @staticmethod
    def get_news_content(data):
        pass
    @staticmethod
    def get_news_blockquote(data):
        pass

# %%
api = TrtAPI()
query = api.make_query("egitim")

Parser.parse(query)


# %%
class News:
    def __init__(self):
        pass
