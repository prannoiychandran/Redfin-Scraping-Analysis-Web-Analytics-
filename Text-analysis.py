import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

df = pd.read_csv (r'D:\2020 fall\BYGB-7978 Web Analytics(R)\project\SoldBuilding.csv')
df['sold_price'] = df['sold_price'].str.replace(',', '')

import warnings
warnings.filterwarnings('ignore')
import re
from nltk.stem import WordNetLemmatizer, PorterStemmer, SnowballStemmer
stop_words_file = 'SmartStoplist.txt'

stop_words = []

with open(stop_words_file, "r") as f:
    for line in f:
        stop_words.extend(line.split()) 
        
stop_words = stop_words  

def preprocess(raw_text):
    
    #regular expression keeping only letters 
    letters_only_text = re.sub("[^a-zA-Z]", " ", str(raw_text))

    # convert to lower case and split into words -> convert string into list ( 'hello world' -> ['hello', 'world'])
    words = letters_only_text.lower().split()

    cleaned_words = []
    lemmatizer = PorterStemmer() 
    
    # remove stopwords
    for word in words:
        if word not in stop_words:
            cleaned_words.append(word)
    
    # stemm or lemmatise words
    stemmed_words = []
    for word in cleaned_words:
        word = lemmatizer.stem(word)   
        stemmed_words.append(word)
    
    # converting list back to string
    return " ".join(stemmed_words)

import nltk
from collections import Counter
frequency=df.building_description.str.split(expand=True).stack().value_counts()
frequency[:40]

from collections import Counter
Counter(" ".join(df["prep"]).split()).most_common(30)

#nice library to produce wordclouds
from wordcloud import WordCloud

import matplotlib.pyplot as plt
# if uising a Jupyter notebook, include:
%matplotlib inline

all_words = '' 

#looping through all incidents and joining them to one text, to extract most common words
for arg in df["prep"]: 

    tokens = arg.split()  
      
    all_words += " ".join(tokens)+" "

wordcloud = WordCloud(width = 700, height = 700, 
                background_color ='white', 
                min_font_size = 10).generate(all_words) 
  
# plot the WordCloud image                        
plt.figure(figsize = (5, 5), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show()

from nltk.util import ngrams
n_gram = 2
n_gram_dic = dict(Counter(ngrams(all_words.split(), n_gram)))

for i in n_gram_dic:
    if n_gram_dic[i] >= 2:
        print(i, n_gram_dic[i])
#Above part is for the description of sold building

from nltk.util import ngrams
n_gram = 2
n_gram_dic = dict(Counter(ngrams(all_words.split(), n_gram)))
onlist={}
freq=[]
for i in n_gram_dic:
    if n_gram_dic[i] >= 2:
        onlist[i] = n_gram_dic[i]
        freq.qppend()
        print(i, n_gram_dic[i])

