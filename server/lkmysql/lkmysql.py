import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "mysql+pymysql://root:lvliang@localhost:3306/pcc?charset=utf8",
    encoding="utf-8",
    echo=False
)

DB_Session = sessionmaker(bind=engine)
session = DB_Session()

def update_feed_stat(feed_id):
    session.execute(
        "UPDATE feed_stat SET total=total+1 \
        WHERE feed_id=%s" % feed_id
    )
    session.commit()

def insert_feed_like(feed_id, user_id):
    now_time = datetime.datetime.now()
    now_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
    session.execute(
        "INSERT INTO feed_like\
        (feed_id, like_uid, ctime) VALUES \
        (%s, %s, '%s')"
        % (feed_id, user_id, now_time)
    )

def query_feed_stat(feed_id):
    total = session.execute(
        "SELECT total FROM feed_stat \
        WHERE feed_id=%s" % feed_id
    ).fetchone()[0]
    return total

def query_friend_list_sql(user_id):
    return "SELECT to_uid FROM friends WHERE from_uid=%s" % user_id

def query_friend_list(user_id):
    res = session.execute(query_friend_list_sql(user_id))
    return res.fetchall()

def query_friend_feed_like(feed_id, user_id, is_friend, page_count=1000):
    res = session.execute(
        "SELECT like_uid FROM feed_like \
        WHERE feed_id = %s AND \
        like_uid IN (%s) \
        order by id limit %s"
        % (
            feed_id,
            query_friend_list_sql(user_id),
            page_count
        )
    )
    return res.fetchall()

def query_non_friend_feed_like(feed_id, user_id, is_friend, max_id, page_count=100):
    res = session.execute(
        "SELECT id, like_uid FROM feed_like \
        WHERE feed_id = %s AND \
        like_uid NOT IN (%s) AND \
        id > %s \
        order by id limit %s"
        % (
            feed_id,
            query_friend_list_sql(user_id),
            max_id
            page_count
        )
    ).fetchall()
    user_list = []
    new_max_id = 0
    if len(res) > 0:
        user_list = [x[1] for x in res]
        new_max_id = res[-1][0]
    return user_list, new_max_id
    
