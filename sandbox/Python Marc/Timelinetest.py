
def count_bag(n, arg_here):
	print(arg_here)
	return n + 1

x = sorted([1,2,34,45,2], key=count_bag "arg matey!", reverse=True)






'''from sklearn.feature_extraction.text import CountVectorizer
import tweepy 


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
fave_tweets = api.favorites()

for x in fave_tweets:
	print(x.text)'''