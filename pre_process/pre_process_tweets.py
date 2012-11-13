# splits the tweet dump into files marked as 1 minute interval from the start of debate
import sys
import os
import tweepy
import webbrowser
import pickle
from datetime import datetime
from collections import defaultdict


input_path = "/home/tarun/school/arnab/datasets/elections/for_context_raw"
output_path = "/home/tarun/school/arnab/datasets/elections/for_context_split_by_time"
start_time = datetime.strptime("2012-10-04 01:00:00", '%Y-%m-%d %I:%M:%S')
tweets_by_minute = dict()
def get_files(path):
  dirList=os.listdir(path)
  files = []
  for fname in dirList:
    files.append(fname)
  return files

files_list = get_files(input_path)
for f in sorted(files_list):
  input_file_path = input_path + "/" + f
  print "File: ", input_file_path
  var = pickle.load(open(input_file_path, "r"))
  for en, t in enumerate(var):
    date_object = t.created_at#datetime.strptime(t.created_at, '%Y-%m-%d %I:%M:%S')
    min_offset = ((date_object - start_time).seconds) / 60
    if min_offset in tweets_by_minute:
       tweets_by_minute[min_offset].append(t)
    else:
       tweets_by_minute[min_offset] = [t]

for min_offset in tweets_by_minute:
  pickle.dump(tweets_by_minute[min_offset], open(output_path + "/" + str(min_offset), "w"))
#for t in tweets_by_minute[1]:
#  print t.created_at
