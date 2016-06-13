from flask import Flask, redirect, request
from flask_restful import Resource, Api
import tweepy

app = Flask(__name__)
api = Api(app)

consumer_key    = "BbTvs8T7CZguiloHMIVeRdKUO"
consumer_secret = "Ji9JyeCKRrY9DUhE0ry0wWpYcVxJMHyOheqGc62VJOB4UsBXZy"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

tweets = {
    'tweet1': {'content': 'this is test tweet'},
    'tweet2': {'content': 'this is test tweet'},
    'tweet3': {'content': 'this is test tweet'},
}

class Tweets(Resource):
    def get(self):
        access_token = request.headers["oauth_token"]
        access_token_secret = request.headers["oauth_token_secret"]

        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)

        public_tweets = api.home_timeline()
        for tweet in public_tweets:
            print(tweet.text)
        return public_tweets

class IOSAppRedirectHelper(Resource):
    def get(self):
        oauth_token = request.args.get('oauth_token')
        oauth_verifier = request.args.get('oauth_verifier')

        location = 'lovelace://oauth-callback?oauth_token='
        location += oauth_token
        location += '&oauth_verifier='
        location += oauth_verifier
        return redirect(location)



# ios twitter authentication callback url redirect helper
api.add_resource(IOSAppRedirectHelper, '/oauth-callback')

api.add_resource(Tweets, '/tweets')

if __name__ == '__main__':
    app.run()
