#from ... 
#from . import RecommenderTextual
from .Executors import RecommenderTextual
from sklearn.feature_extraction.text import CountVectorizer
import tweepy 

number_of_recommendations = 70 

consumer_key = "KOUIbWm4VWYzI0uuQLogzGRa0"
consumer_secret = "r5Ac1fwLmuYFYL6biR4E1iYzS8S78DInUNM3AQ76EeMDBBVSFL"
at = "733308744638038017-oZYXhQOz1qUgTe2Sex3PctTMbkfM1dJ"
ats = "3jAoAPk2krE9KClg4XC0MIDLlpAMKUumi6cDSnf5gtWJk"

vectorizer = CountVectorizer()

access_token = at
access_token_secret = ats
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

users_tweets = api.user_timeline()
followed_tweets = api.home_timeline()

recommender_object = RecommenderTextual(users_tweets, followed_tweets) 
recommended_tweets = recommender_object.generate(number_of_recommendations, None) 

print(" *** ")
print(" *** ")
print(" Recommended set: ")
print(" *** ")
print(" *** ")
for tweet in recommended_tweets:
    print(tweet.text.encode('utf-8'))