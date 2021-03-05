
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from glob import glob
import nltk
from nltk.tokenize import word_tokenize

DATA_PATH = "Results"
OUTPATH = os.path.join(DATA_PATH ,"graphs")
os.makedirs(OUTPATH,exist_ok =True)

nltk.download('stopwords')
from nltk.corpus import stopwords
stopWords = set(stopwords.words('turkish'))
print(stopWords)
print(type(stopWords))
def generate_wordcloud(text,column,filename):
    # Generate a word cloud image
    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    # the matplotlib way:

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(os.path.join(OUTPATH,filename + '_' + column + "_zoom_in.png"))
    

    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(os.path.join(OUTPATH,filename + '_' + column + "_zoom_out.png"))
    plt.clf()

    #plt.show(


def remove_stop_words(text):
    words = word_tokenize(text)
    #print(words)
    #print(type(words))
    wordsFiltered = []
    for w in words:
        if w not in stopWords:
            wordsFiltered.append(w)
    #wordsFiltered = [w for w in words if w not in stopwords]
    return " ".join(wordsFiltered)

def get_result_by_column(column,column_name,filename):
    text = ""
    for idx, val in column.iteritems():
        text += val

    text = remove_stop_words(text)
    generate_wordcloud(text,column_name,filename)


for csv_file in glob(DATA_PATH+os.sep+"*.csv"):
    print(csv_file)
    data = pd.read_csv(csv_file,encoding="utf-8", sep="~")
    get_result_by_column(data["title"],"title",csv_file.replace(".","_").split("_")[-2])
    get_result_by_column(data["summary"],"summary",csv_file.replace(".","_").split("_")[-2])
    get_result_by_column(data["content"],"content",csv_file.replace(".","_").split("_")[-2])

# %%
