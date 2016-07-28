#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, redirect, request, Response, jsonify
from flask import got_request_exception  # For Rollbar logging
from flask_restful import Resource, Api
import tweepy
import json
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from recommender import Recommender
import rethinkdb as r
from RecommenderTextual import RecommenderTextual
import os  # For environment variables and Rollbar logging
import rollbar
import rollbar.contrib.flask

app = Flask(__name__)
api = Api(app)


# =============================================================================
# Setup for Rollbar, our error logging service. This should be all that is
# required to catch all errors and exceptions that ocurr in our program. To
# view them see https://rollbar.com/lambda-lovelace/Lambda-Lovelace-Backend/
# The team members should have an account.
# =============================================================================
@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token for the demo app: https://rollbar.com/demo
        "9a41d7e8fdbb49cead0cae434765a927",
        # environment name, production for now, maybe we want to change this
        # to a configurable environment variable later, e.g. environment for
        # each branch
        'production',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
# =============================================================================

consumer_key = "BbTvs8T7CZguiloHMIVeRdKUO"
consumer_secret = "Ji9JyeCKRrY9DUhE0ry0wWpYcVxJMHyOheqGc62VJOB4UsBXZy"
# consumer_key = 'WtxItBWIIw35Ei1tQ4Zrmkybk'
# consumer_secret = '7KV0Mmg1P7qrIrYCeeRB5V1nKrVRK0r3PQiy7RwNWYTCDxNevH'

# The recommend system part
class RecommendTweets(Resource):
    def get(self):
        access_token = request.args.get('oauth_token')
        access_token_secret = request.args.get('oauth_token_secret')
        page = request.args.get('page')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api_flask = tweepy.API(auth)

        # get user's information
        user = api_flask.me()

        # connect database
        r.connect(host='ec2-52-51-162-183.eu-west-1.compute.amazonaws.com', port=28015, db='lovelace',
                  password="marcgoestothegym").repl()

        # get a list of screen_names
        users = list(r.db('lovelace').table('user_tokens').get_field('screen_name').run())

        # user's screen_name
        screen_name = user._json['screen_name']
        print(1233333)
        print(screen_name)
        # get user's own timeline
        user_tweets = [tweet._json for tweet in api_flask.user_timeline(count=50)]

        home_tweets = []

        # if true, then this is the first time user uses this app
        # so we first get tweets directly from twitter API
        if screen_name not in users:
            home_tweets = [tweet._json for tweet in api_flask.home_timeline(count=50)
                           if tweet._json['user']['screen_name'] != screen_name]

            for item in home_tweets:
                r.db('lovelace').table('tweets').insert(
                    {'screen_name': screen_name, 'tweet_id': item['id'], 'tweet': item}).run()

            r.db('lovelace').table('user_tokens').insert({'access_secret': access_token_secret,
                                                          'access_token': access_token,
                                                          'consumer_key': consumer_key,
                                                          'consumer_secret': consumer_secret,
                                                          'screen_name': screen_name,
                                                          'created_at': r.now().to_epoch_time().run()}).run()

        # if not, we get tweets directly from database
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

        # give the user timeline and home timeline to the recommender system to make recommendation
#        print("Home tweets count: " + str(len(home_tweets)))
        recommender_object = RecommenderTextual(user_tweets, home_tweets)
        recommended_tweets = recommender_object.generate(50, 1)
#        print("Recommended tweet count: " + str(len(recommended_tweets)))

        return jsonify(recommended_tweets)
#        return screen_name

# The original tweet part
class EvaluationData(Resource):
    def get(self):
        access_token = request.args.get('oauth_token')
        access_token_secret = request.args.get('oauth_token_secret')
        page = request.args.get('page')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        home_tweets = [tweet._json for tweet in api.home_timeline(count=200, page=page)]
        
        user_tweets = [tweet._json for tweet in api.user_timeline(count=50)]
        
        recommender_object = RecommenderTextual(user_tweets, home_tweets)
        recommended_tweets = recommender_object.generate(200, 1)

        return jsonify({"original_tweets":home_tweets, "recommend_tweets":recommended_tweets["recommended_tweets"]})


class IOSAppRedirectHelper(Resource):
    def get(self):
        oauth_token = request.args.get('oauth_token')
        oauth_verifier = request.args.get('oauth_verifier')

        location = 'lovelace://oauth-callback?oauth_token='
        location += oauth_token
        location += '&oauth_verifier='
        location += oauth_verifier
        return redirect(location)

#Evaluation part
class EvaluationResult(Resource):
    def put(self):
        
        jsonData = request.get_json()
        access_token = jsonData['oauthToken']
        access_token_secret = jsonData['oauthTokenSecret']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api_flask = tweepy.API(auth)
        
        me = api_flask.me()
        
        screen_name = me._json['screen_name']
        following_count = me._json['friends_count']
        liked_count = me._json['favourites_count']
        tweets_of_me = me._json['statuses_count']
        
        jsonData['screen_name'] = screen_name
        jsonData['following_count'] = following_count
        jsonData['liked_count'] = liked_count
        jsonData['tweets_of_me'] = tweets_of_me
        
        del jsonData['oauthToken']
        del jsonData['oauthTokenSecret']
        
        r.connect(host='ec2-52-51-162-183.eu-west-1.compute.amazonaws.com', port=28015, db='lovelace',
                  password="marcgoestothegym").repl()

        r.db('evaluation').table('results').insert(jsonData).run()
                  
        return jsonData

# An endpoint to test if errors are correctly being transmitted to Rollbar
@app.route("/error")
def error():
    print "In /error"
    x = None
    x[5]
    return "We won't get to here!"


# A test endpoint so we know which version is currently running
@app.route("/")
def hello():
    buildnumber = os.getenv("JENKINS_BUILDNUMBER", "N/A")
    githash = os.getenv("GITHASH", "N/A")
    return "<p>Hello λ Lovelace!</p><p>Jenkins build number: " + buildnumber + "<br /> Git hash: " + githash + "</p>"


# test
# ios twitter authentication callback url redirect helper
api.add_resource(IOSAppRedirectHelper, '/oauth-callback')

api.add_resource(RecommendTweets, '/recommend')
api.add_resource(EvaluationData, '/evaluationData')

api.add_resource(EvaluationResult, '/evaluationResult')

if __name__ == '__main__':
    # If for some reason there was an issue starting the Flask server, report
    # it to Rollbar.
    try:
        app.run(host="0.0.0.0", port=80)  # Production
        # app.run(host="127.0.0.1", port=5000)  # Local debugging
    except:
        rollbar.report_exc_info()

