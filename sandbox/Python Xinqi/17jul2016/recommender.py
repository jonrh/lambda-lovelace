from sklearn.feature_extraction.text import CountVectorizer

class Recommender:

    def __init__(self, followed_tweets, users_tweets):
        self.followed_tweets = followed_tweets
        self.users_tweets = users_tweets
        self.vectorizer = CountVectorizer()
        self.counts = []

    def generate(self, number_of_recommendations, followed_accounts, how_many_days_ago):

        #generate a count list
        counts = [self.count_bag(tweet) for tweet in self.followed_tweets]
        
        #return sorted home timeline and sorted list of count
        return {"recommended_tweets":sorted(self.followed_tweets, key=self.count_bag, reverse=True), "counts":sorted(counts, reverse=True)}

    def count_bag(self, item):

        # generate a list of stop words
        stop_words = [word for word in CountVectorizer(stop_words='english').get_stop_words()]
        stop_words.append('rt')#retweets
        stop_words.append('https')#urls

        # fetch the text of user's own timeline
        users_tweets_text = [tweet['text'] for tweet in self.users_tweets]

        # for user's own timeline, tokenize words, convert to lowercase, filter out stop words
        #generate a list of terms of the user's own timeline
        tokenize = self.vectorizer.build_tokenizer()
        terms = [word.lower() for sentence in users_tweets_text
                 for word in tokenize(sentence)
                 if len(word.lower()) > 1 and word.lower() not in stop_words]
                 
        
        count = 0
        #for each tweet in home timeline, tokenize words, convert to lowercase, filter out stop words
        words = [word.lower() for word in tokenize(item['text'])
                 if len(word.lower()) > 1 and word.lower() not in stop_words]

        #the for each word in words, if it exists in the terms of user's own timeline, the increase count by one
        #at last
        for word in words:
            if word in terms:
                count += 1

        return count