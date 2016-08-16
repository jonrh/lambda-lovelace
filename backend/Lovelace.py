#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, redirect, request, Response, jsonify
from flask import got_request_exception  # For Rollbar logging
from flask_restful import Resource, Api
import tweepy
import rethinkdb as r
from RecommenderTextual import RecommenderTextual
import os  # For environment variables and Rollbar logging
import rollbar
import rollbar.contrib.flask

app = Flask(__name__)
api = Api(app)


# =============================================================================
# Setup for Rollbar, our error logging service. This should be all that is
# required to catch all errors and exceptions that occur in our program. To
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

countOfReturnTweets = 200

"""This class handles the recommend request from the iOS client.
Basically, when the Flask server receives /recommend request from iOS client,
it'll check if the user logs in for the first time or not.

If so, it'll get tweets from twitter directly then save it into database.

If the user has logged in and has not logged out, it'll get tweets data
from database instead of from twitter API.

If the user has logged out, but re-logged in within 15 min after he/she has logged out,
it'll still get tweets from database.

If the user has logged out for a long time (more than 15min), when she/he re-log in,
it'll get tweets data from twitter api, because when the user logs out for more than
15 minutes, Celery will stop fetching data for the user. The tweets in the database may
be a bit old.
"""
class RecommendTweets(Resource):
    def get(self):

        # authentication
        access_token = request.args.get('oauth_token')
        access_token_secret = request.args.get('oauth_token_secret')
        page = int(request.args.get('page'))
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api_flask = tweepy.API(auth)


        # connect database
        r.connect(host='ec2-52-51-162-183.eu-west-1.compute.amazonaws.com', port=28015, db='lovelace',
                  password="marcgoestothegym").repl()

        # get a list of screen_names, i.e. users that have logged into our app
        users = list(r.db('lovelace').table('user_tokens').get_field('screen_name').run())

        # get user's screen_name which was returned from iOS client
        screen_name = request.args.get('currentUserScreenName') or "NoUserNameFound"
        rollbar.report_message(screen_name + "request tweets of page: " + str(page), "debug")

        # list of user's own tweets
        user_tweets = []

        # list of user's home timeline
        home_tweets = []

        # Check if this is the first time the user uses our app
        # if true, we get data from twitter API and save it into database
        if screen_name not in users:

            # get user's home timline and get rid of user's own tweets
            home_tweets = [tweet._json for tweet in api_flask.home_timeline(count=200)
                           if tweet._json['user']['screen_name'] != screen_name]

            # save each tweet into database
            for item in home_tweets:
                r.db('lovelace').table('tweets').insert(
                    {'screen_name': screen_name, 'tweet_id': item['id_str'], 'tweet': item}).run()

            # get liked tweets of the users
            liked_tweets = [liked_tweet._json for liked_tweet in api_flask.favorites(count=200)]
            print(len(liked_tweets))

            # save each liked tweet into database
            for item in liked_tweets:
                r.db('lovelace').table('like_user_timeline').insert(
                    {'screen_name': screen_name, 'tweet_id': item['id_str'], 'type': 'like', 'tweet': item}).run()

            # get user's own timeline
            user_tweets = [user_tweet._json for user_tweet in tweepy.Cursor(api_flask.user_timeline, count=200).items(1000)]

            # save each tweet into database
            for item in user_tweets:
                r.db('lovelace').table('like_user_timeline').insert(
                    {'screen_name': screen_name, 'tweet_id': item['id_str'], 'type': 'user', 'tweet': item}).run()

            # combine user's own tweets and liked tweets together
            # for recommender system to use
            user_tweets = user_tweets + liked_tweets

            # Add this user into the database which contains a list of users
            # we should regularly fetch tweets of this user from now on
            r.db('lovelace').table('user_tokens').insert({'access_secret': access_token_secret,
                                                          'access_token': access_token,
                                                          'consumer_key': consumer_key,
                                                          'consumer_secret': consumer_secret,
                                                          'screen_name': screen_name,
                                                          'last_login': r.now().to_epoch_time().run(),
                                                          'last_logout': None,
                                                          'fetch_status': True}).run()

        # if the user is not using the app for the first time
        else:

            # get user info from database
            user = r.db('lovelace').table('user_tokens').get(screen_name).run()

            # get current time
            current_time = r.now().to_epoch_time().run()

            # check if the user has logged out or not
            # if "fetch_status" equals True, then the
            # user has not logged out, so we get tweets from database
            if user['fetch_status'] == True:

                # get user's home timeline from database
                tweets = r.db('lovelace').table('tweets').order_by(r.desc('tweet_id')).filter(
                    {'screen_name': screen_name}).slice(countOfReturnTweets * (page - 1), countOfReturnTweets * page).run()

                # convert the result returned from database into a list
                home_tweets = [tweet['tweet'] for tweet in tweets
                               if tweet['tweet']['user']['screen_name'] != screen_name]

                # get user's own timeline and user's liked tweets
                user_data = r.db('lovelace').table('like_user_timeline').group('screen_name').limit(2000).run()
                raw_user_tweets = user_data[screen_name]
                user_tweets = [user_tweet['tweet'] for user_tweet in raw_user_tweets]

            # if "fetch_status" equals false, then the user has logged out
            # if current time minus "last_logout" is less than 900 seconds
            # it means the user re-logs in within 15 minutes after he/she logs out
            # so we still get tweets data from database
            elif user['last_logout'] is None or (current_time - user['last_logout']) <= 900:

                # get user's home timeline from database
                tweets = r.db('lovelace').table('tweets').order_by(r.desc('tweet_id')).filter(
                    {'screen_name': screen_name}).slice(countOfReturnTweets * (page - 1), countOfReturnTweets * page).run()

                # convert the result returned from database into a list
                home_tweets = [tweet['tweet'] for tweet in tweets
                               if tweet['tweet']['user']['screen_name'] != screen_name]

                # get user's own timeline and user's liked tweets
                user_data = r.db('lovelace').table('like_user_timeline').group('screen_name').limit(2000).run()
                raw_user_tweets = user_data[screen_name]
                user_tweets = [user_tweet['tweet'] for user_tweet in raw_user_tweets]

                # update the "fetch_status" to True again,
                # indicates that the user has logged in again
                r.db('lovelace').table('user_tokens').update({'screen_name': screen_name,
                                                              'fetch_status': True}).run()
            # if the "fetch_status" equals false but if current time
            # minus "last_logout" is more than 900 seconds
            # it means the user has logged out for a long time
            # tweets of the user in the database may be a bit old
            # so we get tweets data from twitter API again
            else:
                print('put of 15 min, get from twitter api')
                home_tweets = [tweet._json for tweet in api_flask.home_timeline(count=50)
                               if tweet._json['user']['screen_name'] != screen_name]
                for item in home_tweets:
                    r.db('lovelace').table('tweets').insert(
                        {'screen_name': screen_name, 'tweet_id': item['id_str'], 'tweet': item}).run()

                r.db('lovelace').table('user_tokens').update({'screen_name': screen_name,
                                                              'last_login': r.now().to_epoch_time().run(),
                                                              'fetch_status': True}).run()

                # get user liked tweets
                liked_tweets = [liked_tweet._json for liked_tweet in api_flask.favorites(count=200)]

                for item in liked_tweets:
                    r.db('lovelace').table('like_user_timeline').insert(
                        {'screen_name': screen_name, 'tweet_id': item['id_str'], 'type': 'like', 'tweet': item}).run()

                # get user timeline
                user_tweets = [user_tweet._json for user_tweet in
                               tweepy.Cursor(api.user_timeline, count=200).items(1000)]

                for item in user_tweets:
                    r.db('lovelace').table('tweets').insert(
                        {'screen_name': screen_name, 'tweet_id': item['id_str'], 'type': 'user', 'tweet': item}).run()

                user_tweets = user_tweets + liked_tweets

        # get single feedback from database
        # single feedback is the data of like/dislike function in our app
        single_feedback = r.db('lovelace').table('single_feedback').filter({"user_name":screen_name}).run()

        # give the user timeline + liked tweets and home timeline to the recommender system to make recommendation
        recommender_object = RecommenderTextual(user_tweets, home_tweets, single_feedback)
        recommended_tweets = recommender_object.generate(50, 7)

        return jsonify(recommended_tweets)


