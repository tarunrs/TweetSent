import urllib2
from BeautifulSoup import BeautifulSoup, NavigableString, Tag
import pickle
from time import time, strftime, localtime, sleep

def get_news_items(soup):
  links = soup.findAll('h2', { 'class' : 'esc-lead-article-title'})
  news_items = []
  for l in links:
    story = {}
    story['text'] = l.a.text
    story['link'] = l.a['href']
    news_items.append(story)
  return news_items

def get_news_items_from_url(url):
  html_doc = urllib2.urlopen(url).read()
  soup = BeautifulSoup(html_doc)
  return get_news_items(soup)

def get_sub_topics(soup_object):
  first_level = soup.ul.contents
  sub_topics = []
  for item in first_level:
    if item['class'].find('selected-nav-item') != -1:
      if section != "Spotlight":
        for sub_item in item.div.contents:
          #print sub_item.a.string, sub_item.a.get('href')
          sub_topic = {}
          sub_topic['link'] = sub_item.a['href']
          sub_topic['text'] = sub_item.a.text
          sub_topics.append(sub_topic)
      break
  return sub_topics

def print_topics(topics):
  for topic in topics:
    print topic
    for sub_topic in topics[topic]:
      print "\t" + sub_topic['text'], '\t', sub_topic['link']

def print_stories(top_stories, section):
  print '\n', section, '\n'
  for sub_category in top_stories[section]:
    print_stories_of_section(top_stories, section, sub_category)
 
def print_stories_of_section(top_stories, section, sub_category):
  for story in top_stories[section][sub_category]:
    print story['text'], '\n', story['link'], '\n\n'

def dump_stories(top_stories, section, fname):
  f = open(fname, "w")
  f.write('\n'+ section + '\n')
  for sub_category in top_stories[section]:
    f.write('\n'+ sub_category + '\n')
    dump_stories_of_section(top_stories, section, sub_category, f)
  f.close()


def dump_stories_of_section(top_stories, section, sub_category, f):
  for story in top_stories[section][sub_category]:
    try:
      f.write( story['text'].decode('utf-8') + '\n' + story['link'].decode('utf-8') + '\n\n')
    except:
      print story['text'], '\n', story['link'], '\n\n'

start = time()

while True:
  sections = {
  'Top Stories' :  '/news/section?pz=1&cf=all&ned=us&ict=ln',
  'U.S.' : '/news/section?pz=1&cf=all&ned=us&topic=n&ict=ln',
  'Business' : '/news/section?pz=1&cf=all&ned=us&topic=b&ict=ln',
  'Elections' : '/news/section?pz=1&cf=all&ned=us&topic=el&ict=ln',
  'Technology' : '/news/section?pz=1&cf=all&ned=us&topic=tc&ict=ln', 
  'Entertainment' : '/news/section?pz=1&cf=all&ned=us&topic=e&ict=ln' ,
  'Sports' : '/news/section?pz=1&cf=all&ned=us&topic=s&ict=ln', 
  'Science': '/news/section?pz=1&cf=all&ned=us&topic=snc&ict=ln', 
  'Health': '/news/section?pz=1&cf=all&ned=us&topic=m&ict=ln' ,
  'Spotlight' : '/news/section?pz=1&cf=all&ned=us&topic=ir&ict=ln'
  }

  base_url = 'http://news.google.com'
  topics = {}
  top_stories = {}

  for section in sections:
    print "Crawling for", section
    sub_topics = []
    html_doc = urllib2.urlopen(base_url + sections[section]).read()
    soup = BeautifulSoup(html_doc)
    top_stories[section] = {}
    top_stories[section]['Top'] = get_news_items(soup)
    topics[section] = get_sub_topics(soup)

    for sub_topic in topics[section]:
      print '\t', sub_topic['text']
      html_doc = urllib2.urlopen(base_url + sub_topic['link']).read()
      soup = BeautifulSoup(html_doc)
      top_stories[section][sub_topic['text']] = get_news_items(soup)
  fname = strftime("%d-%m-%Y-%H-%M-%S.gn.dmp", localtime())
#  fname = strftime("%H-%M-%S.gn.dmp", localtime())
  print fname
  pickle.dump(top_stories, open(fname, "w"))
  sleep(1800)
