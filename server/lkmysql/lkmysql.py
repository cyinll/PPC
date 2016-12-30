from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "mysql+pymysql://root:lvliang@localhost:3306/pcc?charset=utf8",
    encoding="utf-8",
    echo=False
)

DB_Session = sessionmaker(bind=engine)
session = DB_Session()

def update_feed_stat(feed_id, is_friend, user_id):
    session.execute(
        "UPDATE feed_stat SET total=total+1, \
        WHERE feed_id=%s" % feed_id
    )
    session.commit()

def add_feed_like(feed_id, is_friend, user_id):
    now_time = datetime.datetime.now()
    now_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
    session.execute(
        "INSERT INTO feed_like\
        (feed_id, is_friend, like_uid, ctime) VALUES \
        (%s, %s, %s, '%s')"
        % (feed_id, is_friend, user_id, now_time)
    )

def query_feed_stat(feed_id):
    total = session.execute(
        "SELECT total FROM feed_stat \
        WHERE feed_id=%s" % feed_id
    ).fetchone()[0]
    return total

def query_friend_list_sql(user_id):
    return "SELECT to_uid from friends where from_uid=%s" % user_id

def query_feed_like(feed_id, user_id, is_friend, max_id, page_count=50):
    in_str = "in"
    if not is_friend:
        in_str = "not in"
    res = session.execute(
        "SELECT id, like_uid FROM feed_like \
        where feed_id = %s and \
        like_uid %s (%s) and \
        id > %s \
        order by id limit %s"
        % (
            feed_id,
            in_str,
            query_friend_list_sql(user_id),
            max_id,
            page_count
        )
    ).fetchall()
    user_list = []
    new_max_id = 0
    new_is_friend = is_friend
    if len(res) > 0:
        user_list = [x[1] for x in res]
        new_max_id = res[-1][0]
    return user_list, new_max_id
    
