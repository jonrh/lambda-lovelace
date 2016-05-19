
class Recommender:
	
 def generate(self, tweets, number_of_recommendations, followed_accounts, how_many_days_ago):
  #recommendations = []
  begin_string = "String here, you want "
  middle_string = " recommendations, that are at most "
  end_string = "days old"
  return  begin_string + str(number_of_recommendations) +  middle_string + str(how_many_days_ago) + end_string #recommendations