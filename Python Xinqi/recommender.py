import tweepy
import json
import pandas as pd
from collections import Counter

class Recommender:

    def generate(self, tweets, number_of_recommendations, followed_accounts, how_many_days_ago):
        #recommendations = []
        begin_string = "String here, you want "
        middle_string = " recommendations, that are at most "
        end_string = "days old"
        return  begin_string + str(number_of_recommendations) +  middle_string + str(how_many_days_ago) + end_string #recommendations


    def accounts_recommender(self,results):
        tweets = results

        user_mentions = [user_mention['screen_name']
                            for status in results
                            for user_mention in status['entities']['user_mentions']]

        count = Counter(user_mentions)
        mentions_counts = count.most_common()

        users = [user['user']['screen_name']
                    for user in results]

        user_count = Counter(users)
        users_counts = user_count.most_common()

        return mentions_counts[:3], users_counts[:3]