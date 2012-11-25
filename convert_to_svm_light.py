import re
import pickle
import random

def get_subjectivity_scores(text, subjectivity_words):
  rword = re.compile(r"\w+")
  words = rword.findall(text)
  pos = 0
  neg = 0
  neutral = 0
  for word in words:
    if word in subjectivity_words['positive']:
      pos += 1
    elif word in subjectivity_words['negative'] or word in subjectivity_words['weakneg'] or word in subjectivity_words['strongneg'] :
      neg += 1
    elif word in subjectivity_words['both'] or word in subjectivity_words['neutral'] :
      neutral += 1

  return  (pos, neg, neutral)


def dump_dimensions():
  reg_html = re.compile(r"(http://[^ ]+)")
  reg_word = re.compile(r"\w+")
  reg_at = re.compile(r"(@[^ ]+)")
  reg_hastag = re.compile(r"(#[^ ]+)")

  dimensions = set([])
  for i in range(92):
  
    tweets = pickle.load(open("webservice/data/tweets/" + str(i), "r"))
    for t in tweets:
      s = t.text.lower()
      hashtags = reg_hastag.findall(s) 
      htags = []
      for h in hashtags:
        tags = reg_word.findall(h)
        if tags:
          htags.append("#" + tags[0])
      #hashtags = [h.strip(".,!?\"\'\n\t") for h in hashtags]
      s = reg_hastag.sub('', s)
      words = reg_word.findall(reg_at.sub('',reg_html.sub('', s)))
      dimensions |= set(words)| set(htags)
    print i, len(dimensions)

  temp_str = ""
  dimensions = sorted(list(dimensions))
  for word in dimensions:
    temp_str += word+"\n"
  
  f = open("data/dimensions", "w")
  f.write(temp_str.encode("UTF-8"))
  f.close()
  pickle.dump(dimensions, open("data/dimensions.pkl", "w"))

def dump_dimentions_dict():
  dimensions = pickle.load(open("data/dimensions.pkl", "r"))
  dimensions_dict = dict()
  for i, d in enumerate(dimensions):
    dimensions_dict[d] = i
  print dimensions_dict['obama']
  pickle.dump(dimensions_dict, open("data/dimensions.dict.pkl", "w"))


def get_feature_words(tweet_text):
  reg_html = re.compile(r"(http://[^ ]+)")
  reg_word = re.compile(r"\w+")
  reg_at = re.compile(r"(@[^ ]+)")
  reg_hastag = re.compile(r"(#[^ ]+)")
  s = tweet_text.lower()
  hashtags = reg_hastag.findall(s) 
  htags = []
  for h in hashtags:
    tags = reg_word.findall(h)
    if tags:
      htags.append("#" + tags[0])
      #hashtags = [h.strip(".,!?\"\'\n\t") for h in hashtags]
  s = reg_hastag.sub('', s)
  words = reg_word.findall(reg_at.sub('',reg_html.sub('', s)))
  return set(words)| set(htags)


def convert_tweet_file_to_svm_light(ip_filepath, op_filepath, label):
  d_dict = pickle.load(open("data/dimensions.dict.pkl", "r"))
  sub_words = pickle.load(open("data/subjectivity.pkl", "r"))
  tweets = pickle.load(open(ip_filepath, "r"))
  temp_str = ""
  for tweet in tweets:
    words = get_feature_words(tweet)
    feature_vector = label + " "
    for word in sorted(words):
      if word in d_dict:
        feature_vector += str(d_dict[word]+1)+":" +"1.0 "
      #else:
        #print word
#28865    
    sub_scores = get_subjectivity_scores(tweet, sub_words)
    #feature_vector += "28865:" + str(sub_scores[0])  + " 28866:" + str(sub_scores[1]) + " 28867:" + str(sub_scores[2]) + "\n"
    feature_vector += "\n"
    #print feature_vector
    temp_str += feature_vector
  return temp_str
#pos_files = ["data/romney.o.pos", "data/romney.b.pos"] #Obama vs Romney
#neg_files = ["data/romney.o.neg", "data/both.neg"]
#pos_files = ["data/obama.o.pos", "data/obama.b.pos"]
#neg_files = ["data/obama.o.neg", "data/both.neg"]
pos_files = ["data/romney.o.pos", "data/romney.b.pos", "data/obama.o.pos", "data/obama.b.pos"]
neg_files = ["data/romney.o.neg", "data/both.neg", "data/obama.o.neg", ]

pos_file = "data/svm/temp.pos"
neg_file = "data/svm/temp.neg"
final_training_file = "data/svm/obama.romney.neutral.train.svm"
final_testing_file = "data/svm/obama.romney.neutral.test.svm"

str_to_write = ""
for f in pos_files:
  str_to_write += convert_tweet_file_to_svm_light(f, pos_file + ".svm", "+1")
f = open(pos_file + ".svm", "w")
f.write(str_to_write)
f.close()

str_to_write = ""
for f in neg_files:
  str_to_write += convert_tweet_file_to_svm_light(f, neg_file + ".svm", "-1")
f = open(neg_file + ".svm", "w")
f.write(str_to_write)
f.close()



first_file = open(pos_file + ".svm", "r").readlines()
second_file = open(neg_file + ".svm", "r").readlines()
random.shuffle(first_file)
random.shuffle(second_file)
final_training_str = ""
final_testing_str = ""
print len(first_file), len(second_file)
count_line = 400
if len(first_file) < len(second_file):
  final_training_str += "".join(first_file[:count_line]) + "".join(second_file[:count_line])
  final_testing_str += "".join(first_file[count_line:]) +  "".join(second_file[count_line:])
else:
  final_training_str += "".join(first_file[:count_line]) + "".join(second_file[:count_line])
  final_testing_str += "".join(first_file[count_line:])+ "".join(second_file[count_line:])

f = open(final_training_file, "w")
f.write(final_training_str)
f.close()


f = open(final_testing_file, "w")
f.write(final_testing_str)
f.close()
#dump_dimensions()
#dump_dimentions_dict()
