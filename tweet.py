import tweepy as tw
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys

consumer_key = "MaF5KIHIjuAwrd7MgLQLDcLEo"
consumer_secret = "NRuFy9iKN9ZziahectpmQZNVuXWLStVCvEky58g5mHqx4DRm1d"
access_token = '1338326173676400641-4uc4T4tIZvtFRz2EdDTU7bSlHQGPQ0'
access_token_secret = 'O4yrscIawohfpAJ86vJfG5hHFjQFX3Okjsm82miRTpFzJ'
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth)

# List of users
#account_list = ['KingJames']
account_list = ['KingJames', 'KDTrey5', 'StephenCurry30', 'DwyaneWade', 'carmeloanthony', 'CP3', 'paugasol', 'JHarden13', 'DwightHoward', 'russwest44']

for target in account_list:
    print("Getting data for " + target)
    item = api.get_user(target)
    print("name: " + item.name)
    print("screen_name: " + item.screen_name)
    print("description: " + item.description)
    print("statuses_count: " + str(item.statuses_count))
    print("friends_count: " + str(item.friends_count))
    print("followers_count: " + str(item.followers_count))
    tweets = item.statuses_count
    account_created_date = item.created_at
    delta = datetime.utcnow() - account_created_date
    account_age_days = delta.days
    print("Account age (in days): " + str(account_age_days))
    if account_age_days > 0:
        print("Average tweets per day: " + "%.2f" % (float(tweets) / float(account_age_days)))
    hashtags = []
    mentions = []
    tweet_count = 0
    end_date = datetime.utcnow() - timedelta(days=365)
    for status in Cursor(api.user_timeline, id=target).items():
        tweet_count += 1
        if hasattr(status, "entities"):
            entities = status.entities
            if "hashtags" in entities:
                for ent in entities["hashtags"]:
                    if ent is not None:
                        if "text" in ent:
                            hashtag = ent["text"]
                            if hashtag is not None:
                                hashtags.append(hashtag)
            if "user_mentions" in entities:
                for ent in entities["user_mentions"]:
                    if ent is not None:
                        if "screen_name" in ent:
                            name = ent["screen_name"]
                            if name is not None:
                                mentions.append(name)
        #break out of the loop once we hit Tweets that are more than 30 days old
        if status.created_at < end_date:
            break

    print("Most mentioned Twitter users:")
    for item, count in Counter(mentions).most_common(10):
        print(item + "\t" + str(count))

    print("Most used hashtags:")
    for item, count in Counter(hashtags).most_common(10):
        print(item + "\t" + str(count))
    print("All done. Processed " + str(tweet_count) + " tweets.")

