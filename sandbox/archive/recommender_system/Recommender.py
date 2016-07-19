# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
from Tweetbox import Tweetbox
from collections import Counter
import tweepy
import time
import string


class Recommender:
    
    #TO-DO:
    #-set language to users own twitter language
    #-currently misses end hashtags
    #-Does not search for hashtags, just "word-searches"
    #-does not add hashtags to term-frequency document
    #-does not distinguish Java from JavaScript (Could use a bigram list for this)
    
    def __init__(self, ckey, csecret, atoken, atokensecret):
        self.vectorizer = CountVectorizer()
        consumer_key = ckey
        consumer_secret = csecret
        access_token = atoken
        access_token_secret = atokensecret
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)
        self.set_own_tweets()#Set the users tweets aas a variable
        self.set_followed_tweets()#Grab the users home timeline and set it as an attribute
        self.get_term_frequency_weightings(None, None)

    #This method sets the "followed_tweets" attribute for the recommender object. Followed tweets are ones that we make recommendations upon.
    def set_followed_tweets(self):
        self.followed_tweets = self.api.home_timeline()

    ###To-do: using this method does not work on line 78
    def has_bad_words(self, tweet):
        print('has_bad_words_here')
        print(tweet.text.encode('utf-8'))
        bad_word = False
        #https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/blob/master/en
        list_of_bad_words = ['2g1c','2 girls 1 cup','acrotomophilia','alabama hot pocket','alaskan pipeline','anal','anilingus','anus','apeshit','arsehole','ass','asshole','assmunch','auto erotic','autoerotic','babeland','baby batter','baby juice','ball gag','ball gravy','ball kicking','ball licking','ball sack','ball sucking','bangbros','bareback','barely legal','barenaked','bastard','bastardo','bastinado','bbw','bdsm','beaner','beaners','beaver cleaver','beaver lips','bestiality','big black','big breasts','big knockers','big tits','bimbos','birdlock','bitch','bitches','black cock','blonde action','blonde on blonde action','blowjob','blow job','blow your load','blue waffle','blumpkin','bollocks','bondage','boner','boob','boobs','booty call','brown showers','brunette action','bukkake','bulldyke','bullet vibe','bullshit','bung hole','bunghole','busty','butt','buttcheeks','butthole','camel toe','camgirl','camslut','camwhore','carpet muncher','carpetmuncher','chocolate rosebuds','circlejerk','cleveland steamer','clit','clitoris','clover clamps','clusterfuck','cock','cocks','coprolagnia','coprophilia','cornhole','coon','coons','creampie','cum','cumming','cunnilingus','cunt','darkie','date rape','daterape','deep throat','deepthroat','dendrophilia','dick','dildo','dingleberry','dingleberries','dirty pillows','dirty sanchez','doggie style','doggiestyle','doggy style','doggystyle','dog style','dolcett','domination','dominatrix','dommes','donkey punch','double dong','double penetration','dp action','dry hump','dvda','eat my ass','ecchi','ejaculation','erotic','erotism','escort','eunuch','faggot','fecal','felch','fellatio','feltch','female squirting','femdom','figging','fingerbang','fingering','fisting','foot fetish','footjob','frotting','fuck','fuck buttons','fuckin','fucking','fucktards','fudge packer','fudgepacker','futanari','gang bang','gay sex','genitals','giant cock','girl on','girl on top','girls gone wild','goatcx','goatse','god damn','gokkun','golden shower','goodpoop','goo girl','goregasm','grope','group sex','g-spot','guro','hand job','handjob','hard core','hardcore','hentai','homoerotic','honkey','hooker','hot carl','hot chick','how to kill','how to murder','huge fat','humping','incest','intercourse','jack off','jail bait','jailbait','jelly donut','jerk off','jigaboo','jiggaboo','jiggerboo','jizz','juggs','kike','kinbaku','kinkster','kinky','knobbing','leather restraint','leather straight jacket','lemon party','lolita','lovemaking','make me come','male squirting','masturbate','menage a trois','milf','missionary position','motherfucker','mound of venus','mr hands','muff diver','muffdiving','nambla','nawashi','negro','neonazi','nigga','nigger','nig nog','nimphomania','nipple','nipples','nsfw images','nude','nudity','nympho','nymphomania','octopussy','omorashi','one cup two girls','one guy one jar','orgasm','orgy','paedophile','paki','panties','panty','pedobear','pedophile','pegging','penis','phone sex','piece of shit','pissing','piss pig','pisspig','playboy','pleasure chest','pole smoker','ponyplay','poof','poon','poontang','punany','poop chute','poopchute','porn','porno','pornography','prince albert piercing','pthc','pubes','pussy','queaf','queef','quim','raghead','raging boner','rape','raping','rapist','rectum','reverse cowgirl','rimjob','rimming','rosy palm','rosy palm and her 5 sisters','rusty trombone','sadism','santorum','scat','schlong','scissoring','semen','sex','sexo','sexy','shaved beaver','shaved pussy','shemale','shibari','shit','shitblimp','shitty','shota','shrimping','skeet','slanteye','slut','s&m','smut','snatch','snowballing','sodomize','sodomy','spic','splooge','splooge moose','spooge','spread legs','spunk','strap on','strapon','strappado','strip club','style doggy','suck','sucks','suicide girls','sultry women','swastika','swinger','tainted love','taste my','tea bagging','threesome','throating','tied up','tight white','tit','tits','titties','titty','tongue in a','topless','tosser','towelhead','tranny','tribadism','tub girl','tubgirl','tushy','twat','twink','twinkie','two girls one cup','undressing','upskirt','urethra play','urophilia','vagina','venus mound','vibrator','violet wand','vorarephilia','voyeur','vulva','wank','wetback','wet dream','white power','wrapping men','wrinkled starfish','xx','xxx','yaoi','yellow showers','yiffy','zoophilia','🖕']
        custom_bad_word_list = ['@peggingdating:', 'pegged', 'peggingdating:', 'strapon', 'femdom', 'manpussy', 'kinky']
        for word in tweet.text.split():
            if (word.encode('utf-8').lower() in list_of_bad_words) or (word.encode('utf-8').lower() in custom_bad_word_list):
                bad_word = True

        for tag in tweet.entities['hashtags']:
            print('Tags Here')
            print(tag)
            if (str(tag).lower() in list_of_bad_words) or (str(tag).lower() in custom_bad_word_list):
                bad_word = True

        return bad_word

    #This method using the streaming object and term frequency doc to find new tweets from unfollowed accounts 
    def get_unfollowed_tweets(self, term):
        #streaming_obj = Streaming()
        #streaming_obj.stream(term)

        #To-do: Ignore tweets containing pornographic term such as the following:
        #RT @PeggingDating: RT if u want ur man pussy fucked
        #https://t.co/0SpIwNe7w2
        #fucktoy #ladycock #manpussy https://t.co/etVFsuu8ws
        #Write Comment Here https://t.co/9ExueyfZyV
        #GayFriends #colorado #gay Hello, I'm a chubby virgin in 
        #search of someone to use my ass - 18: Please pickÔÇª #gaydate https://t.co/BgPZevKngj

        tweets = self.api.search(q=term, count=3, lang=["english"]) # languages=["english"], locale=["english"], 
        #print(" unfollowed tweets here for:")
        #print(term)
        #for tweet in tweets:
        #    print tweet.text.encode('utf-8')
        
        removed = []

        for tweet in tweets:
            if self.has_bad_words(tweet):
                print("*****")
                print("*****")
                print("This tweet has bad words")
                print(tweet.text.encode('utf-8'))
                print("*****")
                print("*****")
                removed.append(tweet)
                tweets.remove(tweet)

        print("all bad tweets")
        for tweet in removed:
            print("*****")
            print(tweet.text.encode('utf-8'))
            print("*****")

        print("alltweets")
        for tweet in tweets:
            print("*****")
            print(tweet.text.encode('utf-8'))
            print("*****")
        return tweets

    #This method sets the "own_tweets" attrribute for the recommender object. These are tweets
    #from the users personal timeline, used to make the term frequncy document.   
    def set_own_tweets(self):                                      
        self.own_tweets = self.api.user_timeline()

    #This method currently gets the top thirty terms that a users tweets with
    def get_term_frequency_weightings(self, number_of_terms_in_document, number_of_user_timeline_tweets):
        weightings = {}#Dictionary of terms (keys) and their weighting (value)
        top_amount_of_terms = 30# or just the "number_of_terms_in_document" parameter
        amount_of_tweets_to_gather = 101#Or just the "number_of_user_timeline_tweets" parameter, + 1
                                        #The extra "1" is because python is not inclusive of the last digit in the range that 
                                        #this variable is used for later on.
        
        #On a scale up to 10.0
        numeric_scale = 10

        #We want the top 5 most occurring terms
        top_x_terms = 5

        #http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
        exclude = set(string.punctuation)
        
        #generate a list of stop words
        stop_words = [word for word in CountVectorizer(stop_words='english').get_stop_words()]
        stop_words.append('rt')
        stop_words.append('https')

        #Filtering section
        my_first_x_tweets = self.own_tweets[0:amount_of_tweets_to_gather]
        overall_list = []
        for sublist in my_first_x_tweets: 
            for item in sublist.text.split():
                if item not in stop_words:
                    transformed_item = item.lower().translate(string.punctuation)
                    #transformed_item = item.lower().join(ch for ch in transformed_item if ch not in exclude)
                    overall_list.append(transformed_item)# item.lower())
        
        total_count = len(overall_list)
        frequency_doc = Counter(overall_list)
        term_frequncy_list = {}

        for term in frequency_doc.keys():
            term_weight = (float(frequency_doc.get(term))/total_count) * numeric_scale
            term_frequncy_list[term] = term_weight

        self.termfreq_doc = term_frequncy_list
        #print("TFDOC")
        #print(self.termfreq_doc)
        top_terms = []
        most_common_raw = frequency_doc.most_common(top_x_terms) 
        for x in range(0, top_x_terms):
            top_terms.append(most_common_raw[x][0])
        
        print("Top 5 Terms")
        print(top_terms)#.__class__)

        remove_these_terms = []

        for term in self.termfreq_doc:
            if term not in top_terms:###############
                remove_these_terms.append(term)
        #print("*****")
        #print("*****")
        #print("Removals")
        #print(remove_these_terms)
        for removal in remove_these_terms:
            self.termfreq_doc.pop(removal, None)
        #print("*****")
        #print("*****")
        #print("Transformed Term Frequency Doc")
        #print(self.termfreq_doc)
        #print("*****")
        #print("*****")
        return weightings

    def get_tweet_term_weighting(self, tweet_text, term):
        weighting = 0
        #match_count = 0
        term_match_weighting = 0
        already_weighted_terms = []
        tweet_text_stripped = tweet_text.replace("#","").encode('utf-8')
        individual_tweet_words = tweet_text_stripped.split(" ")
        for word in individual_tweet_words:  
            if self.termfreq_doc.get(word.lower()) is not None:
                term_match_weighting += self.termfreq_doc.get(word.lower())
        
        #weighting = ((match_count + term_match_weighting)/len(tweet_text_stripped.split()))/ term_match_weighting#(len(self.termfreq_doc) + term_match_weighting)  
        weighting = term_match_weighting#((match_count + term_match_weighting)/len(tweet_text.split()))/(len(self.termfreq_doc) + term_match_weighting)  
        #print "weighting here"
        #print weighting
        #print "tweet here"
        #print tweet_text_stripped
        return weighting

    def generate(self, number_of_recommendations, followed_accounts, how_many_days_ago):
        list_of_owners_tweets = []
        unfollowed_tweets = []
        for tweet in self.own_tweets:
            list_of_owners_tweets.append(tweet.text.encode('utf-8'))

        self.vectorizer.fit_transform(list_of_owners_tweets)
        words = self.own_tweets #The users own tweets
        #print self.termfreq_doc
        tweet_list = self.followed_tweets #tweets from accounts that the user is following

        for term in self.termfreq_doc.keys():
            #print "Getting unfollowed tweets for term: "
            #print term
            unfollowed_tweet_list = self.get_unfollowed_tweets(term)
            
            for tweet in unfollowed_tweet_list:
                print("added:")
                print(tweet.text.encode('utf-8'))
                unfollowed_tweets.append(tweet)

        print("UNFOLLOWED HERE")
        for tweet in unfollowed_tweets:
            print(tweet.text.encode('utf-8'))

        for unfollowed_tweet in unfollowed_tweets:
            tweet_list.append(unfollowed_tweet)

        data_returned = sorted(tweet_list, key=self.count_bag, reverse=True)
        results = data_returned[0:number_of_recommendations]
       
        return results

    def count_bag(self, tweet):
        count = 0
        sanitised_tweet_text = tweet.text
        
        #bug
        #Somehow, the following tweet is being counted as six (should be three)
        #Tweet!
        #Guavate: tiny library bridging Guava and Java8 - Core Java Google Guava, Guavate, Java 8 https://t.co/kQnWkUy9V7
        #count!
        #6

        for word in sanitised_tweet_text.split():
            if word.lower() in self.termfreq_doc.keys():
                count += 1 
                count += self.get_tweet_term_weighting(sanitised_tweet_text, self.termfreq_doc.get(word))

        return count