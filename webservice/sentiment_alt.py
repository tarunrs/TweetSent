import re
import pickle
import os
from collections import defaultdict
class Sentiment():
  def __init__(self):
    self.HOME_DIR = "/home/tarun/git/TweetSent/webservice/"
    #self.HOME_DIR = "/root/server/webservice/"
    pass

  def get_feature_vectors(self, tweets):
    d_dict = pickle.load(open("data/dimensions.dict.pkl", "r"))    
    temp_str = ""
    print len(tweets)
    for tweet in tweets:
      words = self.get_feature_words(tweet.text)
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

  def generate_ensemble_file(self):
    obama_predictions = open("svm/tmp/obama.prediction", "r").readlines()
    romney_predictions = open("svm/tmp/romney.prediction", "r").readlines()
    obama_romney_predictions = open("svm/tmp/obama.romney.neutral.prediction", "r").readlines()
    feature_vecs = []
    for i in range(len(obama_predictions)):
      feature_vecs.append("0 1:"+ obama_predictions[i].strip() + " 2:" + romney_predictions[i].strip() + " 3:" + obama_romney_predictions[i].strip() +"\n")
    f = open("svm/tmp/ensemble.svm", "w") 
    f.write("".join(feature_vecs))
    f.close()

  def evaluate_results(self, tweets):
    obama_predictions = open("svm/tmp/obama.prediction", "r").readlines()
    romney_predictions = open("svm/tmp/romney.prediction", "r").readlines()
    pos_tweets = []
    neg_tweets = []
    for i in range(len(obama_predictions)):
      p = float(obama_predictions[i].strip()) + float(romney_predictions[i].strip())
      if p > 0.0:
        #print tweets[i].text      
        pos_tweets.append((p, tweets[i]))
      else:
#        print tweets[i].text
        neg_tweets.append((p, tweets[i]))
    return (pos_tweets, neg_tweets)

  def split_results(self, tweets, predicted_file):
    predictions = open(predicted_file, "r")
    pos_tweets = []
    neg_tweets = []
    for i, p in enumerate(predictions):
      if float(p.strip()) > 0:
        pos_tweets.append((p,tweets[i]))
      else:
        neg_tweets.append((p,tweets[i]))
    return (pos_tweets, neg_tweets)

  def classify_tweets(self, positive_tweets):
    predicted_value, tweets = zip(*positive_tweets)
    svm_file_path = self.HOME_DIR + "svm/tmp/for_classification.svm"
    op_feature_vector_file = open(svm_file_path, "w" )
    op_feature_vector_file.write(self.get_feature_vectors(tweets))
    op_feature_vector_file.close()
    os.system('svm/svm_classify svm/tmp/for_classification.svm svm/models/obama.romney.model svm/tmp/classified.prediction')
    return self.split_results(tweets, "svm/tmp/classified.prediction")

  def get_sentiments(self, time_interval):
    censored_words = ["fuck", "nigga", "motherfucker", "nigga", "nigger", "ass", "asshole", "cunt", "bitch", "dick", "cock"]
    time_interval = time_interval + 2
    states_counts = dict()
    states = ['US-AK', 'US-AL', 'US-AR', 'US-AS', 'US-AZ', 'US-CA', 'US-CO', 'US-CT', 'US-DC', 'US-DE', 'US-FL', 'US-GA', 'US-GU', 'US-HI', 'US-IA', 'US-ID', 'US-IL', 'US-IN', 'US-KS', 'US-KY', 'US-LA', 'US-MA', 'US-MD', 'US-ME', 'US-MH', 'US-MI', 'US-MN', 'US-MO', 'US-MP', 'US-MS', 'US-MT', 'US-NC', 'US-ND', 'US-NE', 'US-NH', 'US-NJ', 'US-NM', 'US-NOT_US', 'US-NV', 'US-NY', 'US-OH', 'US-OK', 'US-OR', 'US-PA', 'US-RI', 'US-SC', 'US-SD', 'US-TN', 'US-TX', 'US-Twin Cities', 'US-UT', 'US-VA', 'US-VI', 'US-VT', 'US-WA', 'US-WI', 'US-WV', 'US-WY']
    for state in states:
       states_counts[state] = [0.0 , 0.0, 0.0]
    ip_file_path = self.HOME_DIR + "data/tweets/" + str(time_interval)
    svm_file_path = self.HOME_DIR + "svm/tmp/"+str(time_interval)+".svm"
    tweets = pickle.load(open(ip_file_path, "r"))
    print len(tweets)
    op_feature_vector_file = open(svm_file_path, "w" )
    op_feature_vector_file.write(self.get_feature_vectors(tweets))
    op_feature_vector_file.close()
    os.system('svm/svm_classify svm/tmp/'+str(time_interval)+'.svm svm/models/obama.neutral.model svm/tmp/obama.prediction')
    os.system('svm/svm_classify svm/tmp/'+str(time_interval)+'.svm svm/models/romney.neutral.model svm/tmp/romney.prediction')
