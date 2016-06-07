import tweepy

from Recommender import Recommender

from bottle import route, run, template

tweet_two = 'tweet one two'
tweet_one = 'tweet one two three'
tweet_four = 'tweet'
tweet_three = 'tweet one'
list_of_tweets = [tweet_three, tweet_four, tweet_one, tweet_two]
users_tweets = ['tweet one', 'tweet two', 'tweet three']

recommender_object = Recommender(list_of_tweets)
recommended_tweets = recommender_object.generate(users_tweets, 3, None, None)

print(recommended_tweets)

#The below is simply commented out code that this file was originally used for.
#As this is simply a test file, there is little point in removing it when I could use it later 
#(And this is my sandbox so I am the King of this file).

#Use the following url to use the test accounts details to login with all the keys/tokens
#localhost:8088/auth/KOUIbWm4VWYzI0uuQLogzGRa0/r5Ac1fwLmuYFYL6biR4E1iYzS8S78DInUNM3AQ76EeMDBBVSFL/733308744638038017-oZYXhQOz1qUgTe2Sex3PctTMbkfM1dJ/3jAoAPk2krE9KClg4XC0MIDLlpAMKUumi6cDSnf5gtWJk

'''@route('/auth/<ckey>/<csecret>/<atoken>/<atokensecret>')
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
 following = api.friends()
 dict_of_followed_tweets = {}
 for friend in following:
   follow_acc = api.get_user(friend.screen_name)
   dict_of_followed_tweets[friend.screen_name] = friend.timeline()

 recommenderObj = Recommender()
 generatedTweet = recommenderObj.generate(my_tweets, 1, following, 2, dict_of_followed_tweets)

 return template('Result: {{generatedTweetHere}}',generatedTweetHere =generatedTweet)

run(host='localhost', port=8088, debug=True)'''