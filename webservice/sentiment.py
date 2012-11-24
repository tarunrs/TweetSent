import re
import pickle

class Sentiment():
  def __init__(self):
    HOME_DIR = "/home/tarun/git/TweetSent/"
    pass

  def get_feature_vectors(ip_filepath):
    d_dict = pickle.load(open("data/dimensions.dict.pkl", "r"))
    tweets = pickle.load(open(ip_filepath, "r"))
    temp_str = ""
    for tweet in tweets:
      words = self.get_feature_words(tweet)
      feature_vector = "0 "
      for word in sorted(words):
        if word in d_dict:
          feature_vector += str(d_dict[word]+1)+":" +"1.0 "
    feature_vector += "\n"
    temp_str += feature_vector
  return temp_str

  def get_feature_words(self, tweet_text):
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
    return set(words) | set(htags)

  def get_sentiments(time_interval):
    ip_file_path = self.HOME_DIR + "data/tweets/" + str(time_interval)
    svm_file_path = self.HOME_DIR + "data/temp/"+str(time_interval)+".svm"
    op_feature_vector_file = open(svm_file_path, "w" )
    op_feature_vector_file.write(get_feature_vectors(ip_file_path))
    op_feature_vector_file.close()
    




