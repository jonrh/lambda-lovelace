class Tweet: 
     
    def __init__(self, id, created_at, id_str, text, truncated, entities, extended_entities, source, in_reply_to_status_id, in_reply_to_status_id_str, in_reply_to_user_id, in_reply_to_user_id_str, in_reply_to_screen_name, user, geo, coordinates, place, contributors, is_quote_status, retweet_count, favorite_count, favorited, retweeted, possibly_sensitive, possibly_sensitive_appealable, lang): 
        self.id = id
        self.created_at = created_at
        self.id_str = id_str
        self.text = text
        self.truncated = truncated
        self.entities = entities
        self.extended_entities = extended_entities
        self.source = source
        self.in_reply_to_status_id = in_reply_to_status_id
        self.in_reply_to_status_id_str = in_reply_to_status_id_str
        self.in_reply_to_user_id = in_reply_to_user_id
        self.in_reply_to_user_id_str = in_reply_to_user_id_str
        self.in_reply_to_screen_name = in_reply_to_screen_name
        self.user = user
        self.geo = geo
        self.coordinates = coordinates
        self.place = place
        self.contributors = contributors
        self.is_quote_status = is_quote_status
        self.retweet_count = retweet_count
        self.favorite_count = favorite_count
        self.favorited = favorited
        self.retweeted = retweeted
        self.possibly_sensitive = possibly_sensitive
        self.possibly_sensitive_appealable = possibly_sensitive_appealable
        self.lang = lang

    def get_text(self): 
        return self.text

    def get_id(self): 
        return self.id

    def get_user(self): 
        return self.user

    def all_tweets(self): 
        return self.tweets