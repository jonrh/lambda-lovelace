from sklearn.feature_extraction.text import CountVectorizer
from Tweetbox import Tweetbox
from collections import Counter


class Recommender:
    
    def __init__(self):#, followed_tweets):
        #self.followed_tweets = followed_tweets
        self.vectorizer = CountVectorizer()
    
    def get_term_weightings(self, ckey, csecret, atoken, atokensecret):
        weightings = {}#Dictionary of terms (keys) and their weighting (value)
        top_amount_of_terms = 10
        amount_of_tweets_to_gather = 101#Extra "1" is because python is not inclusive of the last digit in the range that this variable is used for later on.
        consumer_key = ckey
        consumer_secret = csecret
        access_token = atoken
        access_token_secret = atokensecret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        #api = tweepy.API(auth)
        #my_tweets = api.user_timeline()

        #Filtering section
        my_first_x_tweets = my_tweets[0,amount_of_tweets_to_gather]
        overall_list = []
        for sublist in test: 
            for item in sublist.split():
            overall_list.append(item)
        
        term_frequencies = Counter(overall_list)
        top_x_terms = term_frequencies.most_common(top_amount_of_terms) 

        following = api.friends()
        self.vectorizer.fit_transform(my_first_x_tweets)
        terms = self.vectorizer.get_feature_names()
        
        #Recommendations section
        #Recommendations from accounts that the user does not follow. Use hashtags to achieve this with the keys in the users weightings. 

        #Streaming section
        #Streaming API stuff. Place really good ones (Lot's of retweets) here. 
        #Could leave this out since every time the app is refreshed it'll get new tweets. 
        #Could also leave as optional for the user, hidden away in some settings.

        return weightings

    def generate(self, user_tweets, number_of_recommendations, followed_accounts, how_many_days_ago):
        self.vectorizer.fit_transform(user_tweets)
        terms = self.vectorizer.get_feature_names()
        words = user_tweets
        data_returned = sorted(self.followed_tweets, key=self.count_bag, reverse=True)
        results = data_returned[0:number_of_recommendations]
        return results

    def count_bag(self, user_tweets):
        count = 0
        terms = self.vectorizer.get_feature_names()
        words = user_tweets.split()
        
        for word in words:
            if word in terms:
                count += 1

        return count