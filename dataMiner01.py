import inspect
import json
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk
import snscrape.modules.twitter as sntwitter
import networkx as nx

##############################################################
### informações

k="( Eleições OR Lula OR Eleição OR Dilma OR PT OR Bolsonaro )"

maxTweets = 100
years =[2015,2016,2017,2018,2019,2020,2021,2022]

tweets=[]
try:
    for y in years:
        for i,tweet in enumerate(sntwitter, sntwitter.TwitterSearchScraper(
            k + 'since:<year>-01-01 until:<year>-12-31 lang:pt'.replace("<year>", str(y))
        ).get_items()):
            if i > maxTweets:
                break
            theme = k.split("OR")[0].replace('(","')
            username = tweet.username
            text = tweet.content
            pubdate = tweet.date
            permalinks = tweet.url
            outlinks = tweet.outlinks
            tcooutlinks= tweet.tcooutlinks
            tweets.apeend({
                "permalink":permalinks,
                "text":text,
                "username":username,
                "outlinks":outlinks,
                "tcooutlinks":tcooutlinks,
                "date":pubdate,
                "to":tweet.inReplyToUser,
                "likes":tweet.likeCount,
                "replies":tweet.replyCount,
                "retweets":tweet.retweetCount,
                "mentions":tweet.mentionedUsers,
                "theme":k.split("OR")[0].replace('(","')
            })
            scraper = sntwitter.TwitterSearchScraper('fom'+username+'filter:replies')
            for i, tweet in enumerate(scraper.get_items()):
                if i > 10:
                    break
                tweets.append(
                    {
                        "permalink":tweet.url,
                        "text":tweet.content,
                        "username":tweet.username,
                        "outlinks":tweet.outlinks,
                        "tcooutlinks":tweet.tcooutlinks,
                        "date":tweet.date,
                        "to":tweet.inReplyToUser,
                        "likes":tweet.likeCount,
                        "replies":tweet.replyCount,
                        "retweets":tweet.retweetCount,
                        "mentions":tweet.mentionedUsers,
                        "theme": k.split("OR")[0].replace('(","')
                    }
                )
    print("___________________________")
    print("ano: ", y)
    print("tweets Length: ", len(tweets))

except Exception as e:
        print("Private Acconts Error: ", e)

### processamento
final_set = pd.DataFrame(tweets)
final_set['date'] = pd.to_datetime(final_set['date'])
final_set['to'] = final_set['to'].apply(lambda x: str(x).replace("http://twitter.com/",""))
final_set['likes'].fillna(0, inplace=True)

### exportando csv
#final_set.to_csv("./data/elecoes_tweets_br.csv", index=False)

### importando csv
#final_set = pd.read_csv("./data/elecoes_tweets_br.csv")

### exploração simples
for k,v in final_set.sample(5).iterrows():
    print("----------------")
    print("User: ", v['username'])
    print("Date: ", v['date'])
    print("Tweet: ", v['text'])
