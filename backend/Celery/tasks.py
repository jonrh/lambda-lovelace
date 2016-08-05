from celery import Celery
from celery.signals import task_failure
from datetime import timedelta
import rethinkdb as r
import tweepy
import rollbar

# =============================================================================
#                                  ROLLBAR
# =============================================================================
# Setup for Rollbar, our error logging service. To view them see
# https://rollbar.com/lambda-lovelace/Lambda-Lovelace-Backend/ Team members
# should have an account. This code is worked from the following example:
# https://github.com/rollbar/rollbar-celery-example
rollbar.init(access_token="9a41d7e8fdbb49cead0cae434765a927", environment="celery-worker")


def celery_base_data_hook(request, data):
    data['framework'] = 'celery'

rollbar.BASE_DATA_HOOK = celery_base_data_hook
# =============================================================================


# Terminal command to run this task file
# celery -A tasks worker -B -c 8 --loglevel=info

app = Celery('tasks', broker='redis://celery-redis:6379/0')

# config celery, the task 'add' will be executed every 60 seconds
app.conf.update(
    CELERYBEAT_SCHEDULE={
        "add": {
            "task": "tasks.add",
            "schedule": timedelta(seconds=65),
        },
    },
)


@task_failure.connect
def handle_task_failure(**kw):
    """Send all error and exception to Rollbar"""
    rollbar.report_exc_info(extra_data=kw)


@app.task
def add():
    # read tokens of all user's in the database
    tokens = read_tokens()
    
    # iteratively fetch tweets of each user
    # all tasks are async tasks, so will not affect each other
    for item in tokens:
        get_tweet.delay(item)


@app.task(bind=True)
def get_tweet(self, token):
    """Get tweets"""
    # connect to database
    r.connect(
        host='ec2-52-51-162-183.eu-west-1.compute.amazonaws.com',
        port=28015, db='lovelace', password="marcgoestothegym"
    ).repl()
    
    last_login = token['last_login']
    print(last_login)
    now = r.now().to_epoch_time().run()
    print(now - last_login)
    screen_name = token['screen_name']

    # check the time interval between the time when token is inserted and the time when next celery task executes if the
    # interval is less than 64 seconds, we wait for another 64 seconds,this is to avoid sending two requests to the
    # Twitter API in one minute we can only send one request each 64 seconds.
    if (now - last_login) >= 64:
        # authentication
        auth = tweepy.OAuthHandler(consumer_key=token['consumer_key'], consumer_secret=token['consumer_secret'])
        auth.set_access_token(token['access_token'], token['access_secret'])
        
        api = tweepy.API(auth)
        
        # fetch user's home timeline and insert it into database
        # here is an error handling, if the rate limit exceed, the task will be retried after 5 seconds
        try:
            if (token['fetch_status'] is True) or ((token['fetch_status'] is False) and (r.now().to_epoch_time().run() - token['last_logout'] <= 900)):
                # since_id is the id of the newest tweet of user's home timeline in the database
                since_id = r.db('lovelace').table('tweets').filter({'screen_name': screen_name}).max('tweet_id').run()
                # only fetch the tweets whose ids are greater than the since_id, to avoid fetching duplicate tweets
                new_tweets = [tweet._json for tweet in api.home_timeline(count=200, since_id=since_id['tweet_id'])]
                print(len(new_tweets))
                # insert each tweet into database
                for item in new_tweets:
                    r.db('lovelace').table('tweets').insert({
                        'screen_name': screen_name,
                        'tweet_id': item['id_str'],
                        'tweet': item
                    }).run()
                # check rate limit remaining
                limit = api.rate_limit_status()
                return limit['resources']['statuses']['/statuses/home_timeline']
        except tweepy.RateLimitError as exc:
            raise self.retry(exc=exc, countdown=5, max_retries=10)


# method to read all tokens of the users from database
def read_tokens():
    r.connect(
        host='ec2-52-51-162-183.eu-west-1.compute.amazonaws.com',
        port=28015, db='lovelace', password="marcgoestothegym"
    ).repl()

    tokens = r.db('lovelace').table('user_tokens').run()

    return tokens
