# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import time
import string
from datetime import datetime
import rollbar
import operator
from Stopwords import Stopwords

"""This class takes in information about a users personal timeline,
   home timeline and iOS client feedback. It uses this information
   to recommend a personalized list of tweets for that particular
   user. This class is used in the Lovelace.py class for both the regular 
   and evaluator versions of the Lambda Lovelace iOS application and
   can be executed standalone by running the Execute_2.py file in a 
   Python environment.

   A functionality worth noting is the second net behaviour. This 
   functionality appears in the get_term_frequency_weightings and generate
   functions and essentially acts as a bigger version of the term frequency
   document. This is essentially an effort to organise any remaining tweets 
   that were not organised into a recommendation due to a lack of term 
   frequency document terms appearing in the tweet.

   At times, you will see lines of code that have alternate versions commented
   out beaneath them, such as the following example:

   sanitised_tweet_text = tweet['text']  # OSX
   #sanitised_tweet_text = tweet.text # Windows

   This is due to an inconsistency on getting the Python to work on multiple
   operating systems. In order to run this class stand-alone on Windows, simply
   comment out the # OSX line and uncomment the # Windows line, comment out the rollbar 
   import, comment out the debug_term_frequency_to_rollbar function on line 653 
   and comment out "self.debug_term_frequency_to_rollbar()" on line 279. 
   Then run the Execute_2.py file to see textual information from tweet belonging 
   to one of the Lambda Lovelace test accounts. Several print statements have been 
   commented out for your ease of testing the effect of changing variables for this 
   class to see what effect they have.

    Attributes:
        amount_of_tweets_to_gather: The max number of most recent 
        user tweets used when creating the term frequency document.
        
        top_x_terms: The amount of the most-occurring terms in tweets 
        that should be added to the term frequency document. In other 
        words, the top x ocucurring terms.
        
        second_net_multiplier: The multiple of top_x_terms that applies 
        to the amount of most-occurring terms in tweets that will be added
        to the second-net term frequency document.

        numeric_scale: On a scale up to X.0, what is the scale that the 
        term frequency document should follow. For example if set to 10.0,
        then all term frequency document term values will be in range of
        0.0 to 10.0.

        hash_tag_multiplier: How much are hashtags worth as opposed to terms 
        (worth 1, so 2 means that a hashtag is worth double the worth of a term).

        single_tweet_feedback: Variable to hold feedback from the iOS client.
        
        liked_tweets: Variable to hold liked tweet feedback from the 
        single_tweet_feedback variable.

        disliked_tweets: Variable to hold disliked tweet feedback from the 
        single_tweet_feedback variable.

        liked_authors: Variable to hold liked author feedback from the 
        single_tweet_feedback variable. Contains the name of several authors 
        repeatedly, and eventually this list is fed into the author_feedback variable.

        disliked_authors: Variable to hold disliked author feedback from the 
        single_tweet_feedback variable. Contains the name of several authors 
        repeatedly, and eventually this list is fed into the author_feedback variable.
        
        termfreq_doc: terms that hold significance to the user. Each term is 
        given a value that is a fraction taken from the numeric_scale value.
        The larger the fraction, the greater the significance.

        second_net_termfreq_doc: A larger version of the termfreq_doc. This 
        is used to recommended less important tweets to the user.

        more_or_less_from_this_author_multiplier: The value given to each 
        like/dislike of an author when making recommendations.

        like_and_dislike_multiplier: The value given to each 
        like/dislike of a tweet when making recommendations.

        own_tweets: Tweets from the users user timeline.
        
        followed_tweets: Tweets from the users home timeline.
        
        author_feedback: An overall dictionary of all author feedback, 
        and the extent to which a user likes/dislikes an author.
        
        vectorizer: A CountVectorizer object from the scikit-learn library.     
"""

