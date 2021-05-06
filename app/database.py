from redis import Redis
from rq import Queue

from app.settings import settings

redis = Redis.from_url(settings.REDIS_URL)
queue = Queue(connection=redis)


def get_queue() -> Queue:
    return queue
