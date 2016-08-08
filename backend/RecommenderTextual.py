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
        self.single_tweet_feedback = single_tweet_feedback #{"me":"m"}#single_tweet_feedback["author"]
        self.liked_tweets = []#single_tweet_feedback["like"]
        self.disliked_tweets = []#single_tweet_feedback["dislike"]
        self.liked_authors = []#single_tweet_feedback["like"]
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
            self.get_liked_weighting(tweet_text)
        for tweet_text in self.disliked_tweets:
            self.get_dislike_weighting(tweet_text)

    def set_author_sentiment(self):
        author_feedback = {}
        for author in self.disliked_authors:
            print("author")
            print(str(author) + " disliked!")
            author_feedback[author] = author_feedback.get(author, 0) - 1
        for author in self.liked_authors:
            print("author")
            print(str(author) + " liked!")
            author_feedback[author] = author_feedback.get(author, 0) + 1
        return author_feedback

    '''def contains_tweet_text(self, tlist, test_tweet):
        contain = False
        for tweet in tlist:
            #if tweet['text'] == test_tweet['text']:
            if tweet.text == test_tweet.text:
                contain = True
        return contain'''

    def set_feedback(self):
        #WORKS
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

    # This method gets the top x terms that a users tweets with
    def get_term_frequency_weightings(self):
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
            # hashtag = str(u'#{}'.format(term))#.encode('utf-8')
            hashtag = u'#' + term
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
        author_name = tweet['user']['screen_name']
        #author_name = tweet.author.screen_name
        print("scored")
        score = 0.0
        print(str(author_name.lower().encode("utf-8")))
        for name in self.author_feedback.keys():
            if str(author_name.lower().encode("utf-8")) == str(name.lower().encode("utf-8")):
                feedback_score = self.author_feedback.get(author_name)
                multiplier = self.more_or_less_from_this_author_multiplier
                scale = self.numeric_scale
                score = float(feedback_score)/float(scale) * float(multiplier)
        print(score)
        return score

    def get_dislike_weighting(self, tweet):
        #WORKS
        tweet_text = tweet#['text']#.lower()
        #tweet_text = tweet#.text.lower()
        print("tweet")
#        print(u"DISLIKED " + tweet_text)
        terms_to_reduce = set() # We only want to reduce each term once
        for word in tweet_text.replace("\n"," ").split():
            unhashedword = word
            if word.startswith("#"):
                unhashedword = unhashedword[1:]
            for term in self.termfreq_doc.keys():
                if unhashedword == term:
                    terms_to_reduce.add(str(term))#Add the term, because a "term" can be inside another full word (Javacodegeeks for Java)
        
        # Only execute this method if there is a term in the tweets text that can be reduced.
        # This means that disliking a tweet that does not contain a term will have no effect, but
        # these terms are towards the end of the recommended list anyway.
        if len(terms_to_reduce) >= 1:
            self.balance_reduce_term_freq_doc_preference(terms_to_reduce)
        
    def balance_reduce_term_freq_doc_preference(self, terms_to_reduce):
        num_of_reduced_terms = len(terms_to_reduce)
        num_of_terms = len(self.termfreq_doc.keys())
        alter_value = self.like_and_dislike_multiplier
        reduce_value = alter_value/num_of_reduced_terms 
        increase_value = alter_value/(num_of_terms - num_of_reduced_terms) 
        increase_terms = []
        for key in self.termfreq_doc.keys():
            if str(key) not in terms_to_reduce:
                increase_terms.append(str(key))

        for term in terms_to_reduce:
            print("reducing from " + str(term) + " with " + str(reduce_value))
            self.termfreq_doc[term] -= reduce_value

        for term in increase_terms:
            print("adding to " + str(term) + " with " + str(increase_value))
            self.termfreq_doc[term] += increase_value

    def get_liked_weighting(self, tweet):
        #WORKS
        tweet_text = tweet#['text']#.lower()
        #tweet_text = tweet#.text.lower()
        print("Tweet")
#        print("LIKED" + str(tweet_text))
        terms_to_increase = set() # We only want to increase each term once
        for word in tweet_text.replace("\n"," ").split():
            unhashedword = word
            if word.startswith("#"):
                unhashedword = unhashedword[1:]
            for term in self.termfreq_doc.keys():
                if unhashedword == term:
                    terms_to_increase.add(str(term))

        # Only execute this method if there is a term in the tweets text that can be increased.
        # This means that liking a tweet that does not contain a term will have no effect, but
        # the more the user tweets/retweets/likes on Twitter, the more likely these terms will appear.
        if len(terms_to_increase) >= 1:
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
            print("adding to " + str(term) + " with " + str(increase_value))
            self.termfreq_doc[term] += increase_value

        for term in reduce_terms:
            print("reducing from " + str(term) + " with " + str(reduce_value))
            self.termfreq_doc[term] -= reduce_value


    def generate(self, number_of_recommendations, how_many_days_ago):
        """What does this function do?"""
        #WORKS
        max_age_in_seconds = how_many_days_ago * 86400  # number of seconds in 1 day
        seconds_ago = 0
        if how_many_days_ago > 7:
            max_age_in_seconds = 1000000

        #for tweet in self.own_tweets:
        #    list_of_owners_tweets.append(tweet.text.encode('utf-8'))
            #list_of_owners_tweets.append(tweet['text'].encode('utf-8'))  # UNCOMMENT THIS LINE BEFORE COMMITTING AND COMMENT OUT LINE ABOVE

        #self.vectorizer.fit_transform(list_of_owners_tweets)
        words = self.own_tweets  # The users own tweets
        tweet_list = self.followed_tweets  # tweets from accounts that the user is following

        '''tweet_list = []
        for tweet in tweet_list_x:
            if self.contains_tweet_text(tweet_list, tweet):
                continue
            else:
                tweet_list.append(tweet)'''

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
        tweet_age = tweet['created_at']
        tweet_age = datetime.strptime(tweet_age, '%a %b %d %H:%M:%S +0000 %Y')  # dirty fix
        #tweet_age = tweet.created_at

        # http://stackoverflow.com/questions/23356523/how-can-i-get-the-age-of-a-tweet-using-tweepy
        age = time.time() - (tweet_age - datetime(1970, 1, 1)).total_seconds()
        week_seconds = 604800 # 604800 seconds in a week
        rank = (age / week_seconds) * self.numeric_scale
        return rank

    def count_bag_first_net(self, tweet):
        return self.count_bag(tweet, True)

    def count_bag_second_net(self, tweet):
        return self.count_bag(tweet, False)

    def count_bag(self, tweet, use_first_tf_doc):
        count = 0.0
        sanitised_tweet_text = tweet['text']  # UNCOMMENT THIS LINE BEFORE COMMITTING AND COMMENT OUT LINE BELOW
        #sanitised_tweet_text = tweet.text
        hashtag = False
        term_frequency_document = self.termfreq_doc if use_first_tf_doc else self.second_net_termfreq_doc
        # bug
        # Somehow, the following tweet is being counted as six (should be three)
        # Tweet!
        # Guavate: tiny library bridging Guava and Java8 - Core Java Google Guava, Guavate, Java 8 https://t.co/kQnWkUy9V7
        # count!
        # 6

        count += self.get_author_sentiment(tweet)
        if tweet in self.disliked_tweets:
            self.get_dislike_weighting(tweet)

        if tweet in self.liked_tweets:
            self.get_liked_weighting(tweet)

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
                    count -= self.get_tweet_age_score(tweet)
                    if count <= 0.0:
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