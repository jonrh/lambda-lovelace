from celery import Celery
from celery.signals import task_failure
from celery.utils.log import get_task_logger

from datetime import timedelta
import rethinkdb as r
import tweepy
import rollbar

"""What tasks.py does is continuously fetching the user's home timeline
(Tweets and retweets posted by the accounts he/she follows).

The task "add" is configured to be executed every 65 seconds. This is to avoid
making too many requests at a time and hitting the twitter rate limit.

When task "add" is executed, firstly the method "read_tokens()" will be called
which will read the tokens of all the users who have logged into our app from
the database, then return a list of user tokens and other user information.

User information includes:

"access_secret", "access_token", "consumer_key", "consumer_secret" - user tokens,
"fetch_status" - 'True' or 'False', if 'True', Celery will fetch tweets for the users
"last_login" - last time user logged in
"last_logout" - last time user logged out or 'None'
"screen_name" - screen name of the user



Then in task "add", it will iteratively fetch tweets of each user by calling
the method "get_tweet.delay()". ".delay()" means the methods are executed
asynchronously, so they will not affect each other. A method will NOT wait for
the last method finish executing.

We set a mechanism that, after 15 minutes since the user has logged out, celery will
stop fetching tweets for the user. So in the method "get_tweet()", it will check if
the user has NOT logged out or if the user has logged out but still WITHIN 15 minutes.
If it is true, then in "get_tweet()" it will send a request to Twitter API and get new
tweets for the user.
"""

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

# logger for logging error
logger = get_task_logger(__name__)

# Create an Celery instance, here we use redis as a broker
app = Celery('tasks', broker='redis://celery-redis:6379/0')


# config celery, the task 'add' will be executed every 65 seconds
app.conf.update(
    CELERYBEAT_SCHEDULE={
        "add": {
            "task": "tasks.add",
            "schedule": timedelta(seconds=65),
        },
    },
)


@app.task
def add():
    """
    Get user tokens from database, and then use the
    user tokens to fetch tweets for the users.

    Args:
        No arguments

    Returns:
        No returns
    """

    # read tokens of all user's in the database
    tokens = read_tokens()

    # iteratively fetch tweets of each user
    # all tasks are async tasks, so will not affect each other
    for item in tokens:
        get_tweet.delay(item)


@app.task(bind=True)
def get_tweet(self, token):
    """
    Get tweets of the user

    Args:
        token: user token and user information got from database

    Returns:
        Rate limit remaining
    """

    # connect to database
    r.connect(
        host='ec2-52-51-162-183.eu-west-1.compute.amazonaws.com',
        port=28015, db='lovelace', password="marcgoestothegym"
    ).repl()

    # get last login time
    last_login = token['last_login']

    # get current time
    now = r.now().to_epoch_time().run()

    # get user's screen name
    screen_name = token['screen_name']

    # When a user logs in our app for the first time, Flask server will insert the
    # user token and user information into database.
    # Meanwhile, as there are no tweets of the user in the database yet, Flask server
    # will get some tweets directly from twitter API and save them into database for
    # the recommender system to use. This will consume one request.
    # So here we check the time interval between the time when the token is inserted
    # into database and the time when next celery task executes.
    # If the interval is less than 65 seconds, we wait for another 65 seconds,
    # this is to avoid sending two requests to the Twitter API within 65 seconds.
    # We can only send one request each 65 seconds.
    if (now - last_login) >= 65:

        # authentication
        auth = tweepy.OAuthHandler(consumer_key=token['consumer_key'], consumer_secret=token['consumer_secret'])
        auth.set_access_token(token['access_token'], token['access_secret'])
        api = tweepy.API(auth)

        # fetch user's home timeline and insert it into database
        try:
            # if user has not logged out or has logged out but within 15 minutes (900 seconds)
            if (token['fetch_status'] is True) or ((token['fetch_status'] is False) and (r.now().to_epoch_time().run() - token['last_logout'] <= 900)):

                # since_id is the id of the newest tweet of user's home timeline in the database
                since_id = r.db('lovelace').table('tweets').filter({'screen_name': screen_name}).max('tweet_id').run()

                # only fetch the tweets whose ids are greater than the since_id, to avoid fetching duplicate tweets
                new_tweets = [tweet._json for tweet in api.home_timeline(count=200, since_id=since_id['tweet_id'])]

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

        # error handling
        except tweepy.RateLimitError as exc:
            logger.warning("Rate limit exceeded. Skipped.")
        except r.ReqlNonExistenceError as e:
            logger.exception("Most likely couldn't find a specific user in RethinkDB")


def read_tokens():
    """
    method to read all tokens of the users from database

    Args:
         No arguments

    Returns:
        A list of user tokens
    """
    r.connect(
        host='ec2-52-51-162-183.eu-west-1.compute.amazonaws.com',
        port=28015, db='lovelace', password="marcgoestothegym"
    ).repl()

    tokens = r.db('lovelace').table('user_tokens').run()

    return tokens


@task_failure.connect
def handle_task_failure(**kw):
    """Send all error and exception to Rollbar"""
    rollbar.report_exc_info(extra_data=kw)
