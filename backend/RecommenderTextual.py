# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import time
import string
from datetime import datetime
import rollbar
import operator
from Stopwords import Stopwords


###DESC
#second net

#lines 143-153

class RecommenderTextual:

    def __init__(self, users_own_tweets, users_followed_tweets, single_tweet_feedback):
        ######################################################
        # get_term_frequency_weightings function variables###
        ######################################################
        # Could also be called the "number_of_user_timeline_tweets" parameter, + 1
        # The extra "1" is because python is not inclusive of the last digit in the range that
        # this variable is used for later on to set a max on the number of the users tweets
        # to use when creating their term frequency document.
        self.amount_of_tweets_to_gather = 101
        # We want the top 5 most occurring terms
        self.top_x_terms = 23
        self.second_net_multiplier = 2
        # On a scale up to X.0, what is the scale that the term frequency document should follow
        self.numeric_scale = 10
        # How much are hashtags worth as opposed to terms (worth 1, so 2 means that a hashtag is
        # worth double the worth of a term)
        # This is currently bugged however, see bugs section above.
        self.hash_tag_multiplier = 2
        self.single_tweet_feedback = single_tweet_feedback
        self.liked_tweets = []
        self.disliked_tweets = []
        self.liked_authors = []
        self.disliked_authors = []
        self.termfreq_doc = {}
        self.second_net_termfreq_doc = {}
        self.more_or_less_from_this_author_multiplier = 5.1#2.5
        self.like_and_dislike_multiplier = 10.1#0.125
        ###################
        # Method calls, etc#
        ###################
        self.own_tweets = users_own_tweets
        self.followed_tweets = users_followed_tweets
        self.get_term_frequency_weightings()
        self.set_feedback()
        self.author_feedback = self.set_author_sentiment()
        self.set_tweet_feedback()
        self.vectorizer = CountVectorizer()

    def set_tweet_feedback(self):
        for tweet_text in self.liked_tweets:
            self.get_liked_terms_and_increase_weighting(tweet_text)
        for tweet_text in self.disliked_tweets:
            self.get_disliked_tweets_terms_and_reduce(tweet_text)

    def set_author_sentiment(self):
        author_feedback = {}
        for author in self.disliked_authors:
            #print("author")
            #print(str(author) + " disliked!")
            author_feedback[author] = author_feedback.get(author, 0) - 1
        for author in self.liked_authors:
            #print("author")
            #print(str(author) + " liked!")
            author_feedback[author] = author_feedback.get(author, 0) + 1
        return author_feedback

    def set_feedback(self):#WORKS
        for feedback in self.single_tweet_feedback:
            if feedback.get("feedback", None).lower() == "like" and feedback.get("reason", None).lower() == "subject":
                self.liked_tweets.append(feedback.get("tweetContent", None))

            elif feedback.get("feedback", None).lower() == "dislike" and feedback.get("reason", None).lower() == "subject":
                self.disliked_tweets.append(feedback.get("tweetContent", None))
            
            elif feedback.get("feedback", None).lower() == "like" and feedback.get("reason", None).lower() == "author":
                self.liked_authors.append(feedback.get("followerScreenName", None))
            
            elif feedback.get("feedback", None).lower() == "dislike" and feedback.get("reason", None).lower() == "author":
                self.disliked_authors.append(feedback.get("followerScreenName", None))
            
            else:
                print(feedback.get("reason", None).lower())
                print(feedback.get("feedback", None).lower())
                print("ERROR, the following feedback could not be processed: " + str(feedback))

    def get_term_frequency_weightings(self):#WORKS
        """Creates weightings for the term frequency document.
       
           This function sets the recommender objects termfreq_doc
           and second_net_termfreq_doc attributes.

           Args:
               No arguments

           Returns:
               Nothing. This function is used to set attributes within
               the Recommender object.
        """
        weightings = {}  # Dictionary of terms (keys) and their weighting (value)
        second_net_top_x_terms = self.top_x_terms * self.second_net_multiplier
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
        for sublist in my_first_x_tweets:
            for item in sublist['text'].split(): # UNCOMMENT THIS LINE BEFORE COMMITTING AND COMMENT OUT LINE BELOW
            #for item in sublist.text.split():#Iterating each word of a tweet
                if item.lower() not in stop_words and item.lower() not in long_stop_words:
                    # https://www.quora.com/How-do-I-remove-punctuation-from-a-Python-string
                    word = item.lower()
                    transformed_item = ''.join(c for c in word if c not in string.punctuation)
                    overall_list.append(transformed_item)
            
            for hashtag in sublist['entities']['hashtags']: # UNCOMMENT THIS LINE BEFORE COMMITTING AND COMMENT OUT LINE BELOW
            #for hashtag in sublist.entities['hashtags']: 
                tag = hashtag['text'].lower()
                # https://www.quora.com/How-do-I-remove-punctuation-from-a-Python-string
                overall_list.append(''.join(c for c in tag if c not in string.punctuation))

        total_count = len(overall_list)
        frequency_doc = Counter(overall_list)
        second_net_frequency_doc = Counter(overall_list)
        term_frequency_list = {}

        for term in frequency_doc.keys():
            #hashtag = str(u'#{}'.format(term))#.encode('utf-8')
            hashtag = u'#' + term
            #print("hashtag")
            #print(hashtag)
            hashtag_value = float(frequency_doc.get(hashtag) * self.hash_tag_multiplier) if frequency_doc.get(hashtag) is not None else 0.0
            term_value = float(frequency_doc.get(term))
            term_weight = ((hashtag_value + term_value)/total_count) * self.numeric_scale
            term_frequency_list[term] = term_weight

        self.termfreq_doc = term_frequency_list.copy()
        self.second_net_termfreq_doc = term_frequency_list.copy()
        top_terms = []
        second_net_top_terms = []
        last_index = self.top_x_terms if len(frequency_doc) > self.top_x_terms else len(frequency_doc)
        second_net_last_index = second_net_top_x_terms if len(frequency_doc) > second_net_top_x_terms else len(frequency_doc)

        most_common_raw = frequency_doc.most_common(last_index) 
        second_net_most_common_raw = frequency_doc.most_common(second_net_last_index)
        
        for x in range(0, last_index):
            top_terms.append(most_common_raw[x][0])

        for x in range(0, second_net_last_index):
            second_net_top_terms.append(second_net_most_common_raw[x][0])

        remove_these_terms = []
        second_net_remove_these_terms = []

        for term in self.termfreq_doc:
            if term not in top_terms:
                remove_these_terms.append(term)
 
        for term in self.second_net_termfreq_doc:
            if term not in second_net_top_terms:
                second_net_remove_these_terms.append(term)

        for removal in remove_these_terms:
            self.termfreq_doc.pop(removal, None)
        
        for removal in second_net_remove_these_terms:
            self.second_net_termfreq_doc.pop(removal, None)
        
        self.debug_term_frequency_to_rollbar()
        
        # Removes the empty string from the term frequency document. This is a fix for an issue we were not able to
        # resolve otherwise. What happens is that terms that only contain special characters get aggregated together
        # to create a "super" term. This is not indented so we remove the empty string as a viable term.
        
        #print("This is the term frequency document")
        #print(self.termfreq_doc)
        if "" in self.termfreq_doc.keys():
            print("POPPED the empty string!")
            self.termfreq_doc.pop("")
        else:
            print("Did not POP an empty string...")

        #return weightings#This line can be removed

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
        """Retrieve author sentiment for a tweet object.

           Args:
               tweet: A tweet object from the Twitter REST API.

           Returns:
               A numeric score, reflective of the users preferences
               based on the author_feedback object
        """
        author_name = tweet['user']['screen_name']
        #author_name = tweet.author.screen_name
        score = 0.0
        #print(str(author_name.lower().encode("utf-8")))
        for name in self.author_feedback.keys():
            if str(author_name.lower().encode("utf-8")) == str(name.lower().encode("utf-8")):
                feedback_score = self.author_feedback.get(author_name)
                multiplier = self.more_or_less_from_this_author_multiplier
                scale = self.numeric_scale
                score = float(feedback_score)/float(scale) * float(multiplier)
        return score

    def get_disliked_tweets_terms_and_reduce(self, tweet):
        """Retrieve terms whose value will be reduced due to their
           appearance in a disliked tweet object and call the 
           "balance_reduce_term_freq_doc_preference" function with 
           those terms as arguments.

           Args:
               tweet: A tweet object from the Twitter REST API.

           Returns:
               Nothing. This function calls the "balance_reduce_term_freq_doc_preference"
               with the terms that need to be reduced in weight.
        """
        tweet_text = tweet
        #print("tweet")
        #print(u"DISLIKED " + tweet_text)
        terms_to_reduce = set() # We only want to reduce each term once
        for word in tweet_text.replace("\n"," ").split():
            unhashedword = word
            if word.startswith("#"):
                unhashedword = unhashedword[1:]
            for term in self.termfreq_doc.keys():
                if unhashedword == term:
                    terms_to_reduce.add(term)#Add the term, because a "term" can be inside another full word (Javacodegeeks for Java)
        
        # Only execute this method if there is a term in the tweets text that can be reduced.
        # This means that disliking a tweet that does not contain a term will have no effect, but
        # these terms are towards the end of the recommended list anyway.
        if len(terms_to_reduce) >= 1:
            self.balance_reduce_term_freq_doc_preference(terms_to_reduce)
        
    def balance_reduce_term_freq_doc_preference(self, terms_to_reduce):
        """Given the terms that should be reduced from the
            "get_disliked_tweets_terms_and_reduce" function,
            find them in the term frequency document and reduce
            the value of their weightings. Increase the value of
            all other terms in proportion to the total weight reduced 
            in the term frequency document to maintain the chosen 
            ratio (the value of self.numeric_scale) 

           Args:
               terms_to_reduce: A list of terms to be reduced 
               in weight, found in the term frequency document.

           Returns:
               Nothing. This function changes the values of 
               terms in the term frequency document
        """
        num_of_reduced_terms = len(terms_to_reduce)
        num_of_terms = len(self.termfreq_doc.keys())
        alter_value = self.like_and_dislike_multiplier
        reduce_value = alter_value/num_of_reduced_terms 
        increase_value = alter_value/(num_of_terms - num_of_reduced_terms) 
        increase_terms = []
        for key in self.termfreq_doc.keys():
            if key not in terms_to_reduce:
                increase_terms.append(key)

        for term in terms_to_reduce:
            #print("reducing from " + term + " with " + str(reduce_value))
            self.termfreq_doc[term] -= reduce_value

        for term in increase_terms:
            #print("adding to " + term + " with " + str(increase_value))
            self.termfreq_doc[term] += increase_value

    def get_liked_terms_and_increase_weighting(self, tweet):#WORKS
        """Retrieve terms whose value will be increased due to their
           appearance in a liked tweet object and call the 
           "balance_increase_term_freq_doc_preference" function with 
           those terms as arguments.

           Args:
               tweet: A tweet object from the Twitter REST API.

           Returns:
               Nothing. This function calls the "balance_increase_term_freq_doc_preference"
               with the terms that need to be increased in weight.
        """
        tweet_text = tweet
        #print("Tweet")
        #print("LIKED" + str(tweet_text))
        terms_to_increase = set() # We only want to increase each term once
        for word in tweet_text.replace("\n"," ").split():
            unhashedword = word
            if word.startswith("#"):
                unhashedword = unhashedword[1:]
            for term in self.termfreq_doc.keys():
                if unhashedword == term:
                    terms_to_increase.add(term)

        # Only execute this method if there is a term in the tweets text that can be increased.
        # This means that liking a tweet that does not contain a term will have no effect, but
        # the more the user tweets/retweets/likes on Twitter, the more likely these terms will appear.
        if len(terms_to_increase) >= 1:
            self.balance_increase_term_freq_doc_preference(terms_to_increase)

    def balance_increase_term_freq_doc_preference(self, terms_to_increase):
        """Given the terms that should be increased from the
           "get_liked_terms_and_increase_weighting" function,
           find them in the term frequency document and increase
           the value of their weightings. Decrease the weighting value of
           all other terms in proportion to the total weight increase 
           in the term frequency document to maintain the chosen 
           ratio (the value of self.numeric_scale) 

           Args:
               terms_to_increase: A list of terms to be increased in 
               weight, found in the term frequency document.

           Returns:
               Nothing. This function changes the values of 
               terms in the term frequency document
        """
        num_of_increased_terms = len(terms_to_increase)
        num_of_terms = len(self.termfreq_doc.keys())
        alter_value = self.like_and_dislike_multiplier 
        increase_value = alter_value/(num_of_increased_terms) 
        reduce_value = alter_value/(num_of_terms - num_of_increased_terms) 
        reduce_terms = []
        for key in self.termfreq_doc.keys():
            if key not in terms_to_increase:
                reduce_terms.append(key)

        for term in terms_to_increase:
            #print("adding to " + term + " with " + str(increase_value))
            self.termfreq_doc[term] += increase_value

        for term in reduce_terms:
            #print("reducing from " + term + " with " + str(reduce_value))
            self.termfreq_doc[term] -= reduce_value


    def generate(self, number_of_recommendations, how_many_days_ago):
        """TO-DO

           Args:
               number_of_recommendations:

           Returns:
               A list of tweets, sorted by learned user preferences.
        """
        #WORKS
        max_age_in_seconds = how_many_days_ago * 86400  # number of seconds in 1 day
        seconds_ago = 0
        if how_many_days_ago > 7:
            max_age_in_seconds = 1000000

        words = self.own_tweets  # The users own tweets
        tweet_list = self.followed_tweets  # tweets from accounts that the user is following

        remove_these_tweets = []

        for tweet in tweet_list:
            #tweet_age = tweet.created_at
            # http://stackoverflow.com/questions/23356523/how-can-i-get-the-age-of-a-tweet-using-tweepy
            tweet_age = tweet['created_at']
            tweet_age = datetime.strptime(tweet_age, '%a %b %d %H:%M:%S +0000 %Y')  # dirty fix
            age = time.time() - (tweet_age - datetime(1970, 1, 1)).total_seconds()
            if age > max_age_in_seconds:
                remove_these_tweets.append(tweet)

        for removal in remove_these_tweets:
            tweet_list.remove(removal)

        prelim_results = tweet_list
        tweets_that_contain_tf_terms = []
        tweets_that_do_not_contain_tf_terms = []
        
        for tweet in prelim_results:
            for term in self.termfreq_doc.keys():
                if term in tweet['text'].lower():
                #if term in tweet.text.lower():
                    tweets_that_contain_tf_terms.append(tweet)
                    break

        for tweet in prelim_results:
            if tweet not in tweets_that_contain_tf_terms:
                tweets_that_do_not_contain_tf_terms.append(tweet)

        term_tweets_sorted = sorted(tweets_that_contain_tf_terms, key=self.count_bag_first_net, reverse=True)
        non_term_tweets_sorted = sorted(tweets_that_do_not_contain_tf_terms, key=self.count_bag_second_net, reverse=True) 
        counts_for_term_tweets = [self.count_bag_first_net(tweet) for tweet in term_tweets_sorted]
        counts_for_non_term_tweets = [self.count_bag_second_net(tweet) for tweet in non_term_tweets_sorted]
        counts_for_term_tweets.extend(counts_for_non_term_tweets)
        term_tweets_sorted.extend(non_term_tweets_sorted)
    
        results = term_tweets_sorted[0:number_of_recommendations]
        counts = counts_for_term_tweets[0:number_of_recommendations]

        return {
            "recommended_tweets": results,
            "counts": sorted(counts, reverse=True)
        }

    def get_tweet_age_score(self, tweet):
        """Given a tweet object, this function returns the age
           of that tweet relative to a week. If a tweet is older than a week,
           then the rank equation will return a value that will completely
           de-weight the tweet, placing it at the very end of a recommendation list.
           This is to ensure that extremely old tweets a de-emphasized in the event 
           that they appear in the recommender objects self.followed_tweets attribute.

           Args:
               tweet: A tweet object from the Twitter REST API.

           Returns:
               A list of tweets, sorted by learned user preferences.
        """
        tweet_age = tweet['created_at']
        tweet_age = datetime.strptime(tweet_age, '%a %b %d %H:%M:%S +0000 %Y')  # dirty fix
        #tweet_age = tweet.created_at

        # http://stackoverflow.com/questions/23356523/how-can-i-get-the-age-of-a-tweet-using-tweepy
        age = time.time() - (tweet_age - datetime(1970, 1, 1)).total_seconds()
        week_seconds = 604800 # number of seconds in a week
        rank = (age / week_seconds) * self.numeric_scale
        return rank

    def count_bag_first_net(self, tweet):
        return self.count_bag(tweet, True)

    def count_bag_second_net(self, tweet):
        return self.count_bag(tweet, False)

    def count_bag(self, tweet, use_first_tf_doc):
        """This function is used in the generate method to sort tweets
           based on user preference and tweet content. 

           Args:
               tweet: A tweet object from the Twitter REST API.
               use_first_tf_doc: A boolean value used to determine whether 
               to use use the term frequency document or the "second net" 
               term frequency document.

           Returns:
               A numeric value used to rank the tweet.
        """

        count = 0.0
        sanitised_tweet_text = tweet['text']  # UNCOMMENT THIS LINE BEFORE COMMITTING AND COMMENT OUT LINE BELOW
        #sanitised_tweet_text = tweet.text
        hashtag = False
        term_frequency_document = self.termfreq_doc if use_first_tf_doc else self.second_net_termfreq_doc
        
        count += self.get_author_sentiment(tweet)


        # The following loop first checks if the word in the tweet
        # is a hastag, setting the hashtag boolean to true if it is.


        for word in sanitised_tweet_text.split():
            if word[0] == "#":
                new_word = word.replace("#", "")
                hashtag = True
            else:
                new_word = word
            for term in term_frequency_document.keys():
                if new_word.lower() == term:
                    count += 1
                    if hashtag == True:
                        count += (self.get_tweet_term_weighting(sanitised_tweet_text) * self.hash_tag_multiplier)
                    else:
                        count += self.get_tweet_term_weighting(sanitised_tweet_text)
        count -= self.get_tweet_age_score(tweet)####MOVED
        if count <= 0.0:
            count = 0.0 
        print(count)
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