import redis
from lkmysql import lkmysql 

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
redis_client = redis.Redis(connection_pool=pool)

def update_feed_stat():
