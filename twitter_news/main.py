# Python program to get top 3 trendy news item
# courtesy geeksforgeeks


import tweepy
import json
from datetime import date, timedelta, datetime
from pymongo import MongoClient
from html.parser import HTMLParser
import re
from pyshorteners import Shortener

NewsArrayIndex = 0
NewsArray = [None] * 3


class MyHTMLParser(HTMLParser):

    # This function collects the value
    # of href and stores in NewsArrayIndex
    # variable
    def handle_starttag(self, tag, attrs):

        # Only parse the 'anchor' tag.
        global NewsArrayIndex
        if tag == "a":

            # Check the list of defined attributes.
            for name, value in attrs:

                # If href is defined, print it.
                if name == "href":
                    # print(value + "\t" + News1)
                    NewsArray[NewsArrayIndex] = value

                    # print(NewsArray)
                    NewsArrayIndex += 1


# This function is the primary place
# to tweet the collected daily news
# News is retrieved from Coll_DailyNewsPlusReview
# collection (MongoDB collection) This collection
# holds the value of " News Headlines, Its review
# count, news link" and based upon the review count,
# top most # reviewed news are taken As twitter allows
# only 280 characters, the retrieved news link got
# shortened by using BITLY API Hashtags related to
# the news are added underneath the retrieved top
# 3 news (All together allowed characters are 280)
# Then top 3 news gets tweeted from a credential
# Finally per day basis the tweeted news are stored
# into another collection for audit purposes as well
# as for weekly posting
def tweetDailyNews():
    try:

        # This is the collection name in mongodb
        cursor_P = db1.Coll_DailyNewsPlusReview.find({"time": date_str})

        p0 = cursor_P[0]
        News = p0.get('News')
        sortedNews = sorted(News, key=lambda x: int(x[1]), reverse=True)
        print(sortedNews[0][0] + "--" + sortedNews[0][1],
              sortedNews[1][0] + ".." + sortedNews[1][1],
              sortedNews[2][0] + ".." + sortedNews[2][1])

        hyperlink_format = '<a href ="{link}">{text}</a>'
        parser = MyHTMLParser()
        dailyNews = "Impactful News of the Day" + "\n"

        News0 = sortedNews[0][2]
        parser.feed(hyperlink_format.format(link=News0, text=News0))

        News1 = sortedNews[1][2]
        print("News1", News1)
        parser.feed(hyperlink_format.format(link=News1, text=News1))

        News2 = sortedNews[2][2]
        print(News2)
        parser.feed(hyperlink_format.format(link=News2, text=News2))

        # News shortening pattern
        BITLY_ACCESS_TOKEN = "20dab258cc44c7d017bcd1c1f4b24484a37b8de9"
        b = Shortener(api_key=ACCESS_TOKEN)

        NewsArray[0] = re.sub('\n', '', NewsArray[0])
        response1 = b.bitly.short(NewsArray[0])
        response1 = response1['url']

        NewsArray[1] = re.sub('\n', '', NewsArray[1])
        response2 = b.bitly.short(NewsArray[1])
        response2 = response2['url']

        NewsArray[2] = re.sub('\n', '', NewsArray[2])
        response3 = b.bitly.short(NewsArray[2])
        response3 = response3['url']

        news1FewWords = sortedNews[0][0].split()
        dailyNews += news1FewWords[0] + " "
        + news1FewWords[1] + " " + news1FewWords[2]
        + "...." + response1 + "\n"

        news2FewWords = sortedNews[1][0].split()
        dailyNews += news2FewWords[0] + " "
        + news2FewWords[1] + " " + news2FewWords[2]
        + "...." + response2 + "\n"

        news3FewWords = sortedNews[2][0].split()
        dailyNews += news3FewWords[0] + " "
        + news3FewWords[1] + " " + news3FewWords[2]
        + "...." + response3 + "\n" + "# india \
		# amarnath \
		# fintech"
        print(dailyNews)

        status = api.update_status(status=dailyNews)
        if status:
            for i in range(3):
                datas = {}
                datas['time'] = str(date.today())
                datas['posted_as'] = i
                datas['news'] = sortedNews[i][0]
                datas['shortenedlink'] = NewsArray[i]
                datas['reviewcount'] = sortedNews[i][1]
                datas['link'] = sortedNews[i][2]
                db1.Collection_tweeted_news.insert(datas)


    except Exception as e:
        print(e)
        print("Error in getting today news data", str(date_str))


# Driver Code
News1 = ' '
News2 = ' '

date_str = str(date.today())
print("today", date_str)
client = MongoClient('mongodb://localhost:27017/')

# Connect your database here
db1 = client.xxxx

# credentials to tweet
consumer_key = "wjLlVsfN7YF2kUDkQsAh0FAPz"
consumer_secret = "XJLEDT72yMgfS1x6iUsHcrwhbnp4wHhwiHVKYxXz3VMg6qJN1z"
access_token = "1301183650482933761-pf83UZdPxJogVW9qf0jRJyWsSJwuKj"
access_token_secret = "h8AdZgNsKwYgwrq1BzR7h3ZV1XW0RFH03mfN2LZVKQU1T"

# authentication of consumer key and secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# authentication of access token and secret
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,
                 wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

tweetDailyNews()
