from sklearn.feature_extraction.text import CountVectorizer
from Tweetbox import Tweetbox
from collections import Counter
import tweepy


class Recommender:
    
    #TO-DO:
    #-currently misses end hashtags
    #-does not add hashtags to term-frequency document
    #-does not distinguish Java from JavaScript (Could use a bigram list for this)
    #-does not filter stop-words from the term-frequency document (Should be something in a library to help with this)
    
    def __init__(self, ckey, csecret, atoken, atokensecret):
        self.vectorizer = CountVectorizer()
        consumer_key = ckey
        consumer_secret = csecret
        access_token = atoken
        access_token_secret = atokensecret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.set_own_tweets()#Set the users tweets aas a variable
        self.set_followed_tweets()#Grab the users home timeline and set it as an attribute
        self.get_term_frequency_weightings(None, None)

    #This method sets the "followed_tweets" attrribute for the recommender object. Followed tweets are ones that we make recommendations upon.
    def set_followed_tweets(self):
        self.followed_tweets = self.api.home_timeline()

    #def get_Unfollowed_tweets(self):
    #    api.

    #This method sets the "own_tweets" attrribute for the recommender object. These are tweets
    #from the users personal timeline, used to make the term frequncy document.   
    def set_own_tweets(self):                                      
        self.own_tweets = self.api.user_timeline()

    #This method currently gets the top thirty terms that a users tweets with
    def get_term_frequency_weightings(self, number_of_terms_in_document, number_of_user_timeline_tweets):
        weightings = {}#Dictionary of terms (keys) and their weighting (value)
        top_amount_of_terms = 30# or just the "number_of_terms_in_document" parameter
        amount_of_tweets_to_gather = 101#Or just the "number_of_user_timeline_tweets" parameter, + 1
                                        #The extra "1" is because python is not inclusive of the last digit in the range that 
                                        #this variable is used for later on.
        numeric_scale = 10 #(on a scale up to 10.0)

        #Filtering section
        my_first_x_tweets = self.own_tweets[0:amount_of_tweets_to_gather]
        overall_list = []
        for sublist in my_first_x_tweets: 
            for item in sublist.text.split():
                overall_list.append(item.lower())
        
        total_count = len(overall_list)
        frequency_doc = Counter(overall_list)
        term_frequncy_list = {}
        #print 'total count'
        #print total_count
        for term in frequency_doc.keys():
         #   print 'occurences'
         #   print frequency_doc.get(term)
            
            term_weight = (float(frequency_doc.get(term))/total_count) * numeric_scale
          #  print 'weighting'
          #  print term_weight

            term_frequncy_list[term] = term_weight

        self.termfreq_doc = term_frequncy_list#Counter(overall_list)
        #top_x_terms = self.termfreq_doc.most_common(top_amount_of_terms) 
        #print "tf doc"
        #print self.termfreq_doc
        return weightings

    def get_tweet_term_weighting(self, tweet_text, term):
        weighting = 0
        match_count = 0
        term_match_weighting = 0
        already_weighted_terms = []
        tweet_text_stripped = tweet_text.replace("#","").encode('utf-8')
        individual_tweet_words = tweet_text_stripped.split(" ")
        for word in individual_tweet_words:  
            if self.termfreq_doc.get(word.lower()) is not None:
                term_match_weighting += self.termfreq_doc.get(word.lower())
        
        #weighting = ((match_count + term_match_weighting)/len(tweet_text_stripped.split()))/ term_match_weighting#(len(self.termfreq_doc) + term_match_weighting)  
        weighting = term_match_weighting#((match_count + term_match_weighting)/len(tweet_text.split()))/(len(self.termfreq_doc) + term_match_weighting)  
        print "weighting here"
        print weighting
        print "tweet here"
        print tweet_text_stripped
        ##Include "term_match_weighting" here? 
        return weighting

    def generate(self, number_of_recommendations, followed_accounts, how_many_days_ago):
        list_of_owners_tweets = []
        for tweet in self.own_tweets:
            list_of_owners_tweets.append(tweet.text.encode('utf-8'))

        self.vectorizer.fit_transform(list_of_owners_tweets)
        words = self.own_tweets #The users own tweets
        print self.termfreq_doc
        tweet_listy = self.followed_tweets #tweets from accounts that the user is following
        data_returned = sorted(tweet_listy, key=self.count_bag, reverse=True)
        results = data_returned[0:number_of_recommendations]

        return results

    def count_bag(self, tweet):
        count = 0
        sanitised_tweet_text = tweet.text
        #print "Tweet!"
        #print sanitised_tweet_text.encode('utf-8')
        #terms = self.vectorizer.get_feature_names()
        #Use term frequency here
        
        #bug
        #Tweet!
        #Guavate: tiny library bridging Guava and Java8 - Core Java Google Guava, Guavate, Java 8 https://t.co/kQnWkUy9V7
        #count!
        #6

        #todo: add in get_tweet_term_weighting(tweet)
        for word in sanitised_tweet_text.split():
            if word.lower() in self.termfreq_doc.keys():
                count += 1 
                count += self.get_tweet_term_weighting(sanitised_tweet_text, self.termfreq_doc.get(word))
        #print "count!"
        #print count
        return count