class RecommenderTextual:

    def __init__(self, users_own_tweets, users_followed_tweets, single_tweet_feedback):
        self.amount_of_tweets_to_gather = 101
        self.top_x_terms = 23
        self.second_net_multiplier = 2
        self.numeric_scale = 10
        self.hash_tag_multiplier = 2
        self.single_tweet_feedback = single_tweet_feedback
        self.liked_tweets = []
        self.disliked_tweets = []
        self.liked_authors = []
        self.disliked_authors = []
        self.termfreq_doc = {}
        self.second_net_termfreq_doc = {}
        self.more_or_less_from_this_author_multiplier = 2.5 # Set at 5.1 for final presentation
        self.like_and_dislike_multiplier = 0.125 # Set at 10.1 for final presentation
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

    def set_feedback(self):
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

    def get_term_frequency_weightings(self):
        """Creates weightings for the term frequency document.
       
           This function sets the recommender objects termfreq_doc
           and second_net_termfreq_doc attributes.

           Args:
               No arguments

           Returns:
               Nothing. This function is used to set attributes within
               the Recommender object.
        """
        
        second_net_top_x_terms = self.top_x_terms * self.second_net_multiplier

        # http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
        exclude = set(string.punctuation)
        
        # generate a list of stop words
        stop_words = [word for word in CountVectorizer(stop_words='english').get_stop_words()]
        stop_words.append('rt')
        stop_words.append('https')

        # Filtering section
        # In this section, the users tweets are iterated through and any
        # words that are not stopwords are added to the overall_list list.
        # Hashtags are also added.
        my_first_x_tweets = self.own_tweets[0: self.amount_of_tweets_to_gather]
        overall_list = []
        stop_words_list = Stopwords()
        long_stop_words = stop_words_list.return_stopwords()
        for sublist in my_first_x_tweets:
            for item in sublist['text'].split(): # OSX
            #for item in sublist.text.split():# Windows
                if item.lower() not in stop_words and item.lower() not in long_stop_words:
                    # https://www.quora.com/How-do-I-remove-punctuation-from-a-Python-string
                    word = item.lower()
                    transformed_item = ''.join(c for c in word if c not in string.punctuation)
                    overall_list.append(transformed_item)

            # Iterate over the hastags (again). This essentially makes hashtags
            # count "twice".
            for hashtag in sublist['entities']['hashtags']: # OSX
            #for hashtag in sublist.entities['hashtags']: # Windows
                tag = hashtag['text'].lower()
                # https://www.quora.com/How-do-I-remove-punctuation-from-a-Python-string
                overall_list.append(''.join(c for c in tag if c not in string.punctuation))

        total_count = len(overall_list)
        frequency_doc = Counter(overall_list)
        second_net_frequency_doc = Counter(overall_list)
        term_frequency_list = {}


        # This loop assigns values to each term that the term frequency
        # document will eventually be comprised of
        print("FREQ")
        print(frequency_doc)
        for term in frequency_doc.keys():
            hashtag = u'#' + term

            # If a hash-tagged term has been added to the frequency_doc list, find it again
            hashtag_value = float(frequency_doc.get(hashtag)) if frequency_doc.get(hashtag) is not None else 0.0
            
            term_value = float(frequency_doc.get(term))
            term_weight = ((hashtag_value + term_value)/total_count) * self.numeric_scale
            term_frequency_list[term] = term_weight

        #Shallow copies, as the term_frequency_list is not "deep"
        self.termfreq_doc = term_frequency_list.copy()
        self.second_net_termfreq_doc = term_frequency_list.copy()

        top_terms = []
        second_net_top_terms = []

        # The last index of the first term frequency document will be self.top_x_terms,
        # unless that value is higher then the number of elements in the frequency_doc list
        last_index = self.top_x_terms if len(frequency_doc) > self.top_x_terms else len(frequency_doc)

        # The last index of the second net term frequency document will be second_net_top_x_terms,
        # unless that value is higher then the number of elements in the frequency_doc list
        second_net_last_index = second_net_top_x_terms if len(frequency_doc) > second_net_top_x_terms else len(frequency_doc)

        # the most_common() function return the X most ocurring elements in
        # the Counter object being called upon, where X is the argument.
        most_common_raw = frequency_doc.most_common(last_index) 
        second_net_most_common_raw = frequency_doc.most_common(second_net_last_index)

        # Simply take the values from the above variables and place up to the final index
        # of each variable into a new variable (top_terms and second_net_top_terms)
        for x in range(0, last_index):
            top_terms.append(most_common_raw[x][0])

        for x in range(0, second_net_last_index):
            second_net_top_terms.append(second_net_most_common_raw[x][0])

        # Remove terms from both the first and second term frequency documents
        # if they are not in their respective top term list.
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
        
        if "" in self.termfreq_doc.keys():
            print("POPPED the empty string!")
            self.termfreq_doc.pop("")
        else:
            print("Did not POP an empty string...")

    def get_author_sentiment(self, tweet):
        """Retrieve author sentiment for a tweet object.

           Args:
               tweet: A tweet object from the Twitter REST API.

           Returns:
               A numeric score, reflective of the users preferences
               based on the author_feedback object
        """
        author_name = tweet['user']['screen_name'] # OSX
        #author_name = tweet.author.screen_name # Windows
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
           balance_reduce_term_freq_doc_preference function with 
           those terms as arguments.

           Args:
               tweet: A tweet object from the Twitter REST API.

           Returns:
               Nothing. This function calls the balance_reduce_term_freq_doc_preference
               with the terms that need to be reduced in weight.
        """
        tweet_text = tweet
        #print("tweet")
        #print(u"DISLIKED " + tweet_text)
        terms_to_reduce = set() # We only want to reduce each term once
        for word in tweet_text.replace("\n"," ").split():
            unhashedword = word.lower()
            if word.startswith("#"):
                unhashedword = unhashedword[1:]
            if self.termfreq_doc.has_key(unhashedword):
            #if unhashedword in self.termfreq_doc.keys():
                terms_to_reduce.add(unhashedword)

        # Only execute this method if there is a term in the tweets text that can be reduced.
        # This means that disliking a tweet that does not contain a term will have no effect, but
        # these terms are towards the end of the recommended list anyway.
        if len(terms_to_reduce) >= 1:
            self.balance_reduce_term_freq_doc_preference(terms_to_reduce)
        
    def balance_reduce_term_freq_doc_preference(self, terms_to_reduce):
        """Given the terms that should be reduced from the
           get_disliked_tweets_terms_and_reduce function,
           find them in the term frequency document and reduce
           the value of their weightings. Increase the value of
           all other terms in proportion to the total weight reduced 
           in the term frequency document to maintain the chosen 
           ratio (the value of self.numeric_scale). For example, if a term
           is to be decreased in a term frequcny document by 1, then the 
           remaining two terms should be increased by 0.5.

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

    def get_liked_terms_and_increase_weighting(self, tweet):
        """Retrieve terms whose value will be increased due to their
           appearance in a liked tweet object and call the 
           balance_increase_term_freq_doc_preference function with 
           those terms as arguments.

           Args:
               tweet: A tweet object from the Twitter REST API.

           Returns:
               Nothing. This function calls the balance_increase_term_freq_doc_preference
               with the terms that need to be increased in weight.
        """
        tweet_text = tweet
        #print("Tweet")
        #print("LIKED" + str(tweet_text))
        terms_to_increase = set() # We only want to increase each term once
        for word in tweet_text.replace("\n"," ").split():
            unhashedword = word.lower()
            if word.startswith("#"):
                unhashedword = unhashedword[1:]
            if self.termfreq_doc.has_key(unhashedword):
            #if unhashedword in self.termfreq_doc.keys():
                terms_to_increase.add(unhashedword)

        # Only execute this method if there is a term in the tweets text that can be increased.
        # This means that liking a tweet that does not contain a term will have no effect, but
        # the more the user tweets/retweets/likes on Twitter, the more likely these terms will appear.
        if len(terms_to_increase) >= 1:
            self.balance_increase_term_freq_doc_preference(terms_to_increase)

    def balance_increase_term_freq_doc_preference(self, terms_to_increase):
        """Given the terms that should be increased from the
           get_liked_terms_and_increase_weighting function,
           find them in the term frequency document and increase
           the value of their weightings. Decrease the weighting value of
           all other terms in proportion to the total weight increase 
           in the term frequency document to maintain the chosen 
           ratio (the value of self.numeric_scale). For example, if a term
           is to be increased in a term frequcny document by 1, then the 
           remaining two terms should be decreased by 0.5.

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


    def find_older_tweets_to_remove(self, tweet_list, how_many_days_ago):
        """Given a number, find all tweets in a set that are older than
           that number of days from the current time. 

           Args:
               tweet_list: A list of tweets from this objects self.followed_tweets
               field
               how_many_days_ago: A cut-off point for the age of tweets recommended.
               E.g. a value of 1 ensures that no returned tweets will be older than
               a day.

           Returns:
               A list of tweets, to be removed as they are too old for
               the calling function.
        """

        max_age_in_seconds = how_many_days_ago * 86400  # 86400 is the number of seconds in a single day.
        seconds_ago = 0
        # If the caller wants tweets older than a week, simply set the value to one week.
        # The twitter API does not currently allow third-party developers to request tweets older
        # than a week, so setting this value to one week is simply a safety-check (in the
        # event that twitter changes it's stance on this limit. We do not know what other stipulations
        # Twitter may impose on retrieving tweets older than a week). 
        if how_many_days_ago > 7:
            max_age_in_seconds = 7 * 86400
        remove_these_tweets = []

        for tweet in tweet_list:
            # http://stackoverflow.com/questions/23356523/how-can-i-get-the-age-of-a-tweet-using-tweepy
            #tweet_age = tweet.created_at # Windows
            tweet_age = tweet['created_at'] # OSX
            tweet_age = datetime.strptime(tweet_age, '%a %b %d %H:%M:%S +0000 %Y')  # OSX
            tweet_age_in_seconds = time.time() - (tweet_age - datetime(1970, 1, 1)).total_seconds()
            if tweet_age_in_seconds > max_age_in_seconds:
                remove_these_tweets.append(tweet)
        return remove_these_tweets

    def generate(self, number_of_recommendations, how_many_days_ago):
        """The actual recommendation generation function. This function
           uses the term frequency document and second net term frequency
           document to sort a list of the users followed tweets by preference. 

           Args:
               number_of_recommendations: the total amount of recommendations
               that the caller needs from this recommender objects list of
               followed tweets.
               how_many_days_ago: A cut-off point for the age of tweets recommended.
               E.g. a value of 1 ensures that no returned tweets will be older than
               a day.

           Returns:
               A list of tweets, sorted by learned user preferences.
        """
        
        # The users own tweets
        words = self.own_tweets
        # tweets from accounts that the user is following, the recommendation set
        tweet_list = self.followed_tweets  


        # Use the find_older_tweets_to_remove function to find tweets that are older
        # than the how_many_days_ago function (in terms of days). 
        tweets_exceeding_days_ago_limit = self.find_older_tweets_to_remove(tweet_list, how_many_days_ago)

        # Remove the tweets found above from the set of tweets to be recommended.
        for removal in tweets_exceeding_days_ago_limit:
            tweet_list.remove(removal)

        #Dubbed prelim_results, as the second net has yet to take effect.
        prelim_results = tweet_list
        tweets_that_contain_tf_terms = []
        tweets_that_do_not_contain_tf_terms = []

        # Find tweets that the first net can be applied to (Those that contain
        # terms found in the first term frequency document).
        for tweet in prelim_results:
            for term in self.termfreq_doc.keys():
                if term in tweet['text'].lower(): # OSX
                #if term in tweet.text.lower(): # Windows
                    tweets_that_contain_tf_terms.append(tweet)
                    break

        # Find tweets that the second net can be applied to (Those that do not 
        # contain terms from the first term frequency document).
        for tweet in prelim_results:
            if tweet not in tweets_that_contain_tf_terms:
                tweets_that_do_not_contain_tf_terms.append(tweet)

        # Sort both sets of the good (tweets_that_contain_tf_terms) and
        # bad (tweets_that_do_not_contain_tf_terms) tweets according
        # to their term frequency document.
        term_tweets_sorted = sorted(tweets_that_contain_tf_terms, key=self.count_bag_first_net, reverse=True)
        non_term_tweets_sorted = sorted(tweets_that_do_not_contain_tf_terms, key=self.count_bag_second_net, reverse=True) 

        # Essentially, we are performing the same action again here in order
        # to get a numeric value to be used in the iOS apps colour-coded indicator
        # of tweet preference.
        counts_for_term_tweets = [self.count_bag_first_net(tweet) for tweet in term_tweets_sorted]
        counts_for_non_term_tweets = [self.count_bag_second_net(tweet) for tweet in non_term_tweets_sorted]

        # Append the good sets of tweets with the bad sets of tweets.
        # This ensures that both sets remain separate in a sense,
        # that there are two tiers of preference with each using 
        # a different term frequency document with a different quality
        # of terms.
        counts_for_term_tweets.extend(counts_for_non_term_tweets)
        term_tweets_sorted.extend(non_term_tweets_sorted)

        # Shave off excess tweets and give the calling function back
        # the number of tweets requested.
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
        tweet_age = tweet['created_at'] # OSX
        tweet_age = datetime.strptime(tweet_age, '%a %b %d %H:%M:%S +0000 %Y')  # OSX
        #tweet_age = tweet.created_at # Windows

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
        sanitised_tweet_text = tweet['text']  # OSX
        #sanitised_tweet_text = tweet.text # Windows
        hashtag = False
        term_frequency_document = self.termfreq_doc if use_first_tf_doc else self.second_net_termfreq_doc
        count += self.get_author_sentiment(tweet)


        # The following loop first checks if the word in the tweet
        # is a hastag, setting the hashtag boolean to true if it is.
        # Then, a check is used to see if the term is in the term
        # frequency document. If it is, then add the value of that
        # term (plus 1) to the count, multiplying it by the hash_tag_multiplier 
        # variable if the term is a hashtag. Then subtract the number returned
        # by the get_tweet_age_score function for that tweet, and finally
        # return the resulting count. If the count is below zero, return it
        # to zero.


        for word in sanitised_tweet_text.split():
            if word[0] == "#":
                text_word = word.lower().replace("#", "")
                hashtag = True
            else:
                text_word = word.lower()
            if term_frequency_document.has_key(text_word):
            #if text_word in term_frequency_document.keys():
                count += 1
                print("Found term:" + str(text_word))
                if hashtag == True:
                    count += (self.termfreq_doc.get(text_word) * self.hash_tag_multiplier)
                    hashtag = False
                else:
                    count += self.termfreq_doc.get(text_word)
        
        count -= self.get_tweet_age_score(tweet)
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