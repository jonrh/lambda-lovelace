import tweepy


from recommender import Recommender

from bottle import route, run, template

#Use the following url to use the test accounts details to login with all the keys/tokens
#localhost:8088/auth/KOUIbWm4VWYzI0uuQLogzGRa0/r5Ac1fwLmuYFYL6biR4E1iYzS8S78DInUNM3AQ76EeMDBBVSFL/733308744638038017-oZYXhQOz1qUgTe2Sex3PctTMbkfM1dJ/3jAoAPk2krE9KClg4XC0MIDLlpAMKUumi6cDSnf5gtWJk

@route('/auth/<ckey>/<csecret>/<atoken>/<atokensecret>/<topic>')
def authentication(ckey, csecret, atoken, atokensecret, topic):
 consumer_key = ckey
 consumer_secret = csecret
 access_token = atoken
 access_token_secret = atokensecret

 auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
 auth.set_access_token(access_token, access_token_secret)

 api = tweepy.API(auth)
 results = [ status._json for status in tweepy.Cursor(api.search,
                           q=topic,
                           count=1000).items(1000)]

 my_tweets = api.user_timeline()
 my_first_tweet = my_tweets[0].text
 following = api.followers()

 recommenderObj = Recommender()
 generatedTweet = recommenderObj.generate(my_tweets, 1, following, 2)
 accounts_recommend = recommenderObj.accounts_recommender(results)
 user_mentions = [ mention[0] for mention in accounts_recommend[0]]
 users_mentions_counts = [mention[1] for mention in accounts_recommend[0]]
 users = [user[0] for user in accounts_recommend[1]]
 users_counts = [user[1] for user in accounts_recommend[1]]

 return template("My first Tweet was: {{my_first_tweet_here}}, my generated text is {{generatedTweetHere}}"
                 "Your Topic is: {{tweets_topic}}."
                 "Here are some accounts that you may interested in:"
                 "Among all the tweets:"
                 "@{{first_mention}} was mentioned {{first_metion_count}} times."
                 "@{{second_mention}} was mentioned {{second_metion_count}} times."
                 "@{{third_mention}} was mentioned {{third_metion_count}} times."
                 "{{first_user_count}} of @{{first_user}}'s tweets are about {{tweets_topic}}."
                 "{{second_user_count}} of @{{second_user}}'s tweets are about {{tweets_topic}}."
                 "{{third_user_count}} of @{{third_user}}'s tweets are about {{tweets_topic}}."
                 ,
                 my_first_tweet_here = my_first_tweet,
                 generatedTweetHere = generatedTweet,
                 tweets_topic = topic,
                 first_mention = user_mentions[0],
                 second_mention = user_mentions[1],
                 third_mention = user_mentions[2],
                 first_metion_count = users_mentions_counts[0],
                 second_metion_count = users_mentions_counts[1],
                 third_metion_count = users_mentions_counts[2],
                 first_user_count = users_counts[0],
                 second_user_count = users_counts[1],
                 third_user_count = users_counts[2],
                 first_user = users[0],
                 second_user = users[1],
                 third_user = users[2])

run(host='localhost', port=8088, debug=True)