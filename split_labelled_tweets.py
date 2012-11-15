import pickle
from tweetutils.helpers import mentions_obama, mentions_romney

HOME_DIR = "/home/tarun/git/TweetSent/"
l = pickle.load(open(HOME_DIR + "data/labelled_tweets.pkl", "r"))
obama_only_positive = []
romney_only_positive = []
obama_both_positive = []
romney_both_positive = []

obama_only_negative = []
romney_only_negative = []
both_negative = []

for t in l['obama']:
  if mentions_romney(t):
    obama_both_positive.append(t[1:-1])
  else:
    obama_only_positive.append(t[1:-1])

for t in l['romney']:
  if mentions_obama(t):
    romney_both_positive.append(t[1:-1])
  else:
    romney_only_positive.append(t[1:-1])

for t in l['neutral']:
  if mentions_obama(t) and mentions_romney(t):
    both_negative.append(t[1:-1])
  elif mentions_obama(t[1:-1]) :
    obama_only_negative.append(t[1:-1])
  else:
    romney_only_negative.append(t[1:-1])

print "Length of Obama positive", len(l['obama'])
print "Length of Romney positive", len(l['romney'])
print "Length of Neutral", len(l['neutral'])

print "Positive examples for Obama" , len(obama_only_positive)
print "Positive examples for Romney" , len(romney_only_positive)

print "Positive examples for Obama(b)" , len(obama_both_positive)
print "Positive examples for Romney(b)" , len(romney_both_positive)

print "Negative examples for Obama" , len(obama_only_negative)
print "Negative examples for Romney" , len(romney_only_negative)
print "Negative examples for Both" , len(both_negative)

pickle.dump(obama_only_positive, open(HOME_DIR + "data/obama.o.pos.pkl", "w"))
pickle.dump(romney_only_positive, open(HOME_DIR + "data/romney.o.pos.pkl", "w"))
pickle.dump(obama_both_positive, open(HOME_DIR + "data/obama.b.pos.pkl", "w"))
pickle.dump(romney_both_positive, open(HOME_DIR + "data/romney.b.pos.pkl", "w"))

pickle.dump(obama_only_negative, open(HOME_DIR + "data/obama.o.neg.pkl", "w"))
pickle.dump(romney_only_negative, open(HOME_DIR + "data/romney.o.neg.pkl", "w"))
pickle.dump(both_negative, open(HOME_DIR + "data/both.neg.pkl", "w"))






