import re
import pickle

def jaccard(vec1, vec2):
  i = vec1.intersection(vec2)
  u = vec1.union(vec2) 
  return len(i)/float(len(u))

def max_jaccard(transcript_sentences, tweet):
#  return [(jaccard(s, tweet), s) for s in transcript_sentences]
  return max([jaccard(s, tweet) for s in transcript_sentences])

def get_most_similar_tweet(f, transcript_text):
  sims = []
  for i in range(f, f+5):
    if i > 91:
      break
    input_file_path = "/home/tarun/school/arnab/datasets/elections/for_context_split_by_time/" + str(i)
    #print input_file_path
    transcript_words = set((re.split('\W+', transcript_text.strip().lower())))
    tweets = pickle.load(open(input_file_path, "r"))
    for t in tweets:
      tweet_words = set((re.split('\W+', t.text.strip().lower())))
      sims.append((jaccard(transcript_words, tweet_words), t.text))
  return sims

transcript = open("/home/tarun/school/arnab/scripts/twitter/subtitles.processed").readlines()

op_file = open("/home/tarun/school/arnab/scripts/twitter/context.processed", "w")
op_text = ""
for i, context in enumerate(transcript):
  print i, context
  similarity = get_most_similar_tweet(i, context)
  similarity.sort(key=lambda tup: tup[0], reverse=True)
  op_text += "\n" + context 
  sim_text = [ s[1] for s in similarity[0:5]]
  for st in sim_text:
    try:
      op_text += st + "\n"
    except:
      pass
  #print op_text
op_file.write(op_text)


