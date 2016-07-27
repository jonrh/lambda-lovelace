FROM celery
COPY tasks.py tasks.py
CMD celery -A tasks worker -B -c 8 --loglevel=info