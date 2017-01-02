# import lkredis
import json
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
        # lkredis.update_feed_stat(
        #     feed_id,
        #     user_id
        # )
        lkmysql.update_feed_stat(feed_id)
        lkmysql.add_feed_like(feed_id, user_id)
        return json.dumps({"status": "Success"})
    except Exception as e:
        print(e)
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
        total = lkmysql.query_feed_stat(feed_id)
        if total > 0:
            data, new_max_id = lkmysql.query_feed_like(
                feed_id,
                user_id,
                is_friend,
                max_id
            )
            #get data from non-friend
            if len(data) < 50 and is_friend == 1:
                d, new_max_id = lkmysql.query_feed_like(
                    feed_id,
                    user_id,
                    0,
                    0,
                )
                new_is_friend = 0
                data += d

        res['total'] = total
        res['data'] = data
        res['is_friend'] = new_is_friend
        res['max_id'] = new_max_id
        return json.dumps(res)
    except Exception as e:
        print(e)
        return json.dumps({"status": "Failed"})


if __name__ == '__main__':
    app.run()
