# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
from Tweetbox import Tweetbox
from collections import Counter
import tweepy
import time
import string


class RecommenderTextual:
    
    #TO-DO:
    #-set language to users own twitter language
    #-currently misses end hashtags
    #-Does not search for hashtags, just "word-searches"
    #-does not add hashtags to term-frequency document
    #-does not distinguish Java from JavaScript (Could use a bigram list for this)
    
    def __init__(self, users_own_tweets, users_followed_tweets):#, ckey, csecret, atoken, atokensecret):
        self.vectorizer = CountVectorizer()
        self.own_tweets = users_own_tweets
        self.followed_tweets = users_followed_tweets
        self.get_term_frequency_weightings(None, None)  

    #This method currently gets the top thirty terms that a users tweets with
    def get_term_frequency_weightings(self, number_of_terms_in_document, number_of_user_timeline_tweets):
        weightings = {}#Dictionary of terms (keys) and their weighting (value)
        top_amount_of_terms = 30# or just the "number_of_terms_in_document" parameter
        amount_of_tweets_to_gather = 101#Or just the "number_of_user_timeline_tweets" parameter, + 1
                                        #The extra "1" is because python is not inclusive of the last digit in the range that 
                                        #this variable is used for later on.
        
        #On a scale up to 10.0
        numeric_scale = 10

        #We want the top 5 most occurring terms
        top_x_terms = 5

        #http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
        exclude = set(string.punctuation)
        
        #generate a list of stop words
        stop_words = [word for word in CountVectorizer(stop_words='english').get_stop_words()]
        stop_words.append('rt')
        stop_words.append('https')

        #Filtering section
        my_first_x_tweets = self.own_tweets[0:amount_of_tweets_to_gather]
        overall_list = []
        for sublist in my_first_x_tweets: 
            for item in sublist.text.split():
                if item not in stop_words:
                    transformed_item = item.lower().translate(string.punctuation)
                    overall_list.append(transformed_item)# item.lower())
        
        total_count = len(overall_list)
        frequency_doc = Counter(overall_list)
        term_frequncy_list = {}

        for term in frequency_doc.keys():
            term_weight = (float(frequency_doc.get(term))/total_count) * numeric_scale
            term_frequncy_list[term] = term_weight

        self.termfreq_doc = term_frequncy_list
        top_terms = []
        most_common_raw = frequency_doc.most_common(top_x_terms) 
        for x in range(0, top_x_terms):
            top_terms.append(most_common_raw[x][0])

        remove_these_terms = []

        for term in self.termfreq_doc:
            if term not in top_terms:
                remove_these_terms.append(term)

        for removal in remove_these_terms:
            self.termfreq_doc.pop(removal, None)

        return weightings

    def get_tweet_term_weighting(self, tweet_text, term):
        weighting = 0
        term_match_weighting = 0
        already_weighted_terms = []
        tweet_text_stripped = tweet_text.replace("#","").encode('utf-8')
        individual_tweet_words = tweet_text_stripped.split(" ")
        for word in individual_tweet_words:  
            if self.termfreq_doc.get(word.lower()) is not None:
                term_match_weighting += self.termfreq_doc.get(word.lower())
        weighting = term_match_weighting
        return weighting

    def generate(self, number_of_recommendations, how_many_days_ago):
        list_of_owners_tweets = []
        unfollowed_tweets = []
        for tweet in self.own_tweets:
            list_of_owners_tweets.append(tweet.text.encode('utf-8'))

        self.vectorizer.fit_transform(list_of_owners_tweets)
        words = self.own_tweets #The users own tweets
        tweet_list = self.followed_tweets #tweets from accounts that the user is following
        data_returned = sorted(tweet_list, key=self.count_bag, reverse=True)
        results = data_returned[0:number_of_recommendations]
       
        return results

    def count_bag(self, tweet):
        count = 0
        sanitised_tweet_text = tweet.text
        
        #bug
        #Somehow, the following tweet is being counted as six (should be three)
        #Tweet!
        #Guavate: tiny library bridging Guava and Java8 - Core Java Google Guava, Guavate, Java 8 https://t.co/kQnWkUy9V7
        #count!
        #6

        for word in sanitised_tweet_text.split():
            if word.lower() in self.termfreq_doc.keys():
                count += 1 
                count += self.get_tweet_term_weighting(sanitised_tweet_text, self.termfreq_doc.get(word))

        return count