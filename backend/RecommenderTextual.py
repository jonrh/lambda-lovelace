# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import tweepy
import time
import string
from datetime import datetime, timedelta

class RecommenderTextual:
    
    #TO-DO:
    #-set language to users own twitter language
    #-does not distinguish Java from JavaScript (Could use a bigram list for this)

    #BUGS: 
    #-Hashtags are worth "double" than what they appear

    #TODAY:
    #-Tweet.entities.hashtags - iterate when adding to term frequency document.
    #-Figure out if above (entities) appears in tweet.text too.

    def __init__(self, users_own_tweets, users_followed_tweets):
        ######################################################
        ###get_term_frequency_weightings function variables###
        ######################################################
        #Could also be called the "number_of_user_timeline_tweets" parameter, + 1
        #The extra "1" is because python is not inclusive of the last digit in the range that 
        #this variable is used for later on.
        self.amount_of_tweets_to_gather = 101
        #We want the top 5 most occurring terms
        self.top_x_terms = 50
        #On a scale up to X.0, what is the scale that the term frequency document should follow
        self.numeric_scale = 10
        #How much are hashtags worth as opposed to terms (worth 1, so 2 means that a hashtag is 
        #worth double the worth of a term)
        #This is currently bugged however, see bugs section above.
        self.hash_tag_multiplier = 2       

        ###################
        #Method calls, etc#
        ###################
        self.vectorizer = CountVectorizer()
        self.own_tweets = users_own_tweets
        self.followed_tweets = users_followed_tweets
        self.get_term_frequency_weightings()
        #print(self.termfreq_doc)
       

    #This method currently gets the top x terms that a users tweets with
    def get_term_frequency_weightings(self):
        weightings = {}#Dictionary of terms (keys) and their weighting (value)

        #http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
        exclude = set(string.punctuation)
        
        #generate a list of stop words
        stop_words = [word for word in CountVectorizer(stop_words='english').get_stop_words()]
        stop_words.append('rt')
        stop_words.append('https')

        #Filtering section
        my_first_x_tweets = self.own_tweets[0: self.amount_of_tweets_to_gather]
        overall_list = []
        for sublist in my_first_x_tweets:#Iterating each tweet
            for item in sublist['text'].split():#UNCOMMENT THIS LINE BEFORE COMMITTING AND COMMENT OUT LINE BELOW
            #for item in sublist.text.split():#Iterating each word of a tweet
                if item not in stop_words:
                    #https://www.quora.com/How-do-I-remove-punctuation-from-a-Python-string
                    word = item.lower()
                    transformed_item = ''.join(c for c in word if c not in string.punctuation)
                    overall_list.append(transformed_item)
            
            for hashtag in sublist['entities']['hashtags']:#UNCOMMENT THIS LINE BEFORE COMMITTING AND COMMENT OUT LINE BELOW
            #for hashtag in sublist.entities['hashtags']: 
                tag = hashtag['text'].lower()
                #https://www.quora.com/How-do-I-remove-punctuation-from-a-Python-string
                overall_list.append(''.join(c for c in tag if c not in string.punctuation))


        total_count = len(overall_list)
        frequency_doc = Counter(overall_list)
        term_frequncy_list = {}

        for term in frequency_doc.keys():
            hashtag = str('#{}'.format(term))
            hashtag_value = float(frequency_doc.get(hashtag) * self.hash_tag_multiplier) if frequency_doc.get(hashtag) is not None else 0.0
            term_value = float(frequency_doc.get(str(term)))
            term_weight = ((hashtag_value + term_value)/total_count)  * self.numeric_scale
            term_frequncy_list[str(term)] = term_weight

        self.termfreq_doc = term_frequncy_list
        top_terms = []
        last_index = self.top_x_terms if len(frequency_doc) > self.top_x_terms else len(frequency_doc)
        most_common_raw = frequency_doc.most_common(last_index) 
        print(most_common_raw)
        for x in range(0, last_index):
            print(x)
            top_terms.append(most_common_raw[x][0])

        remove_these_terms = []

        for term in self.termfreq_doc:
            if term not in top_terms:
                remove_these_terms.append(term)

        for removal in remove_these_terms:
            self.termfreq_doc.pop(removal, None)

        print(weightings)
        return weightings

    def get_tweet_term_weighting(self, tweet_text):
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







        #http://stackoverflow.com/questions/23356523/how-can-i-get-the-age-of-a-tweet-using-tweepy
        #age = time.time() - (tweet_age - datetime.datetime(1970,1,1)).total_seconds()







        #http://stackoverflow.com/questions/7582333/python-get-datetime-of-last-hour
        #lastHourDateTime = datetime.today() - timedelta(hours = 1)


        for tweet in self.own_tweets:
            #list_of_owners_tweets.append(tweet.text.encode('utf-8'))
            list_of_owners_tweets.append(tweet['text'].encode('utf-8')) #UNCOMMENT THIS LINE BEFORE COMMITTING AND COMMENT OUT LINE ABOVE

        self.vectorizer.fit_transform(list_of_owners_tweets)
        words = self.own_tweets #The users own tweets
        tweet_list = self.followed_tweets #tweets from accounts that the user is following
        data_returned = sorted(tweet_list, key=self.count_bag, reverse=True)
        results = data_returned[0:number_of_recommendations]
        counts  = [self.count_bag(tweet) for tweet in results]
        
        return {"recommended_tweets":results, "counts":sorted(counts, reverse=True)}

    def get_tweet_age_score(self, tweet):
        tweet_age = tweet.created_at
        #http://stackoverflow.com/questions/23356523/how-can-i-get-the-age-of-a-tweet-using-tweepy
        age = time.time() - (tweet_age - datetime.datetime(1970,1,1)).total_seconds()
        week_seconds = 604800 #604800 seconds in a week
        rank = (age / week_seconds) * self.numeric_scale
        return age

    def count_bag(self, tweet):
        count = 0
        sanitised_tweet_text = tweet['text'] #UNCOMMENT THIS LINE BEFORE COMMITTING AND COMMENT OUT LINE BELOW
        #sanitised_tweet_text = tweet.text 
        
        #bug
        #Somehow, the following tweet is being counted as six (should be three)
        #Tweet!
        #Guavate: tiny library bridging Guava and Java8 - Core Java Google Guava, Guavate, Java 8 https://t.co/kQnWkUy9V7
        #count!
        #6

        for word in sanitised_tweet_text.split():
            if word.lower() in self.termfreq_doc.keys():
                count += 1 
                count += self.get_tweet_term_weighting(sanitised_tweet_text)#, self.termfreq_doc.get(word))
                count -= self.get_tweet_age_score(tweet)
                if count < 0:
                    count = 0

        return count