# The original tweet part
class EvaluationData(Resource):
    def get(self):
        access_token = request.args.get('oauth_token')
        access_token_secret = request.args.get('oauth_token_secret')
        page = int(request.args.get('page'))
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api_flask = tweepy.API(auth)


        home_tweets = [tweet._json for tweet in tweepy.Cursor(api_flask.home_timeline, count=200).items(800)]
        user_tweets = [tweet._json for tweet in tweepy.Cursor(api_flask.user_timeline, count=200).items(3200)]
        liked_tweets = [tweet._json for tweet in tweepy.Cursor(api_flask.favorites, count=200).items(3000)]

        user_tweets = user_tweets + liked_tweets

        r.connect(host='ec2-52-51-162-183.eu-west-1.compute.amazonaws.com', port=28015, db='lovelace',
                  password="marcgoestothegym").repl()
        #single feedback
        screen_name = request.args.get('currentUserScreenName')

        single_feedback = r.db('lovelace').table('single_feedback').filter({"user_name":screen_name}).run()

        recommender_object = RecommenderTextual(user_tweets, home_tweets, single_feedback)
        recommended_tweets = recommender_object.generate(200, 1)

        return jsonify({
            "original_tweets": home_tweets,
            "recommend_tweets": recommended_tweets["recommended_tweets"]
        })


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
        users_following = me._json['friends_count']
        tweets_liked = me._json['favourites_count']
        tweets_of_me = me._json['statuses_count']
        
        jsonData['user_info'] = {'screen_name':screen_name,
                                 'users_following':users_following,
                                 'tweets_liked':tweets_liked,
                                 'tweets_of_me':tweets_of_me}
        
        del jsonData['oauthToken']
        del jsonData['oauthTokenSecret']
        
        r.connect(host='ec2-52-51-162-183.eu-west-1.compute.amazonaws.com', port=28015, db='lovelace',
                  password="marcgoestothegym").repl()

        r.db('evaluation').table('results').insert(jsonData).run()
                  
        return jsonData


