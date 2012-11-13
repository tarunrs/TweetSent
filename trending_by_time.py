import re
import pickle
from collections import defaultdict
import operator
from nltk.corpus import stopwords
import string
op_text = ""

remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

for j in range(10):

  input_file_path = "/home/tarun/school/arnab/datasets/elections/for_context_split_by_time/" + str(j)
  print input_file_path
  tweets = pickle.load(open(input_file_path, "r"))
  trending = defaultdict(int)
  for t in tweets:
    tweet_words = re.split('\W+', t.text.strip().lower())
    #tweet_words = re.split('\b[a-z]+\b', t.text.strip().lower())

    #tweet_words = t.text.strip().lower().split()
    #print tweet_text, remove_punctuation_map
    #tweet_words = [s.translate(remove_punctuation_map) for s in tweet_text]

    filtered_words = [w for w in tweet_words if not w in stopwords.words('english')]
    #filtered_words = tweet_words
    for i in range(len(filtered_words) - 2) :
      bigram = filtered_words[i] + filtered_words[i+1]
      trigram = filtered_words[i] + filtered_words[i+1] + filtered_words[i+2] 
#      trending[filtered_words[i]] += 1
    #  trending[bigram] += 1  
      trending[trigram] += 1  
  op_text += str(j) +"\n"
  sorted_counts = sorted(trending.iteritems(), key=operator.itemgetter(1), reverse=True)
  for i, word in enumerate(sorted_counts):
    if i > 5:
      break
    op_text += word[0] + " : " + str(trending[word[0]]) +"\n"
  #print op_text

op_file = open("trending", "w")
op_file.write(op_text)

