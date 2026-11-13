import redis
from ..config.settings import REDIS_URL
QUEUE="fault-evidence:runs"
def client():return redis.Redis.from_url(REDIS_URL,decode_responses=True)
def enqueue(ident):client().rpush(QUEUE,ident)
