import time
import pymysql
from datetime import date

conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="lvliang",
    charset="utf8",
    db="pcc"
)
conn.autocommit(True)


def insert_friends_data(tot, friends):
    # tot: tot user
    # friends: num users all are friends
    with conn.cursor() as cur:
        sql = "INSERT INTO friends (from_uid, to_uid, ctime) VALUES "
        for i in range(1, tot, friends):
            query_list = []
            for j in range(friends):
                for k in range(friends):
                    if j != k:
                        query_list.append(
                            "(%s, %s, '%s')"
                            % (i + j, j + k, date(2016, 12, 25))
                        )
            cur.execute(sql + ",".join(query_list))
            if i % (tot / 100) == 1:
                print("finish", i / 1000)


def init_feed_stat(feeds):
    t1 = time.time()
    sql = "truncate table feed_stat"
    with conn.cursor() as cur:
        cur.execute(sql)
    with conn.cursor() as cur:
        sql = "INSERT INTO feed_stat (feed_id, total, max_friend_uid) VALUES "
        query_list = []
        for i in range(1, feeds+1):
            query_list.append("(%s, 0, 0)" % i)
            if i % 1000 == 0:
                cur.execute(sql + ",".join(query_list))
                query_list = []
        if len(query_list) > 0:
            cur.execute(sql + ",".join(query_list))
    t2 = time.time()
    print("init feed stat finish, cost", t2-t1)
