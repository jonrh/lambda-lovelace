#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, redirect, request, Response, jsonify
from flask_restful import Resource, Api
import tweepy
import json
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from recommender import Recommender
import rethinkdb as r
import os
from RecommenderTextual import RecommenderTextual
from datetime import datetime

app = Flask(__name__)
api = Api(app)

consumer_key    = "BbTvs8T7CZguiloHMIVeRdKUO"
consumer_secret = "Ji9JyeCKRrY9DUhE0ry0wWpYcVxJMHyOheqGc62VJOB4UsBXZy"
#consumer_key = 'WtxItBWIIw35Ei1tQ4Zrmkybk'
#consumer_secret = '7KV0Mmg1P7qrIrYCeeRB5V1nKrVRK0r3PQiy7RwNWYTCDxNevH'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

class UserTimeline(Resource):
    def get(self):

        # access_token = request.headers['oauth_token']
        # access_token_secret = request.headers['oauth_token_secret']
        access_token = request.args.get('oauth_token')
        access_token_secret = request.args.get('oauth_token_secret')

        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        #fetch 100 tweets from user's timeline
        user_tweets = [tweet._json for tweet in tweepy.Cursor(api.user_timeline, count=200).items(100)]
        tweets_texts = [tweet['text'] for tweet in user_tweets]

        #generate a list of stop words
        stop_words = [word for word in CountVectorizer(stop_words='english').get_stop_words()]
        stop_words.append('rt')
        stop_words.append('https')

        #tokenize words, convert to lowercase, filter out stop words
        tokenize = CountVectorizer().build_tokenizer()
        words = [word.lower() for sentence in tweets_texts
                                for word in tokenize(sentence)
                                    if len(word.lower()) > 1 and word.lower() not in stop_words]

        #count term frequency
        c = Counter(words)
        word_counts = c.most_common()
        word_counts[:5]

        #search for 100 tweets from the account that the user is not following
        unfollowed_tweets = [tweet._json['text'] for tweet in tweepy.Cursor(api.search, q=word_counts[0][0], count=200,lang='en').items(100)]

        #return results
        results = {}
        results['user_tweets'] = user_tweets
        results['word_count'] = word_counts[:5]
        results['unfollowed_tweets'] = unfollowed_tweets

        return jsonify(results)



class HomeTimeline(Resource):
    def get(self):

        # access_token = request.headers['oauth_token']
        # access_token_secret = request.headers['oauth_token_secret']
        access_token = request.args.get('oauth_token')
        access_token_secret = request.args.get('oauth_token_secret')

        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        #fetch 100 tweets from user
        home_tweets = [tweet._json for tweet in tweepy.Cursor(api.home_timeline, count=200).items(100)]

        return jsonify(home_tweets)

class Tweets(Resource):
    def get(self):

        access_token = request.args.get('oauth_token')
        access_token_secret = request.args.get('oauth_token_secret')
        page = request.args.get('page')

        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        # tweets = [tweet._json for tweet in tweepy.Cursor(api.home_timeline, count=200).items()]
        tweets = [tweet._json for tweet in api.home_timeline(page=page)]

        return jsonify(tweets)

#The recommend system part
class RecommendTweets(Resource):
    def get(self):

        access_token = request.args.get('oauth_token')
        access_token_secret = request.args.get('oauth_token_secret')
        page = request.args.get('page')
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        
        #get user's information
        user = api.me()

        #connect database
        r.connect(host='ec2-52-51-162-183.eu-west-1.compute.amazonaws.com', port=28015, db='lovelace', password="marcgoestothegym").repl()

        #get a list of screen_names
        users = list(r.db('lovelace').table('tweets').get_field('screen_name').run())

        #user's screen_name
        screen_name = user._json['screen_name']

        #get user's own timeline
        user_tweets = [tweet._json for tweet in api.user_timeline(count=50)]

        home_tweets = []

        #if true, then this is the first time user uses this app
        #so we first get tweets directly from twitter API
        if screen_name not in users:
            home_tweets = [tweet._json for tweet in api.home_timeline(count=50)
                           if tweet._json['user']['screen_name'] != screen_name]

            for item in home_tweets:
                r.db('lovelace').table('tweets').insert({'screen_name': screen_name,'tweet_id':item['id'], 'tweet': item}).run()

            r.db('lovelace').table('user_tokens').insert({'access_secret':access_token_secret,
                                                          'access_token':access_token,
                                                          'consumer_key':consumer_key,
                                                          'consumer_secret':consumer_secret,
                                                          'screen_name':screen_name,
                                                          'created_at':r.now().to_epoch_time().run()}).run()

        #if not, we get tweets directly from database
        else:
            data = r.db('lovelace').table('tweets').order_by(r.desc('tweet_id')).group('screen_name').limit(50).run()
            tweets = data[screen_name]
            r.db('lovelace').table('user_tokens').insert({'access_secret': access_token_secret,
                                                          'access_token': access_token,
                                                          'consumer_key': consumer_key,
                                                          'consumer_secret': consumer_secret,
                                                          'screen_name': screen_name,
                                                          'created_at': r.now().to_epoch_time().run()}).run()

            home_tweets = [tweet['tweet'] for tweet in tweets
                           if tweet['tweet']['user']['screen_name'] != screen_name]

        # #fetch tweets of user's own time line
        # #TO-DO: Can this be removed now? It is no longer used when initialising the Recommmender Object.
        # users_tweets = [tweet._json for tweet in tweepy.Cursor(api.user_timeline, count=50).items(50)]
        #
        # #filter out the tweets that the user tweeted from the home timeline
        # #TO-DO: Can this be removed now? It is no longer used when initialising the Recommmender Object.
        # followed_tweets = [tweet for tweet in home_tweets if tweet['user']['screen_name'] != user._json['screen_name']]
        
        #give the user timeline and home timeline to the recommender system to make recommendation
        print(home_tweets)
        recommender_object = RecommenderTextual(user_tweets, home_tweets)
        recommended_tweets = recommender_object.generate(50, None)
        # print(recommended_tweets)
        # return "Hello world!"
        return jsonify(recommended_tweets)


class IOSAppRedirectHelper(Resource):
    def get(self):
        oauth_token = request.args.get('oauth_token')
        oauth_verifier = request.args.get('oauth_verifier')
        
        location = 'lovelace://oauth-callback?oauth_token='
        location += oauth_token
        location += '&oauth_verifier='
        location += oauth_verifier
        return redirect(location)


@app.route("/")
def hello():
    version = os.getenv("LLVERSION", "N/A")
    return "Hello λ Lovelace! Version: "+ version

# test
# ios twitter authentication callback url redirect helper
api.add_resource(IOSAppRedirectHelper, '/oauth-callback')

api.add_resource(UserTimeline, '/user_timeline')
api.add_resource(HomeTimeline, '/home_timeline')
api.add_resource(Tweets, '/tweets')
api.add_resource(RecommendTweets, '/recommend')

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 80)
