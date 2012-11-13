# -*- coding: utf-8 -*-

import sys
import tweepy
import webbrowser
import pickle
from time import time, strftime, localtime
# Query terms

#Q = sys.argv[1:] 
Q = ["mitt", "romney", "barack", "obama", "election" , "elections", "democrat", "democrats", "republican", "republicans", "joe", "biden", "paul", "ryan"]


# Get these values from your application settings.

CONSUMER_KEY = 'TCISxTWBLQJSMQFowHw'
CONSUMER_SECRET = 'iGFHO3bGwEZLub66VDSZ50qLX2bu3kIZ9Xen1XRmY'

# Get these values from the "My Access Token" link located in the
# margin of your application details, or perform the full OAuth
# dance.

ACCESS_TOKEN = '9175042-yMyJMBeyvwj2Mfk6lbMT3P5o5RtvNEZcanc8ZJxxAA'
ACCESS_TOKEN_SECRET = 'dr7HaVobdtfCy8d5fkPG6qwb9VGmniuO0oEH56bLzdQ'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Note: Had you wanted to perform the full OAuth dance instead of using
# an access key and access secret, you could have uses the following 
# four lines of code instead of the previous line that manually set the
# access token via auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET).
# 
# auth_url = auth.get_authorization_url(signin_with_twitter=True)
# webbrowser.open(auth_url)
# verifier = raw_input('PIN: ').strip()
# auth.get_access_token(verifier)
tweets = []
i = 0
fnum = 0
class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        
        # We'll simply print some values in a tab-delimited format
        # suitable for capturing to a flat file but you could opt 
        # store them elsewhere, retweet select statuses, etc.



        try:
            global i
            global fnum
            tweets.append(status)
            i = i + 1
#            print status
#            print "%s\t%s\t%s\t%s" % (status.text, 
#                                      status.author.screen_name, 
#                                      status.created_at, 
#                                      status.source,)
            #print "%s" % (status.text) 
            
            if i == 10000:
              fnum = fnum + 1
              i = 0
              fname = strftime("%H-%M-%S.dmp", localtime())
              print fname
              pickle.dump(tweets, open(fname, "w"))
              del tweets[:]
        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

# Create a streaming API and set a timeout value of 60 seconds.

streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=60)

# Optionally filter the statuses you want to track by providing a list
# of users to "follow".

print >> sys.stderr, 'Filtering the public timeline for "%s"' % (' '.join(Q),)

streaming_api.filter(follow=None, track=Q)

#streaming_api.sample()
