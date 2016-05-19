import tweepy

from recommender import Recommender

from bottle import route, run, template

#Use the following url to use the test accounts details to login with all the keys/tokens
#localhost:8088/auth/KOUIbWm4VWYzI0uuQLogzGRa0/r5Ac1fwLmuYFYL6biR4E1iYzS8S78DInUNM3AQ76EeMDBBVSFL/733308744638038017-oZYXhQOz1qUgTe2Sex3PctTMbkfM1dJ/3jAoAPk2krE9KClg4XC0MIDLlpAMKUumi6cDSnf5gtWJk

@route('/auth/<ckey>/<csecret>/<atoken>/<atokensecret>')
def authentication(ckey, csecret, atoken, atokensecret):
 consumer_key = ckey
 consumer_secret = csecret
 access_token = atoken
 access_token_secret = atokensecret

 auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
 auth.set_access_token(access_token, access_token_secret)

 api = tweepy.API(auth)
 my_tweets = api.user_timeline()
 my_first_tweet = my_tweets[0].text
 following = api.followers()

 recommenderObj = Recommender()
 generatedTweet = recommenderObj.generate(my_tweets, 1, following, 2)

 return template('My first Tweet was: {{my_first_tweet_here}}, my generated text is {{generatedTweetHere}}', my_first_tweet_here = my_first_tweet, generatedTweetHere =generatedTweet)

run(host='localhost', port=8088, debug=True)