#Single tweet feedback
class SingleTweetFeedback(Resource):
    def put(self):

        jsonData = request.get_json()

        r.connect(host='ec2-52-51-162-183.eu-west-1.compute.amazonaws.com', port=28015, db='lovelace',
                  password="marcgoestothegym").repl()
            
        r.db('lovelace').table('single_feedback').insert(jsonData).run()
                  
        return jsonData


class UserProfile(Resource):
    def get(self):
        access_token = request.args.get('oauth_token')
        access_token_secret = request.args.get('oauth_token_secret')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api_flask = tweepy.API(auth)

        me = api_flask.me()
        return me._json

class UserLogout(Resource):
    def delete(self):
        access_token = request.args.get('oauth_token')
        access_token_secret = request.args.get('oauth_token_secret')
        screen_name = request.args.get('currentUserScreenName')

        # connect database
        r.connect(host='ec2-52-51-162-183.eu-west-1.compute.amazonaws.com', port=28015, db='lovelace',
                  password="marcgoestothegym").repl()

        r.db('lovelace').table('user_tokens').update({'screen_name': screen_name,
                                                      'fetch_status': False,
                                                      'last_logout': r.now().to_epoch_time().run()
                                                      }).run()

        rollbar.report_message(screen_name + "has logout" , "debug")
        return ""

@app.route("/error")
def error():
    """An endpoint to test if errors are correctly being transmitted to Rollbar"""
    x = None
    x[5]

    return "We won't get to here!"


@app.route("/")
def hello():
    """A test endpoint so we know which version is currently running"""
    buildnumber = os.getenv("JENKINS_BUILDNUMBER", "N/A")
    githash = os.getenv("GITHASH", "N/A")

    return "<p>Hello λ Lovelace!</p><p>Jenkins build number: " + buildnumber + "<br /> Git hash: " + githash + "</p>"


# test
# ios twitter authentication callback url redirect helper
api.add_resource(IOSAppRedirectHelper, '/oauth-callback')

api.add_resource(RecommendTweets, '/recommend')
api.add_resource(EvaluationData, '/evaluationData')
api.add_resource(SingleTweetFeedback, '/singleTweetFeedback')
api.add_resource(EvaluationResult, '/evaluationResult')
api.add_resource(UserProfile, '/userProfile')
api.add_resource(UserLogout, '/userLogout')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)  # Production
    # app.run(host="127.0.0.1", port=5000)  # Local debugging
