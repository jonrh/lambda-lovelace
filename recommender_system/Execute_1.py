from Recommender import Recommender 

number_of_recommendations = 70 
tweet_two = 'tweet one two' 
tweet_one = 'tweet one two three' 
tweet_four = 'tweet' 
tweet_three = 'tweet one' 
list_of_tweets = [tweet_three, tweet_four, tweet_one, tweet_two] 
users_tweets = ['tweet one', 'tweet two', 'tweet three'] 
 
recommender_object = Recommender("KOUIbWm4VWYzI0uuQLogzGRa0","r5Ac1fwLmuYFYL6biR4E1iYzS8S78DInUNM3AQ76EeMDBBVSFL","733308744638038017-oZYXhQOz1qUgTe2Sex3PctTMbkfM1dJ","3jAoAPk2krE9KClg4XC0MIDLlpAMKUumi6cDSnf5gtWJk") 
recommended_tweets = recommender_object.generate(number_of_recommendations, None, None) 

print(" *** ")
print(" *** ")
print(" Recommended set: ")
print(" *** ")
print(" *** ")
for tweet in recommended_tweets:
    print(tweet.text.encode('utf-8'))