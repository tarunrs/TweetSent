import re
import pickle

weights = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5]

def jaccard(vec1, vec2):
  i = vec1.intersection(vec2)
  u = vec1.union(vec2) 
  return len(i)/float(len(u))

def max_jaccard(transcript_sentences, tweet):
#  return [(jaccard(s, tweet), s) for s in transcript_sentences]
  return max([jaccard(s, tweet) for s in transcript_sentences])

def aggregate_jaccard(tweet_words, ind, transcript):
  total_jaccard = 0.0
  for r, i in enumerate(range(ind - 5, ind+1)):
    if i < 0:
      continue
    transcript_words = set((re.split('\W+', transcript[i].strip().lower())))
    total_jaccard += weights[r] * jaccard(transcript_words, tweet_words)
  return total_jaccard
transcript = ["Opening\n"]
transcript = transcript + open("/home/tarun/school/arnab/scripts/twitter/subtitles.processed").readlines()
op_file = open("/home/tarun/school/arnab/scripts/twitter/context.tweet.processed", "w")
op_text = ""

for i in range(91):
  input_file_path = "/home/tarun/school/arnab/datasets/elections/for_context_split_by_time/" + str(i)
  tweets = pickle.load(open(input_file_path, "r"))
  sims = []
  for t in tweets:
    tweet_words = set((re.split('\W+', t.text.strip().lower())))
    sims.append((aggregate_jaccard(tweet_words, i, transcript), t.text))
  sims.sort(key=lambda tup: tup[0], reverse=True)
  sim_text = [ s[1] for s in sims[0:5]]
  #print transcript[i] 
  op_text += str(i) +"\n" + unicode(transcript[i], errors='ignore')
  for st in sim_text:
    try:
      op_text +=  unicode(st, errors='ignore') + "\n"
    except:
      pass
  print op_text
op_file.write(op_text)

