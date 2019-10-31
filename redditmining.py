#This code automatically visualizes the sentiment from a given subreddit about a given subject in a given time period. 
# Any query can be made by adjusting start_epoch and end_epoch with "form int(dt.datetime(YEAR, MONTH, DAY).timestamp())" then 
# typing rungamut('INSERT QUERY WORD', 'INSERT SUBREDDIT')

from psaw import PushshiftAPI
from copy import deepcopy
import pandas as pd
import datetime as dt
from sklearn.utils import shuffle
import nltk
from matplotlib import pyplot as plt
api = PushshiftAPI()
#This is where you can adjust the dates of the query. 
start_epoch=int(dt.datetime(2017, 9, 11).timestamp())
end_epoch=int(dt.datetime(2017, 11, 12).timestamp())


# In[11]:


nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
def sentiment_value(paragraph):
    analyser = SentimentIntensityAnalyzer()
    result = analyser.polarity_scores(paragraph)
    score = result['compound']
    return round(score,1)


# In[12]:


def createperiods(DF):
    DF["time_period"]=(DF["created_utc"]/86400)
    
    DF = DF.astype({"time_period": int})


# In[13]:


def averagetable(DF):
    k = 17420
    X = []
    Y = []
    while k<=17450:
        temp = []
        for i in range(0,len(DF["time_period"])):
            if int(DF["time_period"][i]) == k:
                temp.append(DF['SENTIMENT_VALUE'][i])
        X.append(k)
        Y.append(sum(temp)/len(temp))
        k+=1
    return X,Y


# In[21]:


def createdataframe(DF):
    all_reviews = DF['body']
    all_sent_values = []
    all_sentiments = []
    for i in range(0,len(all_reviews)):
        all_sent_values.append(sentiment_value(all_reviews[i]))
    SENTIMENT_VALUE = []
    SENTIMENT = []
    for i in range(0,len(all_reviews)):
        sent = all_sent_values[i]
        if (sent<=1 and sent>=0.5):
            SENTIMENT.append('V.Positive')
            SENTIMENT_VALUE.append(5)
        elif (sent<0.5 and sent>0):
            SENTIMENT.append('Positive')
            SENTIMENT_VALUE.append(4)
        elif (sent==0):
            SENTIMENT.append('Neutral')
            SENTIMENT_VALUE.append(3)
        elif (sent<0 and sent>=-0.5):
            SENTIMENT.append('Negative')
            SENTIMENT_VALUE.append(2)
        else:
            SENTIMENT.append('V.Negative')
            SENTIMENT_VALUE.append(1)
    DF['SENTIMENT']= SENTIMENT
    DF['SENTIMENT_VALUE']=SENTIMENT_VALUE
def createChart1 (DF, label):
    DF.SENTIMENT.str.split('|', expand=True).stack().value_counts().plot(kind='pie', label=label, figsize=(12,12), autopct='%1.0f%%')
def createChart2(DF, label):    
    createperiods(DF)
    x, y = averagetable(DF)
    plt.plot(x, y, label = label)
    plt.legend(loc="upper left")
    


# In[30]:


def stringreturn(q, r):
    title = q + ' in ' + 'r/' +r
    return title
def rungamut(q, r):
    print('Searching Reddit...')
    work = api.search_comments(q = q, subreddit = r, after= start_epoch, before= end_epoch)
    print('Creating Data Frame...')
    DF = pd.DataFrame([obj.d_ for obj in work])
    print('Generating Chart Label...')
    label = stringreturn(q, r)
    print('Analyzing Data Frame...')
    createdataframe(DF)
    print('Making Charts...')
    createChart1 (DF, label)
    plt.show()
    print('Second Chart...')
    createChart2(DF, label)
    plt.show()


