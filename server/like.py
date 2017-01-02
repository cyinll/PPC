# import lkredis
import json
import traceback  
from lkredis import lkredis
from lkmysql import lkmysql
from flask import Flask
from flask import request


app = Flask(__name__)


@app.route("/")
def index():
    return "OK"

@app.route("/v1/feed", methods=["POST"])
def feed_like():
    try:
        res = dict()
        feed_id = int(request.form['feed_id'])
        user_id = int(request.form['user_id'])
        lkredis.update_feed_stat(
            feed_id,
            user_id
        )
        lkmysql.update_feed_stat(feed_id)
        lkmysql.insert_feed_like(feed_id, user_id)
        return json.dumps({"status": "Success"})
    except Exception as e:
        traceback.print_exc()
        return json.dumps({"status": "Failed"})


@app.route("/v1/feed/<feed_id>/likes", methods=["GET"])
def get_feed_like_list(feed_id):
    try:
        res = dict()
        res['status'] = "Success"
        user_id = int(request.args.get('user_id'))
        max_id = int(request.args.get('max_id'))
        is_friend = int(request.args.get('is_friend'))
        data = []
        new_max_id = 0
        new_is_friend = is_friend
        total = lkredis.query_feed_stat(feed_id)
        if total > 0:
            if is_friend == 1:
                data, new_max_id = lkredis.query_friend_feed_like(
                    feed_id,
                    user_id,
                    is_friend
                )
                if len(data) == 0:
                    is_friend = 0
            #get data from non-friend
            if len(data) == 0:
                data, new_max_id = lkredis.query_non_friend_feed_like(
                    feed_id,
                    user_id,
                    0,
                    0,
                )

        res['total'] = total
        res['data'] = data
        res['max_id'] = new_max_id
        return json.dumps(res)
    except Exception as e:
        traceback.print_exc()
        return json.dumps({"status": "Failed"})


if __name__ == '__main__':
    app.run()
