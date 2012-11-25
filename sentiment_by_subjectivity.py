import pickle
import re
from collections import defaultdict

def get_subjectivity_words():
  words = dict()
  words["positive"] = []
  words["negative"] = []
  words["neutral"] = []
  words["both"] = []
  words["weakneg"] = []
  words["strongneg"] = []

  f = open("data/subjectivity", "r")
  for line in f.readlines():
    tokens = line.split(" ")
    word = tokens[2].split("=")[1].strip()
    sentiment = tokens[-1].split("=")[1].strip()
    print word, sentiment
    words[sentiment].append(word)
  pickle.dump(words, open("data/subjectivity.pkl", "w"))

def get_sentiment(text, subjectivity_words):
  rword = re.compile(r"\w+")
  words = rword.findall(text)
  pos = 0
  neg = 0
  neutral = 0
#  print words
  for word in words:
    if word in subjectivity_words['positive']:
      #print word
      pos += 1
    elif word in subjectivity_words['negative'] or word in subjectivity_words['weakneg'] or word in subjectivity_words['strongneg'] :
      #print word
      neg += 1
    elif word in subjectivity_words['both'] or word in subjectivity_words['neutral'] :
      neutral += 1
  if pos > neg:
    print text
    print pos, neg, neutral
  return pos < neg

def get_hashtags(text):
  reg_hastag = re.compile(r"(#[^ ]+)")
  reg_word = re.compile(r"\w+")
  hashtags = reg_hastag.findall(text) 
  htags = []
  for h in hashtags:
    tags = reg_word.findall(h)
    if tags:
      htags.append("#" + tags[0])
  return htags

def has_pro_hastags(text, pro_hastags):
  hashtags = get_hashtags(text)
  for h in hashtags:
    if h+"\n" in pro_hastags:
      #print h
      return True
  return False

#get_subjectivity_words()
pro_obama = open("data/pro_obama_hashtags", "r").readlines()
pro_romney = open("data/pro_romney_hashtags", "r").readlines()
sub_words = pickle.load(open("data/subjectivity.pkl", "r"))

tweets = pickle.load(open("data/both.neg", "r"))
sent = 0
for tweet in tweets:
  sent += get_sentiment(tweet.lower(), sub_words)# or has_pro_hastags(tweet, pro_obama)

print len(tweets), sent



