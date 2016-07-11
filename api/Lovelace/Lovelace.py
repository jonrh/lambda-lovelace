from flask import Flask, redirect, request, Response, jsonify
from flask_restful import Resource, Api
import tweepy
import json
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from recommender import Recommender

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
        
        #fetch tweets of user's home timeline
        home_tweets = [tweet._json for tweet in api.home_timeline(count=50,page=page)]
        
        #fetch tweets of user's own time line
        #TO-DO: Can this be removed now? It is no longer used when initialising the Recommmender Object.
        users_tweets = [tweet._json for tweet in tweepy.Cursor(api.user_timeline, count=50).items(50)]
        
        #filter out the tweets that the user tweeted from the home timeline
        #TO-DO: Can this be removed now? It is no longer used when initialising the Recommmender Object.
        followed_tweets = [tweet for tweet in home_tweets if tweet['user']['screen_name'] != user._json['screen_name']]
        
        #give the user timeline and home timeline to the recommender system to make recommendation
        recommender_object = Recommender(consumer_key, consumer_secret, access_token, access_token_secret) 
        recommended_tweets = recommender_object.generate(3, None, None)
        
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



# test
# ios twitter authentication callback url redirect helper
api.add_resource(IOSAppRedirectHelper, '/oauth-callback')

api.add_resource(UserTimeline, '/user_timeline')
api.add_resource(HomeTimeline, '/home_timeline')
api.add_resource(Tweets, '/tweets')
api.add_resource(RecommendTweets, '/recommend')


if __name__ == '__main__':
    app.run()
