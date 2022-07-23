import twitter

'''
Instantiate Twitter auth
'''
CONSUMER_KEY = 'wjLlVsfN7YF2kUDkQsAh0FAPz'
CONSUMER_SECRET = 'XJLEDT72yMgfS1x6iUsHcrwhbnp4wHhwiHVKYxXz3VMg6qJN1z'
OAUTH_ACCESS_TOKEN = '1301183650482933761-pf83UZdPxJogVW9qf0jRJyWsSJwuKj'
OAUTH_ACCESS_TOKEN_SECRET = 'h8AdZgNsKwYgwrq1BzR7h3ZV1XW0RFH03mfN2LZVKQU1T'

# consumer_key = "wjLlVsfN7YF2kUDkQsAh0FAPz"
# consumer_secret = "XJLEDT72yMgfS1x6iUsHcrwhbnp4wHhwiHVKYxXz3VMg6qJN1z"
# access_token = "1301183650482933761-pf83UZdPxJogVW9qf0jRJyWsSJwuKj"
# access_token_secret = "h8AdZgNsKwYgwrq1BzR7h3ZV1XW0RFH03mfN2LZVKQU1T"

auth = twitter.oauth.OAuth(OAUTH_ACCESS_TOKEN, OAUTH_ACCESS_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
'''
Get Twitter object
'''
twitter_api = twitter.Twitter(auth=auth)
'''
Search twitter by hashtag
'''
tweets = twitter_api.search.tweets(q="#machinelearning AND #deeplearning AND #datascience", max_results=200)
'''
Print Tweets
'''
RETWEET_COUNT_THRESHOLD = 25

for status in tweets['statuses']:
    if status['retweet_count'] > RETWEET_COUNT_THRESHOLD:
        print('\n\n', status['user']['screen_name'], ":", status['text'], '\nTweet URL: ',
              status['retweeted_status']['entities']['urls'][0]['expanded_url'],
              '\nRetweet count: ', status['retweet_count'])