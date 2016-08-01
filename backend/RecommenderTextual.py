# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import time
import string
from datetime import datetime
import rollbar
import operator
from Stopwords import Stopwords


class RecommenderTextual:
    # BUGS:
    #  -Hashtags are worth "double" than what they appear

    def __init__(self, users_own_tweets, users_followed_tweets, single_tweet_feedback):
        ######################################################
        # get_term_frequency_weightings function variables###
        ######################################################
        # Could also be called the "number_of_user_timeline_tweets" parameter, + 1
        # The extra "1" is because python is not inclusive of the last digit in the range that
        # this variable is used for later on.
        self.amount_of_tweets_to_gather = 101
        # We want the top 5 most occurring terms
        self.top_x_terms = 50
        # On a scale up to X.0, what is the scale that the term frequency document should follow
        self.numeric_scale = 10
        # How much are hashtags worth as opposed to terms (worth 1, so 2 means that a hashtag is
        # worth double the worth of a term)
        # This is currently bugged however, see bugs section above.
        self.hash_tag_multiplier = 2
        self.single_tweet_feedback = single_tweet_feedback
        self.liked_tweets = []
        self.disliked_tweets = []
        self.more_or_less_from_this_author_multiplier = 0.4
        self.like_and_dislike_multiplier = 0.125
        ###################
        # Method calls, etc#
        ###################
        self.vectorizer = CountVectorizer()
        self.own_tweets = users_own_tweets
        self.followed_tweets = users_followed_tweets
        self.get_term_frequency_weightings()

    # This method currently gets the top x terms that a users tweets with
    def get_term_frequency_weightings(self):
        weightings = {}  # Dictionary of terms (keys) and their weighting (value)

        # http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
        exclude = set(string.punctuation)
        
        # generate a list of stop words
        stop_words = [word for word in CountVectorizer(stop_words='english').get_stop_words()]
        stop_words.append('rt')
        stop_words.append('https')

        # Filtering section
        my_first_x_tweets = self.own_tweets[0: self.amount_of_tweets_to_gather]
        overall_list = []
        stop_words_list = Stopwords()
        long_stop_words = stop_words_list.return_stopwords()
        #for sublist in my_first_x_tweets: # Iterating each tweet
        for item in sublist['text'].split(): # UNCOMMENT THIS LINE BEFORE COMMITTING AND COMMENT OUT LINE BELOW

            for item in sublist.text.split():#Iterating each word of a tweet
                if item.lower() not in stop_words and item.lower() not in long_stop_words:
                    # https://www.quora.com/How-do-I-remove-punctuation-from-a-Python-string
                    word = item.lower()
                    transformed_item = ''.join(c for c in word if c not in string.punctuation)
                    overall_list.append(transformed_item)
            
            for hashtag in sublist['entities']['hashtags']:  # UNCOMMENT THIS LINE BEFORE COMMITTING AND COMMENT OUT LINE BELOW
            #for hashtag in sublist.entities['hashtags']: 
                tag = hashtag['text'].lower()
                # https://www.quora.com/How-do-I-remove-punctuation-from-a-Python-string
                overall_list.append(''.join(c for c in tag if c not in string.punctuation))

        total_count = len(overall_list)
        frequency_doc = Counter(overall_list)
        term_frequncy_list = {}

        for term in frequency_doc.keys():
            # hashtag = str(u'#{}'.format(term))#.encode('utf-8')
            hashtag = u'#' + term
            hashtag_value = float(frequency_doc.get(hashtag) * self.hash_tag_multiplier) if frequency_doc.get(hashtag) is not None else 0.0
            term_value = float(frequency_doc.get(term))
            term_weight = ((hashtag_value + term_value)/total_count)  * self.numeric_scale
            term_frequncy_list[term] = term_weight

        self.termfreq_doc = term_frequncy_list
        top_terms = []
        last_index = self.top_x_terms if len(frequency_doc) > self.top_x_terms else len(frequency_doc)
        most_common_raw = frequency_doc.most_common(last_index) 

        for x in range(0, last_index):
            top_terms.append(most_common_raw[x][0])

        remove_these_terms = []

        for term in self.termfreq_doc:
            if term not in top_terms:
                remove_these_terms.append(term)

        for removal in remove_these_terms:
            self.termfreq_doc.pop(removal, None)

        self.debug_term_frequency_to_rollbar()

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

    def get_author_sentiment(self, tweet):
        author_name = tweet.author._json['screen_name']
        score = 0
        for name in self.single_tweet_feedback.keys():
            if author_name == str(name):
                #numeric scale?
                feedback_score = self.single_feedback.get(author_name)
                capped_score =  feedback_score if feedback_score <= 100 else 100
                score =  (capped_score/numeric_scale)* more_or_less_from_this_author_multiplier
        return score

    def get_dislike_weighting(self, tweet):
        print("DISLIKED")
        print(tweet.text)
        tweet_text = tweet.text
        terms_to_reduce = []
        for word in tweet.text.split(" "):
            unhashedword = word.lower()
            if "#" in word and word[0] == "#":
                unhashedword.replace("#", "", 1)
            if unhashedword in self.termfreq_doc.keys():
                terms_to_reduce.append(unhashedword)
        self.balance_reduce_term_freq_doc_preference(terms_to_reduce)

    def balance_reduce_term_freq_doc_preference(self, terms_to_reduce):
        num_of_reduced_terms = len(terms_to_reduce)
        num_of_terms = len(self.termfreq_doc.keys())
        alter_value = self.like_and_dislike_multiplier
        print("***")
        print(alter_value)
        print("divided by")
        print(num_of_reduced_terms)
        reduce_value = alter_value/num_of_reduced_terms 
        increase_value = alter_value/(num_of_terms - num_of_reduced_terms) #self.numeric_scale/(self.numeric_scale - num_of_reduced_terms) * like_and_dislike_multiplier 
        increase_terms = []
        for key in self.termfreq_doc.keys():
            if str(key) not in terms_to_reduce:
                increase_terms.append(str(key))

        for term in terms_to_reduce:
            print("removing from " + str(term) + " with: " + str(reduce_value))
            self.termfreq_doc[term] -= reduce_value

        for term in increase_terms:
            print("adding to " + str(term) + " with: " + str(increase_value))
            self.termfreq_doc[term] += increase_value

    def get_liked_weighting(self, tweet):
        print("LIKED")
        print(tweet.text)
        tweet_text = tweet.text
        terms_to_increase = []
        for word in tweet.text.split(" "):
            unhashedword = word.lower()
            if "#" in word and word[0] == "#":
                unhashedword.replace("#", "", 1)
            if unhashedword in self.termfreq_doc.keys():
                terms_to_increase.append(unhashedword)
        self.balance_increase_term_freq_doc_preference(terms_to_increase)

    def balance_increase_term_freq_doc_preference(self, terms_to_increase):
        num_of_increased_terms = len(terms_to_increase)
        num_of_terms = len(self.termfreq_doc.keys())
        alter_value = self.like_and_dislike_multiplier 
        increase_value = alter_value/(num_of_increased_terms) 
        reduce_value = alter_value/(num_of_terms - num_of_increased_terms) 
        reduce_terms = []
        for key in self.termfreq_doc.keys():
            if str(key) not in terms_to_increase:
                reduce_terms.append(str(key))

        for term in terms_to_increase:
            print("adding to " + str(term) + " with: " + str(increase_value))
            self.termfreq_doc.get[term] += increase_value

        for term in reduce_terms:
            print("removing from " + str(term) + " with: " + str(reduce_value))
            self.termfreq_doc.get[term] -= reduce_value


    def generate(self, number_of_recommendations, how_many_days_ago):
        list_of_owners_tweets = []
        unfollowed_tweets = []
        seconds_ago = 0 

        # https://www.google.ie/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=seconds%20in%20six%20days
        if how_many_days_ago is 7:
            seconds_ago = 604800  
        elif how_many_days_ago is 6:
            seconds_ago = 518400
        elif how_many_days_ago is 5:
            seconds_ago = 432000
        elif how_many_days_ago is 4:
            seconds_ago = 345600
        elif how_many_days_ago is 3:
            seconds_ago = 259200
        elif how_many_days_ago is 2:
            seconds_ago = 172800
        elif how_many_days_ago is 1:
            # seconds_ago = 86400
            seconds_ago = 1000000
        else:
            seconds_ago = 1000000

        for tweet in self.own_tweets:
            #list_of_owners_tweets.append(tweet.text.encode('utf-8'))
            list_of_owners_tweets.append(tweet['text'].encode('utf-8'))  # UNCOMMENT THIS LINE BEFORE COMMITTING AND COMMENT OUT LINE ABOVE

        self.vectorizer.fit_transform(list_of_owners_tweets)
        words = self.own_tweets  # The users own tweets
        tweet_list = self.followed_tweets  # tweets from accounts that the user is following

        remove_these_tweets = []

        for tweet in tweet_list:
            #tweet_age = tweet.created_at
            tweet_age = tweet['created_at']
            # http://stackoverflow.com/questions/23356523/how-can-i-get-the-age-of-a-tweet-using-tweepy
            tweet_age = datetime.strptime(tweet_age, '%a %b %d %H:%M:%S +0000 %Y')  # dirty fix
            age = time.time() - (tweet_age - datetime(1970, 1, 1)).total_seconds()
            if age > seconds_ago:
                remove_these_tweets.append(tweet)

        for removal in remove_these_tweets:
            tweet_list.remove(removal)

        data_returned = sorted(tweet_list, key=self.count_bag, reverse=True)
        results = data_returned[0:number_of_recommendations]
        counts = [self.count_bag(tweet) for tweet in results]
        
        return {"recommended_tweets": results, "counts": sorted(counts, reverse=True)}

    def get_tweet_age_score(self, tweet):
        tweet_age = tweet['created_at']
        tweet_age = datetime.strptime(tweet_age, '%a %b %d %H:%M:%S +0000 %Y')  # dirty fix
        #tweet_age = tweet.created_at
        # http://stackoverflow.com/questions/23356523/how-can-i-get-the-age-of-a-tweet-using-tweepy
        age = time.time() - (tweet_age - datetime(1970, 1, 1)).total_seconds()
        week_seconds = 604800 # 604800 seconds in a week
        rank = (age / week_seconds) * self.numeric_scale
        return rank

    def count_bag(self, tweet):
        count = 0.0
        sanitised_tweet_text = tweet['text']  # UNCOMMENT THIS LINE BEFORE COMMITTING AND COMMENT OUT LINE BELOW
        #sanitised_tweet_text = tweet.text
        # bug
        # Somehow, the following tweet is being counted as six (should be three)
        # Tweet!
        # Guavate: tiny library bridging Guava and Java8 - Core Java Google Guava, Guavate, Java 8 https://t.co/kQnWkUy9V7
        # count!
        # 6
        count += self.get_author_sentiment(tweet)
        if "Java" in tweet.text:
        #if tweet in self.disliked_tweets:
            self.get_dislike_weighting(tweet)

        if "Ruby" in tweet.text:
        #if tweet in self.liked_tweets:
            self.get_liked_weighting(tweet)

        for word in sanitised_tweet_text.split():
            if word[0] == "#":
                new_word = word.replace("#", "")
            else:
                new_word = word
            for term in self.termfreq_doc.keys():
                if new_word.lower() == str(term.encode("utf-8")):
                    count += 1
                    count += self.get_tweet_term_weighting(sanitised_tweet_text)  # , self.termfreq_doc.get(word))
                    count -= self.get_tweet_age_score(tweet)
                    if count < 0.0:
                        count = 0.0

        return count

    def debug_term_frequency_to_rollbar(self):
        """
        Sends to Rollbar the term frequcny document so we can easily debug
        what terms and weights we work with. This should hopefully allow us to
        see what terms are being used and what sort of weights they get. To
        spot anomalies, stopwords, etc.
        """
        # List of (term, weight) tuples sorted descending by weight. Example: [("lol", 9.89), ("kek", 3.37)]
        sorted_by_weight = sorted(self.termfreq_doc.items(), key=operator.itemgetter(1), reverse=True)

        pretty_termdoc_string = u"Term weights: \n weight: term \n"

        for term, weight in sorted_by_weight:
            pretty_termdoc_string += u"{0:.3f}: {1}\n".format(weight, term)

        rollbar.report_message(pretty_termdoc_string, "debug")
