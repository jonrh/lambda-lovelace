from celery import Celery
from celery.signals import task_failure
from celery.utils.log import get_task_logger
from datetime import timedelta
import rethinkdb as r
import tweepy
import rollbar

"""What tasks_user.py does is continuously fetching the user's own timeline
(Tweets and retweets posted by the user).

The task "user_add" is configured to be executed every 10 seconds because for
user timeline, it is 180 requests/min.
This is to avoid making too many requests at a time and hitting the twitter
rate limit.

When task "user_add" is executed, firstly the method "read_tokens()" will be called
which will read the tokens of all the users who have logged into our app from
the database, then return a list of user tokens and other user information.

User information includes:

"access_secret", "access_token", "consumer_key", "consumer_secret" - user tokens,
"fetch_status" - 'True' or 'False', if 'True', Celery will fetch tweets for the users
"last_login" - last time user logged in
"last_logout" - last time user logged out or 'None'
"screen_name" - screen name of the user

Then in task "user_add", it will iteratively fetch tweets of each user by calling
the method "get_user_tweet.delay()". ".delay()" means the methods are executed
asynchronously, so they will not affect each other. A method will NOT wait for
the last method finish executing.

We set a mechanism that, after 15 minutes since the user has logged out, celery will
stop fetching tweets for the user. So in the method "get_user_tweet()", it will check if
the user has NOT logged out or if the user has logged out but still WITHIN 15 minutes.
If it is true, then in "get__user_tweet()" it will send a request to Twitter API and
get new tweets for the user.
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

# config celery from a file called celeryconfig.py
app.config_from_object("celeryconfig")


# config celery, the task 'user_add' will be executed every 10 seconds
app.conf.update(
    CELERYBEAT_SCHEDULE={
        "user_add": {
            "task": "tasks_user.user_add",
            "schedule": timedelta(seconds=10),
        },
    },
)


@app.task
def user_add():
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
        get_user_tweet.delay(item)


@app.task(bind=True)
def get_user_tweet(self, token):
    """
    Get tweets of the user's own timeline

    Args:
        token: user token and user information got from database

    Returns:
        "user_timeline"
    """

    # connect to database
    r.connect(
        host='ec2-52-51-162-183.eu-west-1.compute.amazonaws.com',
        port=28015, db='lovelace', password="marcgoestothegym"
    ).repl()

    # authentication
    auth = tweepy.OAuthHandler(consumer_key=token['consumer_key'], consumer_secret=token['consumer_secret'])
    auth.set_access_token(token['access_token'], token['access_secret'])
    api = tweepy.API(auth)

    # get user's screen name
    screen_name = token['screen_name']

    new_user_tweets = []
    # fetch user's own timeline and insert it into database
    try:
        # if user has not logged out or has logged out but within 15 minutes (900 seconds)
        if (token['fetch_status'] is True) or ((token['fetch_status'] is False) and (r.now().to_epoch_time().run() - token['last_logout'] <= 900)):
            if screen_name != u"NoUserNameFound":
                # since_id is the id of the newest tweet of user's own timeline in the database
                since_id = r.db('lovelace').table('like_user_timeline').filter({'screen_name': screen_name, 'type': 'user'}).max('tweet_id').run()

                # only fetch the tweets whose ids are greater than the since_id, to avoid fetching duplicate tweets
                new_user_tweets = [tweet._json for tweet in api.user_timeline(count=200, since_id=since_id['tweet_id'])]

                # insert each tweet into database
                for item in new_user_tweets:
                    r.db('lovelace').table('like_user_timeline').insert({
                        'screen_name': screen_name,
                        'tweet_id': item['id_str'],
                        'type': 'user',
                        'tweet': item
                    }).run()

                return "user_timeline"

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