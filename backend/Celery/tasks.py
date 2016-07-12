from celery import Celery
import tweepy
from datetime import timedelta
import pandas as pd
import rethinkdb as r
import time


app = Celery('tasks', backend='amqp://guest@localhost//', broker='amqp://rabbitmq:marcgoestothegymagain@localhost:5672//')

#config celery, the task 'add' will be executed every 60 seconds
app.conf.update(
               CELERYBEAT_SCHEDULE = {
               "add": {
               "task": "tasks.add",
               "schedule": timedelta(seconds=60),
               }, },
               )


@app.task
def add():
    
    #read tokens of all user's in the database
    tokens = read_tokens()
    
    #iteratively fetch tweets of each user
    #all tasks are async tasks, so will not affetc each other
    for item in tokens:
        get_tweet.delay(item)

#get tweets
@app.task(bind=True)
def get_tweet(self, token):
    
    #authentication
    auth = tweepy.OAuthHandler(consumer_key=token['consumer_key'], consumer_secret=token['consumer_secret'])
    auth.set_access_token(token['access_token'], token['access_secret'])

    api = tweepy.API(auth)
    
    #connect to database
    r.connect(host = 'ec2-52-51-162-183.eu-west-1.compute.amazonaws.com', port = 28015, db='lovelace', password = "marcgoestothegym").repl()
    
    #fetch user's home timeline and insert it into database
    #here is an error handling, if the rate limit exceed, the task will be retried after 5 seconds
    try:
        tweets = [tweet._json for tweet in api.home_timeline(count=200)]
        r.table('tweets').insert(tweets).run()
        limit = api.rate_limit_status()
        return limit['resources']['statuses']['/statuses/home_timeline']
    except tweepy.RateLimitError as exc:
        raise self.retry(exc=exc,countdown=5,max_retries=10)

#method to read all tokens of the users from database
def read_tokens():
    
    r.connect(host = 'ec2-52-51-162-183.eu-west-1.compute.amazonaws.com', port = 28015, db='lovelace', password = "marcgoestothegym").repl()
    tokens=r.db('lovelace').table('users').run()
    return tokens