from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "mysql+pymysql://root:lvliang@localhost:3306/pcc?charset=utf8",
    encoding="utf-8",
    echo=True
)

DB_Session = sessionmaker(bind=engine)
session = DB_Session()
session.autocommit = True

def update_feed_stat(feed_id, is_friend, user_id):
    if is_friend != 0:
        session.execute(
            "UPDATE feed_stat SET total=total+1, \
            max_friend_uid=user_id \
            WHERE feed_id=%s" % feed_id
        )
    else:
        session.execute(
            "UPDATE feed_stat SET total=total+1, \
            WHERE feed_id=%s" % feed_id
        )

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
    (total, max_friend_uid) = sesion.execute(
        "SELECT total, max_friend_uid FROM feed_stat \
        WHERE feed_id=%s" % feed_id
    ).fetchone()
    return dict(total=total, max_friend_uid=max_friend_uid)
