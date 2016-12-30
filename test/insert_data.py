import time
import pymysql
import random
import datetime
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    "mysql+pymysql://root:lvliang@localhost:3306/pcc?charset=utf8",
    encoding="utf-8",
    echo=False
)

DB_Session = sessionmaker(bind=engine)
session = DB_Session()

def insert_friends_data(tot, friends):
    # tot: tot user
    # friends: num users all are friends
    t1 = time.time()
    if tot % friends != 0:
        print("error")
        return
    sql = "INSERT INTO friends (from_uid, to_uid, ctime) VALUES "
    for i in range(1, tot, friends):
        query_list = []
        for j in range(friends):
            for k in range(friends):
                now_time = datetime.datetime.now()
                now_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
                if j != k:
                    query_list.append(
                        "(%s, %s, '%s')"
                        % (i + j, i + k, now_time)
                    )
        session.execute(sql + ",".join(query_list))
        session.commit()
        if i % int(tot / 100) == 1:
            print('finish', (i-1) / int(tot/100) + 1)
    t2 = time.time()
    print("finish cost", t2-t1)



def init_feed_stat(feeds, users=100000):
    t1 = time.time()
    sql = "truncate table feed_stat"
    session.execute(sql)
    session.commit()
    sql = "INSERT INTO feed_stat (feed_id, total) VALUES "
    query_list = []
    for i in range(1, feeds+1):
        query_list.append("(%s, 0)" % i)
        if i % 1000 == 0:
            session.execute(sql + ",".join(query_list))
            session.commit()
            query_list = []
    if len(query_list) > 0:
        session.execute(sql + ",".join(query_list))
        session.commit()
    t2 = time.time()
    print("init feed stat finish, cost", t2-t1)


def insert_feed_like(limit, feeds=100000, users=100000):
    # two table feed_like, feed_friend_like
    t1 = time.time()
    tot = 0
    query_list = []
    sql = "INSERT INTO feed_like (feed_id, like_uid, ctime) VALUES "
        
    for feed_id in range(1, feeds+1):
        feed_likes = random.randrange(100000) + 1
        #update feed_stat
        session.execute(
            "UPDATE feed_stat SET total=total+%s \
            WHERE feed_id=%s" 
            % (feed_likes, feed_id)
        )
        session.commit()
        u = 0
        for j in range(feed_likes):
            now_time = datetime.datetime.now()
            now_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
            v = random.randrange(u+1, users+1)
            if v + (feed_likes - j) - 1 > users:
                v = u + 1
            u = v
            query_list.append(
                "(%s, %s, '%s')"
                %(feed_id, u, now_time)
            )            
            tot += 1
            if tot % 1000 == 0:
                session.execute(sql+",".join(query_list))
                session.commit()
                query_list = []
            if limit >= 100 and tot % int(limit / 100) == 0:
                print("finish", int(tot * 100 / limit))
            if tot >= limit:
                break
        if tot >= limit:
            break
    #last commit 
    if len(query_list) > 0:
        session.execute(sql+",".join(query_list))
        session.commit()
    t2 = time.time()
    print("finish cost", t2-t1)
    # while(True):
    #     pass
