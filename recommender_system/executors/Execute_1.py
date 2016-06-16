 
from Recommender import Recommender 
 
number_of_recommendations = 4 
tweet_two = 'tweet one two' 
tweet_one = 'tweet one two three' 
tweet_four = 'tweet' 
tweet_three = 'tweet one' 
list_of_tweets = [tweet_three, tweet_four, tweet_one, tweet_two] 
users_tweets = ['tweet one', 'tweet two', 'tweet three'] 
 
recommender_object = Recommender(list_of_tweets) 
recommended_tweets = recommender_object.generate(users_tweets, number_of_recommendations, None, None) 
 
print(recommended_tweets) 
 
#The below is simply commented out code that this file was originally used for. 
#As this is simply a test file, there is little point in removing it when I could use it later  
index on master: bef4397 Added MVP section to project plan