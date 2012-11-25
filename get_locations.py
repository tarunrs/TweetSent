import pickle
import urllib
import json
import sys
from time import sleep
HOME_DIR = "/home/tarun/git/TweetSent/"
locations = []


def get_location(raw_location, i):
  raw_location = raw_location.encode('utf-8')
  params = {'address' : raw_location, 'sensor' : 'false'}
  params_encoded  = urllib.urlencode(params)
  url_req =  'http://maps.googleapis.com/maps/api/geocode/json?' + params_encoded
  sleep(0.5)
  res = urllib.urlopen(url_req)
  j = json.loads(res.read())
  state_code = "NOT_US"
  country_code = "NOT_US"
  
  if (j['status'] == "OK"):
    try:
      if len(j['results'][0]['address_components']) > 1:
        if j['results'][0]['address_components'][-1]['types'][0] == "country":
          country_code = j['results'][0]['address_components'][-1]['short_name']
          if country_code == 'US':
            state_code = j['results'][0]['address_components'][-2]['short_name']
          else:
            print raw_location, country_code
        elif j['results'][0]['address_components'][-1]['types'][0] == "postal_code":
          country_code = j['results'][0]['address_components'][-2]['short_name']
          if country_code == 'US':
            state_code = j['results'][0]['address_components'][-3]['short_name']
          else:
            print raw_location, country_code
      else:
        print raw_location, j
    except:
      print "[ERROR] :", raw_location
  elif j['status'] == "OVER_QUERY_LIMIT":
    print "[Exiting] : ", j['status'], "[FILE] : ", i
    sys.exit()
  return state_code


for i in range(32, 91):
  input_file_path = "/home/tarun/school/arnab/datasets/elections/for_context_split_by_time/" + str(i)
  output_file_path = "/home/tarun/school/arnab/datasets/elections/states_labelled/" + str(i)
  
  print input_file_path
  tweets = pickle.load(open(input_file_path, "r"))
  for t in tweets:
    if t.place:
      loc = get_location(t.place['full_name'], i)
      print t.place['full_name'], loc
      locations.append(loc)
      setattr( t, 'state_location', loc ) 
    else:
      loc = get_location(t.user.location, i)
      print t.user.location, loc
      locations.append(loc)
      setattr( t, 'state_location', loc ) 
  pickle.dump(tweets, open(output_file_path, "w"))


