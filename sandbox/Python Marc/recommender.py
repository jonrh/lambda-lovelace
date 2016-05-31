
class Recommender:
	
 def generate(self, tweets, number_of_recommendations, followed_accounts, how_many_days_ago, dict_of_followed_tweets):
  recommendations = [10]
  chosen_tweeter = "MarcLaffan"
  recommendations[0] = dict_of_followed_tweets[chosen_tweeter][0].text
  begin_string = "I recommend the following tweet by "
  return  begin_string + chosen_tweeter + ": " + str(recommendations[0])