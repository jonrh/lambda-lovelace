from sklearn.feature_extraction.text import CountVectorizer 
from collections import Counter 
import operator 
 
tokenize = CountVectorizer().build_tokenizer() 
 
tweets = ["This is text here","This is a text here", "This is here","this is also a bunch of text", "Down three levels!"] 
end_result = [] 
 
#Filtering section 
overall_list = [] 
for tweet in tweets:  
    for word in tweet.split(): 
        overall_list.append(word) 
  #  for hashtag in tweets.hashtags 
  #      overall_list.append(hashtag) 
  #      overall_list.append(hashtag) 
 
term_frequencies = Counter(overall_list) 
term_freq_top_five = term_frequencies.most_common(5)  
 
print(term_freq_top_five) 
 
print(term_frequencies)