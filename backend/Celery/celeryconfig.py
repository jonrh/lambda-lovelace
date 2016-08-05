from kombu import Queue
from kombu import Exchange
from datetime import timedelta

CELERY_QUEUES = (
                 Queue('liked_queue',Exchange('liked'), routing_key='liked'),
                 Queue('user_queue',Exchange('user'), routing_key='user'),
                 )

CELERY_ROUTES = {
    
    'tasks_liked.liked_add': {
        'queue': 'liked_queue',
        'routing_key': 'liked',
    },
    'tasks_user.user_add': {
        'queue': 'user_queue',
        'routing_key': 'user',
    },

    'tasks_liked.get_liked_tweet': {
        'queue': 'liked_queue',
        'routing_key': 'liked',
    },
    'tasks_user.get_user_tweet': {
        'queue': 'user_queue',
        'routing_key': 'user',
    },
}