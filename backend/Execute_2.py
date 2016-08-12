from RecommenderTextual import RecommenderTextual
from sklearn.feature_extraction.text import CountVectorizer
import tweepy 

number_of_recommendations = 35

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
followed_tweets = api.home_timeline(count =35)

feedback = [{
"feedback":  "like" ,
"followerScreenName":  "SwiftOnSecurity" ,
"id":  "5ffcdb2d-4917-46d3-84f0-e64256c7a044" ,
"reason":  "subject" ,
"tweetContent": "RT @AnselLindner: The problem is that java was regulated. Changed their security model after a year long investigation by CFTC! https:/" ,
"user_name":  "specter4mjy"
}, {
"feedback":  "dislike" ,
"followerScreenName":  "pritch1963" ,
"id":  "22cce6eb-a72f-4a68-87c1-ccc72e5fe39f" ,
"reason":  "subject" ,
"tweetContent": "RT @1_Aimee_: @andyvblue @bluehand007 @MissPurple5 @pritch1963 java very safe last night, was it?" ,
"user_name":  "lambda_lovelace"
}, {
"feedback":  "dislike" ,
"followerScreenName":  "java" ,
"id":  "10f35fb5-3603-419f-a78f-150a1f15e9cc" ,
"reason":  "subject" ,
"tweetContent":  "RT @Fishrock123: .@nodejs TSC java ruby ruby live now: https://t.co/cXAr2UngT7" ,
"user_name":  "lambda_lovelace"
}, {
"feedback":  "like" ,
"followerScreenName":  "javacodegeeks" ,
"id":  "66b1fc9a-0d5e-4b35-9e9d-58bb81630a04" ,
"reason":  "subject" ,
"tweetContent": "RT @Minorcomplaint: @pritch1963 java @unicorns88_jazz @MissPurple5 @BBCNews fucksakes I'm usually great at pub quizzes... ok, sc" ,
"user_name":  "lambda_lovelace"
}, {
"feedback":  "like" ,
"followerScreenName":  "javacodegeeks" ,
"id":  "c073b857-8789-4a79-bc1a-db6605d15241" ,
"reason":  "subject" ,
"tweetContent": "RT @robheghan: Do you want to know how a persistent array is implemented in @elmlang ? Check this out: https://t.co/QxSh7wchL1" ,
"user_name":  "jonrh"
}, {
"feedback":  "like" ,
"followerScreenName":  "javacodegeeks" ,
"id":  "41f9dd0c-4a73-4d17-ae56-e97e06e678f2" ,
"reason":  "subject" ,
"tweetContent":  "RT @trash_ebooks: STEM: I spent my java prime in java a computer lab so later I could debug a dating app Humanities: I lived in a shed so I co" ,
"user_name":  "xinqili123"
}, {
"feedback":  "dislike" ,
"followerScreenName":  "SwiftOnSecurity" ,
"id":  "4c6559b6-d5b6-4031-96cd-9f25e3b02371" ,
"reason":  "author" ,
"tweetContent": "RT @AnselLindner: The problem is that bitfinex was regulated. Changed their security model after a year long investigation by CFTC! https:/" ,
"user_name":  "specter4mjy"
}]
recommender_object = RecommenderTextual(users_tweets, followed_tweets, feedback) 
recommended_tweets = recommender_object.generate(number_of_recommendations, 3) 

print(" *** ")
print(" *** ")
print(" Recommended set: ")
print(" *** ")
print(" *** ")

for tweet in recommended_tweets["recommended_tweets"]:#Generate now returns the original tweets AND a counter
    print(tweet.text.encode('utf-8'))