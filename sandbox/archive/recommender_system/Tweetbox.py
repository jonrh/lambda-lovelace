class Tweetbox: 
     
    def __init__(self): 
        self.tweets = [] 
 
    def __init__(self, tweetbox): 
        self.tweets = tweetbox 
 
    def add_tweet(self, tweet): 
        self.tweets.append(tweet) 
 
    def all_tweets(self): 
        return self.tweets