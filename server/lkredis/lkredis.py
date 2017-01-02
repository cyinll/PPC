import redis
import threading
import json
from lkmysql import lkmysql 

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)

def update_feed_friend_like(feed_id, user_id):
    friend_list = r.get("friends" + str(user_id))
    if friend_list is None:
        friend_list = lkmysql.query_friend_list(
            user_id
        )
        r.set("friends_%s" % user_id, friend_list)
    for friend in friend_list:
        key = "feed_friend_like_%s_%s" % (feed_id, friend)
        res = r.get(key)
        if res is not None:
            res = json.loads(res.decode("utf8"))
            res.append(friend)
            r.set(key, res)
            
def update_feed_stat(feed_id, user_id):    
    key = "stat_%s" % feed_id
    if r.exists(key):
        r.incr(key)
    update_feed_friend_like(feed_id, user_id)

def set_feed_stat(feed_id, res):
    key = "stat_%s" % feed_id
    r.set(key, res)

def set_feed_friend_like(feed_id, user_id, res):
    key = "feed_friend_like_%s_%s" %(feed_id, user_id)
    r.set(key, res)

def set_feed_non_friend_like(feed_id, user_id, max_id, res):
    key = "feed_non_friend_like_%s_%s_%s" %(feed_id, user_id, max_id)
    r.set(key, res)

def query_feed_stat(feed_id):
    key = "stat_%s" % feed_id
    res = r.get(key)
    if res is not None:
        return json.loads(res.decode("utf8"))
    res = lkmysql.query_feed_stat(feed_id)
    set_feed_stat(feed_id, res)
    return res

def query_friend_feed_like(feed_id, user_id):
    key = "feed_friend_like_%s_%s" %(feed_id, user_id)
    res = r.get(key)
    if res is not None:
        data = json.loads(res.decode("utf8"))
        return data
    data = lkmysql.query_friend_feed_like(
                        feed_id,
                        user_id
                    )
    set_feed_friend_like(feed_id, user_id, data)
    return data, 0

def query_non_friend_feed_like(feed_id, user_id, max_id):
    key = "feed_non_friend_like_%s_%s_%s" %(feed_id, user_id, max_id)
    res = r.get(key)
    if res is not None:
        data = json.loads(res.decode("utf8"))
        return data[0], data[1]
    data, new_max_id = lkmysql.query_friend_feed_like(
                        feed_id,
                        user_id,
                        max_id
                    )
    set_feed_non_friend_like(feed_id, user_id, max_id, (data, new_max_id))
    return data, max_id