#    os.system('svm/svm_classify svm/tmp/'+str(time_interval)+'.svm svm/models/obama.romney.neutral.model svm/tmp/obama.romney.neutral.prediction')
#    self.evaluate_predictions()
#    os.system('svm/svm_classify svm/tmp/ensemble.svm svm/models/ensemble.model svm/tmp/ensemble.prediction')
#    split_tweets = self.split_results(tweets, "svm/tmp/ensemble.prediction")
#    positive_tweets = split_tweets[0]
#    neutral_tweets = split_tweets[1]
    split_tweets = self.evaluate_results(tweets)
    positive_tweets = split_tweets[0]
    neutral_tweets = split_tweets[1]
    classified_tweets = self.classify_tweets(positive_tweets)
    obama_tweets = classified_tweets[0]
    romney_tweets = classified_tweets[1]
    obama_tweets.sort(key=lambda tup: tup[0])#, reverse=True)
    romney_tweets.sort(key=lambda tup: tup[0])#, reverse=True)
    neutral_tweets.sort(key=lambda tup: tup[0])#, reverse=True)
    ret = dict()
    num_tweets = 5
    ret["obama"]  = []
    index = 0
    cnt = 0
    while cnt < num_tweets and index < len(obama_tweets):
      if (obama_tweets[index][1].text, obama_tweets[index][0]) not in ret["obama"]:
        ret["obama"].append((obama_tweets[index][1].text, obama_tweets[index][0]))
        cnt += 1
      index +=1

    num_tweets = 5
    ret["romney"]  = []
    index = 0
    cnt = 0
    while cnt < num_tweets and index < len(romney_tweets):
      if (romney_tweets[index][1].text, romney_tweets[index][0]) not in ret["romney"]:
        ret["romney"].append((romney_tweets[index][1].text, romney_tweets[index][0]))
        cnt += 1
      index +=1

    num_tweets = 5
    ret["neutral"]  = []
    index = 0
    cnt = 0
    while cnt < num_tweets and index < len(neutral_tweets):
      if (neutral_tweets[index][1].text, neutral_tweets[index][0]) not in ret["neutral"]:
        ret["neutral"].append((neutral_tweets[index][1].text, neutral_tweets[index][0]))
        cnt += 1
      index +=1


#    ret["obama"] = [(t[1].text, t[0]) for t in obama_tweets[-5:] ]
#    ret["romney"]= [(t[1].text, t[0]) for t in romney_tweets[-5:] ]
#    ret["neutral"] = [(t[1].text, t[0]) for t in neutral_tweets[-5:] ]
    for censored_word in censored_words:
      ret['obama'] = [(t[0].lower().replace(censored_word, "*bleep*"), t[1]) for t in ret['obama'] ]
      ret['romney'] = [(t[0].lower().replace(censored_word, "*bleep*"), t[1]) for t in ret['romney'] ]
      ret['neutral'] = [(t[0].lower().replace(censored_word, "*bleep*"), t[1]) for t in ret['neutral'] ]
    for t in obama_tweets:
      if "US-"+ t[1].state_location in states_counts:
        states_counts["US-"+ t[1].state_location][0] += 1.0
        states_counts["US-"+ t[1].state_location][2] += 1.0
      else:
        states_counts["US-"+ t[1].state_location] = [1.0,0.0,1.0]

    for t in romney_tweets:
      if "US-"+ t[1].state_location in states_counts:
        states_counts["US-"+ t[1].state_location][1] += 1.0
        states_counts["US-"+ t[1].state_location][2] += 1.0
      else:
        states_counts["US-"+ t[1].state_location] = [0.0,1.0,1.0]
    states_info = dict()
    for state in states_counts:
       total = states_counts[state][0] + states_counts[state][1] + states_counts[state][2]
       if total > 0.0 :
         states_info[state] = (states_counts[state][0]/total) - (states_counts[state][1] /total)
       else:
         states_info[state] = 0
#    ret.append([(t[1].text, t[0]) for t in obama_tweets[-15:] ])
#    ret.append([(t[1].text, t[0]) for t in romney_tweets[-15:] ])
    ret_dict = dict()
    ret_dict['states'] = states_info
    ret_dict['tweets'] = ret
    return ret_dict
#    return (classified_tweets[0][-1][1].text, classified_tweets[0][-1][0])
    





