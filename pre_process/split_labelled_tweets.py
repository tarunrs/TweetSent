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
    obama_both_positive.append(t)
  else:
    obama_only_positive.append(t)

for t in l['romney']:
  if mentions_obama(t):
    romney_both_positive.append(t)
  else:
    romney_only_positive.append(t)

for t in l['romney']:
  if mentions_obama(t):
    romney_both_positive.append(t)
  else:
    romney_only_positive.append(t)

for t in l['neutral']:
  if mentions_obama(t) and mentions_romney(t):
    both_negative.append(t)
  elif mentions_obama(t) :
    obama_only_negative.append(t)
  else:
    romney_only_negative.append(t)

print "Positive examples for Obama" , len(obama_only_positive)
print "Positive examples for Romney" , len(romney_only_positive)
print "Positive examples for Obama(b)" , len(obama_both_positive)
print "Positive examples for Romney(b)" , len(romney_both_positive)
print "Negative examples for Obama" , len(obama_only_negative)
print "Negative examples for Romney" , len(romney_only_negative)
print "Negative examples for Both" , len(both_negative)

pickle.dump(obama_only_positive, HOME_DIR + "data/obama.o.pos")
pickle.dump(romney_only_positive, HOME_DIR + "data/romney.o.pos")
pickle.dump(obama_both_positive, HOME_DIR + "data/obama.b.pos")
pickle.dump(romney_both_positive, HOME_DIR + "data/romney.b.pos")

pickle.dump(obama_only_negative, HOME_DIR + "data/obama.o.neg")
pickle.dump(romney_only_negative, HOME_DIR + "data/romney.o.neg")
pickle.dump(both_negative, HOME_DIR + "data/both.neg")





