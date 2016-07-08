from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import time

consumer_key="KOUIbWm4VWYzI0uuQLogzGRa0"
consumer_secret="r5Ac1fwLmuYFYL6biR4E1iYzS8S78DInUNM3AQ76EeMDBBVSFL"

access_token="733308744638038017-oZYXhQOz1qUgTe2Sex3PctTMbkfM1dJ"
access_token_secret="3jAoAPk2krE9KClg4XC0MIDLlpAMKUumi6cDSnf5gtWJk"

class Streaming(StreamListener):#, number_of_tweets):

    def __init__(self):
        super(Streaming, self).__init__()
        self.max_number_of_tweets = 1#number_of_tweets
        self.streamed_tweets = []

    def get_tweets(self):
        print("get_tweets here")
        print(self.streamed_tweets)
        return self.streamed_tweets

    def get_max(self):
        print("get_max here")
        print(self.max_number_of_tweets)
        return self.max_number_of_tweets

    def on_status(self, status):
        #if len(self.tweets) <= self.max_number_of_tweets:
        #self.tweets.append(status)
        print("Status Tweet")
        #print(status.text.encode("utf-8"))
        #if len(self.tweets) == self.max_number_of_tweets:
        #    return False

    def on_data(self, data):
        print("BQU")
        #print(data)
        self.streamed_tweets.append(data)
        print("Added Data, here is currently stored tweets:")
        self.max_number_of_tweets += 1
        print(self.get_tweets[0])
        if len(self.streamed_tweets) == self.max_number_of_tweets:
            return False
    
    def on_error(self, status):
        print(status)

    def stream(self, term):
        strm = Streaming()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.stream = Stream(auth, strm)
        print("Searching for...")
        print(term)
        self.stream.filter(track=[term], async=True)
        time.sleep(5)
        self.stream.disconnect()
            

'''if __name__ == '__main__':
    l = Streaming()
    self.auth = OAuthHandler(consumer_key, consumer_secret)
    self.auth.set_access_token(access_token, access_token_secret)

    self.stream = Stream(auth, l)
    self.stream.filter(track=['basketball'])'''