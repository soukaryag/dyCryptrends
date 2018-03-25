import re
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import coin_fetcher
import csv
from textblob import TextBlob

total_tweets = 0
good_tweets = 0
neutral_tweets = 0
bad_tweets = 0


def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(tweet)
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def run():
    consumer_key = "YAqvHGeTN46ttmmn8qyvtegSl"
    consumer_secret = "ssDGUf9jyYPsN5JCwrWH1IWA64LaUd9vsTPrd0J0Jm2gkpKURl"
    access_token = "3496798512-LgOl2NRjP0P7aX8XcqRV5c7yUMeJvS6njMJWNcc"
    access_token_secret = "5ApzTKHzk1aZ8rgxqNmEBPEVsxplqOfsKtlBiBx0K9adU"

    class listener(StreamListener):
        time = []

        def on_data(self, data):
            global total_tweets
            global good_tweets
            global bad_tweets
            global neutral_tweets
            all_data = json.loads(data)
            tweet = all_data["text"]                           #Analyze text for bots; things like LINKS, multiple COINS
            username = all_data["user"]["screen_name"]
            date = all_data["created_at"]
            followers = all_data["user"]["followers_count"]
            dollar_sign = re.compile(r"[$]([a-zA-Z0-9]?[a-zA-Z]+\d*)")                       #fetches the coin mentioned
            coin_detect = re.findall(dollar_sign, tweet)

            #SENTIMENT ANANLYSIS
            sent = get_tweet_sentiment(tweet)
            sent_value = int
            if sent is "positive":
                all_data["sentiment"] = 1
                sent_value = 1
                good_tweets += 1
            elif sent is "negative":
                all_data["sentiment"] = -1
                sent_value = -1
                bad_tweets += 1
            elif sent is "neutral":
                all_data["sentiment"] = 0
                sent_value = 0
                neutral_tweets += 1


            for c in range(0, len(coin_detect)):
                c_new = coin_detect[c].upper()
                coin_detect[c] = c_new + "," + str(sent_value)
            #print(username, " :: ", tweet, " :: ", date)

            # TWEAK this to set a maximum number of coins that can be mentioned/tweet before deeming it as a bot
            BOT_TEST = 4

            if 0 < len(coin_detect) < BOT_TEST:
                out = open('out1.txt', 'a')
                for item in coin_detect:
                    out.write(item + ",")
                out.write(str(followers) + ",")
                out.write(date)
                out.write('\n')
                out.close()

            return True

        def on_error(self, status):
            print(status)

    coins_abb_dollar, coins_dict, coins_abb = coin_fetcher.all_coins()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=coins_abb_dollar, languages=["en"])

run()
