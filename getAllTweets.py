import tweepy
import configparser
import pandas as pd
import csv
import time
from colorama import Fore, Back, Style
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
from algo import Struct

# config = configparser.ConfigParser()
# config.read('config.ini')

#Connect to api
api_key =
api_key_secret =

access_token = 
access_token_secret = 

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# , wait_on_rate_limit_notify=True

#global vars
tweets_tmp = api.mentions_timeline()
last_mention= 0
tweets = []
ids = []
tweets_tmp2=[]
cloned_tweets=[]
username_index=0
inital_tweet_id=0
last_mention_txt="init"

while(1):
    # Get user name to scan in last timeline mention
    while(1):
        #does mention contain "scanner" keyword
        if ("scanner" in tweets_tmp[last_mention].text and tweets_tmp[last_mention].text != last_mention_txt):
            # and tweets_tmp[last_mention].text != last_mention_txt pas de cache

            print("scanning...")
            result =[pos for pos, char in enumerate(tweets_tmp[last_mention].text) if char == "@"]
            username_index=result[len(result)-1]
            print(tweets_tmp[last_mention].text[username_index])
            # get initial tweet
            inital_tweet_id=tweets_tmp[last_mention].id
            last_mention_txt=tweets_tmp[last_mention].text

            break

        print("waiting for input")
        time.sleep(10)

        tweets_tmp = api.mentions_timeline()

    i=0
    test=[]

    #get user info
    text_size= len(tweets_tmp[last_mention].text)
    user = tweets_tmp[last_mention].text[username_index:text_size]
    user_tmp = tweets_tmp[last_mention].text[username_index+1:text_size]

    user_status = api.get_user(screen_name=user_tmp)

    # Vérification si le compte est privé
    if user_status.protected:
        print(f"Le compte {user} est privé.")
    else:
        # Get all user's tweets
        limit=3200
        tweepy_cursor = tweepy.Cursor(api.user_timeline, screen_name=user, count=200, tweet_mode='extended', include_rts=False, exclude_replies=True).items()

        # Store tweets texts and IDs
        nbr_tweets=0
        # for tweet in tweepy_cursor:
        for tweet in tweepy_cursor:

            tweets.append(str(tweet.full_text))
            ids.append(str(tweet.id))
            nbr_tweets=nbr_tweets+1
            if (nbr_tweets==1):
                print("salut)")




        def similar(a, b):
            return SequenceMatcher(None, a, b).ratio()


        # create dataframe
        columns = ['User', 'Tweet']
        data = []

        class stat(Struct):
            text=str
            rec=int
            ids=str

            
        tweet_stats=[]

        for tweet in tweets:
            print(tweet)

        ind_limit=nbr_tweets

        #Brute force string comparison, >= 70 == similar tweets
        d=0
        for i in range(ind_limit):

            tweet_stats.append(stat(text=tweets[i], rec = 1, ids=ids[i]))

            for c in range(ind_limit-i-1):

                if(tweets[i] in tweets_tmp2):break

                c=c+i+1        

                token_ratio=fuzz.token_sort_ratio(tweets[i], tweets[c])
                if(token_ratio >= 70):
                    print("\n Ce tweet : "+ tweets[i] + " et ce tweet : " + tweets[c] + " sont similaires \n" )
                    
                    tweet_stats[d].rec = tweet_stats[d].rec + 1
                    tweets_tmp2.append(tweets[c])
            
            d=d+1

        #Tweet the repeated tweets with number of occurence, in a threaded answer to the mention tweet
        if (len(tweet_stats)==0):
            api.update_status("Cet utilisateur n'a pas répété ses tweets", in_reply_to_status_id=inital_tweet_id, auto_populate_reply_metadata=True)
            
        else:

            for val in tweet_stats:

                if (val.rec >=2):
                
                    stuff_in_string = "this tweet has been repeated: {} times https://twitter.com/user/status/{}\n".format(str(val.rec), val.ids)
                    print(stuff_in_string)

                    # Quote a tweet
                    api.update_status(stuff_in_string, in_reply_to_status_id=inital_tweet_id, auto_populate_reply_metadata=True)