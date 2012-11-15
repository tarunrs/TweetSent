import pickle
import random
import nltk
from tweetutils.helpers import get_word_features, get_words_in_tweets

HOME_DIR = "/home/tarun/git/TweetSent/"
obama_only_pos = pickle.load(open(HOME_DIR + "data/obama.o.pos", "r"))
obama_only_neg = pickle.load(open(HOME_DIR + "data/obama.o.neg", "r"))

random.shuffle(obama_only_pos)
random.shuffle(obama_only_neg)

#split into training and testing data. First 100 used for training
obama_pos_train = obama_only_pos[0:100]
obama_pos_test = obama_only_pos[100:]
obama_neg_train = obama_only_neg[0:100]
obama_neg_test = obama_only_neg[100:]

print len(obama_only_pos)
print len(obama_only_neg)
print len(obama_neg_train)
print len(obama_neg_test)

tweets = []
for words in obama_neg_train:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, "negative"))
for words in obama_pos_train:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, "positive"))
#print tweets


word_features = get_word_features(get_words_in_tweets(tweets))
#print word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

training_set = nltk.classify.apply_features(extract_features, tweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)
print classifier.show_most_informative_features(32)
counts = dict()
counts['positive'] = 0
counts['negative'] = 0
for t in obama_pos_test:
  counts[classifier.classify(extract_features(t.split()))] += 1

print counts['positive']
print counts['negative']


