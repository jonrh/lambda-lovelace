from sklearn.feature_extraction.text import CountVectorizer

class Recommender:
    
    def __init__(self, followed_tweets):
        self.followed_tweets = followed_tweets
        self.vectorizer = CountVectorizer()

    def generate(self, user_tweets, number_of_recommendations, followed_accounts, how_many_days_ago):
        self.vectorizer.fit_transform(user_tweets)
        terms = self.vectorizer.get_feature_names()
        words = user_tweets
        results = sorted(self.followed_tweets, key=self.count_bag, reverse=True)
        
        return results

    def count_bag(self, user_tweets):
        count = 0
        terms = self.vectorizer.get_feature_names()
        words = user_tweets.split()
        
        for word in words:
            if word in terms:
                count += 1

        return count