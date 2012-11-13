import sys
import os
import tweepy
import webbrowser
import pickle
import random
from collections import defaultdict

def get_files(path):
  dirList=os.listdir(path)
  files = []
  for fname in dirList:
    files.append(fname)
  return files

def is_english(tweet):
   return tweet.user.lang == 'en'

def is_from_US(tweet):
  pass

def tweet_location(t):
  if t.place != None:
    state = t.place['full_name'].split(",")
    if len(state) == 2 and len(state[1]) == 3:
      return state[1]
  return None

def user_location(t):
  if t.user.location != None:
    state = t.user.location.split(",")
    if len(state) > 1 :
        return state[1]
  return None

def mentions_obama(tweet):
  if "obama" in tweet.text.lower() or "barrack" in tweet.text.lower():
    return True
  return False

def mentions_romney(tweet):
  if "romney" in tweet.text.lower() or "mitt" in tweet.text.lower():
    return True
  return False

def split_tweets(tweets):
  obama_tweets = []
  romney_tweets = []
  both_tweets = []
  none_tweets = []
  all_tweets = dict()
  for tweet in tweets:
    if mentions_obama(tweet) and not mentions_romney(tweet):
      obama_tweets.append(tweet)
    elif mentions_romney(tweet) and not mentions_obama(tweet):
      romney_tweets.append(tweet)
    elif mentions_obama(tweet) and mentions_romney(tweet):
      both_tweets.append(tweet)
    else:
      none_tweets.append(tweet)
  all_tweets['obama'] = obama_tweets
  all_tweets['romney'] = romney_tweets
  all_tweets['both'] = both_tweets
  all_tweets['none'] = none_tweets
  return all_tweets

def print_labelled_data(tweets):
  for t in tweets:
    print t.text, t.class_label


def label_tweets(tweets, num_to_label):
  labelled_tweets = []
  num_labelled = 0
  random.shuffle(tweets)
  for t in tweets:
    print t.text
    cls = raw_input()
    if cls == "o" or cls =="r":
      setattr( t, 'class_label', cls )
      num_labelled += 1
      labelled_tweets.append(t)
    if num_labelled == num_to_label:
      break
  return labelled_tweets    
  
def create_labelled_data(all_tweets, input_fname, output_fname, num_to_label):
#first_en_labelled
  obama_tweets = all_tweets['obama']
  romney_tweets = all_tweets['romney']
  both_tweets = all_tweets['both'] 
  none_tweets = all_tweets['none']
  labelled_tweets = []
  labelled_tweets += label_tweets(obama_tweets, num_to_label)
  labelled_tweets += label_tweets(romney_tweets, num_to_label)
  labelled_tweets += label_tweets(both_tweets, num_to_label)
  labelled_tweets += label_tweets(none_tweets, num_to_label)
  print_labelled_data(labelled_tweets)

  
  
  
