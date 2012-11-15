import pickle

l = dict()
l['obama'] =[]
l['romney'] =[]
l['neutral'] =[]
for line in open("/home/tarun/git/TweetSent/data/table.csv"):
  token = line.split("\t")
  if len(token) == 5:
    if token[2] == "\"1\"":
      l['obama'].append(token[1])
    if token[2] == "\"2\"":
      l['romney'].append(token[1])
    else:
      l['neutral'].append(token[1])

pickle.dump(l, open("/home/tarun/git/TweetSent/data/labelled_tweets.pkl", "w"))
