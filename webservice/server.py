import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.database
import re
import pickle
import os
from tornado.options import define, options
import logging

define("mysql_host", default="127.0.0.1", help="blog database host")
define("mysql_database", default="tweets", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="tarun123", help="blog database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/map", MapHandler),
            (r"/set_label", SetLabelHandler),
            (r"/get_contextual_tweets", GetContextHandler),
            (r"/get_tweet", GetTweetHandler),
            (r"/js/jquery.js", JQueryHandler),
            (r"/set_nickname", SetNicknameHandler),
            (r"/js/jquery-jvectormap-1.1.1.min.js", JQueryJVectorHandler),
            (r"/js/states.js", StatesHandler),
            (r"/js/jquery-jvectormap-us-lcc-en.js", JQueryJVectorUSHandler),
        ]
        settings = dict(static_path = os.path.join(os.path.dirname(__file__), "static"))
        self.transcript = open("data/subtitles.processed").readlines()
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = tornado.database.Connection(
        host=options.mysql_host, database=options.mysql_database,
        user=options.mysql_user, password=options.mysql_password)

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    @property
    def transcript(self):
        return self.application.transcript


class MainHandler(BaseHandler):
    def get(self):
        self.render("html/index.html")

class MapHandler(BaseHandler):
    def get(self):
        self.render("html/map.html")

class JQueryHandler(BaseHandler):
    def get(self):
        self.render("js/jquery.js")

class JQueryJVectorHandler(BaseHandler):
    def get(self):
        self.render("js/jquery-jvectormap-1.1.1.min.js")

class StatesHandler(BaseHandler):
    def get(self):
        self.render("js/states.js")

class JQueryJVectorUSHandler(BaseHandler):
    def get(self):
        self.render("js/jquery-jvectormap-us-lcc-en.js")

class GetContextHandler(BaseHandler):
    def get(self):
      time_interval = int(self.get_argument("time_interval"))
      num_tweets = int(self.get_argument("num_tweets"))
      contextual_tweets = self.get_contextual_tweets(time_interval, num_tweets)
      self.write(tornado.escape.json_encode(contextual_tweets))

    def jaccard(self, vec1, vec2):
      i = vec1.intersection(vec2)
      u = vec1.union(vec2) 
      return len(i)/float(len(u))

    def max_jaccard(self, transcript_sentences, tweet):
      return max([self.jaccard(s, tweet) for s in transcript_sentences])

    def get_most_similar_tweet(self, f, transcript_text):
      sims = []
      transcript_words = set((re.split('\W+', transcript_text.strip().lower())))
      weights = [0.5, 0.8, 1.0, 0.8, 0.5]
      wt_index = -1
      for i in range(f, f+5):
        wt_index += 1
        if i > 91:
          break
        input_file_path = "data/tweets/" + str(i)    
        tweets = pickle.load(open(input_file_path, "r"))
        for t in tweets:
          tweet_words = set((re.split('\W+', t.text.strip().lower())))
          sims.append((weights[wt_index] * self.jaccard(transcript_words, tweet_words), t.text))
      return sims

    def get_contextual_tweets(self, time_interval, num_tweets):
      context = self.transcript[time_interval]
      similarity = self.get_most_similar_tweet(time_interval, context)
      similarity.sort(key=lambda tup: tup[0], reverse=True)
      op_text = context + "<br><br>"
      #sim_text = [ s[1] for s in similarity[0:num_tweets]]
      sim_text = []
      index = 0
      cnt = 0
      while cnt < num_tweets and index < len(similarity):
        if similarity[index][1] not in sim_text:
          sim_text.append(similarity[index][1])
          cnt += 1
        index +=1   

      for st in sim_text:
        try:
          op_text += st + "<br>"
        except:
          pass
      return op_text

        

class SetLabelHandler(BaseHandler):
    def get(self):
        tweet_id = self.get_argument("tweetid")
        tweet_label = self.get_argument("label")
        nickname = self.get_cookie("nickname")
        ip = self.request.remote_ip 
        q = "UPDATE rtweets set label = '"+tweet_label +"', ip = '"+ ip +"' where id = '"+ tweet_id + "'"
        self.db.execute(q);
        q = "SELECT score from userinfo where nickname = '"+ nickname + "'"
        score = self.db.query(q);
        q = "UPDATE userinfo set score = " + str (int(score[0].score) + 1 ) +" where nickname = '"+ nickname + "'"
        self.db.execute(q);
        self.set_status(200)

class SetNicknameHandler(BaseHandler):
    def get(self):
        nickname = self.get_argument("nickname")
        ip = self.request.remote_ip 
        q = "insert into userinfo values ( '"+nickname +"', ip = '"+ ip +"', 0 )"
        self.set_cookie("nickname", nickname)
        self.db.execute(q);
        self.set_status(200)

class GetTweetHandler(BaseHandler):
    def get(self):        
        entry = self.db.query("SELECT * FROM rtweets where label LIKE '-' LIMIT 1");
        print entry[0]
        if not self.get_cookie("nickname"):
            resp = {'id': entry[0].id, 'text': entry[0].text}
        else:
            score = self.db.query("SELECT score from userinfo where nickname = '"+ self.get_cookie("nickname") + "'")
            resp = {'id': entry[0].id, 'text': entry[0].text, 'nickname': self.get_cookie("nickname"), 'score': score[0].score}      
        q = "UPDATE rtweets set label = '5' where id = '"+ entry[0].id + "'"
        self.db.execute(q);
        self.write(tornado.escape.json_encode(resp))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    logging.info("starting torando web server")
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
