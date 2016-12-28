# import lkredis
import json
from lkmysql import lkmysql
from flask import Flask
from flask import request


app = Flask(__name__)


@app.route("/")
def index():
    return "OK"

@app.route("/feed", methods=["POST"])
def feed_like():
    try:
        res = dict()
        action = request.form['action']
        feed_id = request.form['feed_id']
        user_id = request.form['user_id']
        # lkredis.update_feed_stat(
        #     feed_id,
        #     is_friend,
        #     user_id
        # )
        mysql.update_feed_stat(feed_id)
        mysql.add_feed_like(feed_id, user_id)
        return json.dumps({"status": "Success"})
    except Exception as e:
        return json.dumps({"status": "Failed"})


@app.route("/feed/<feedid>", methods=["GET"])
def get_feed_like_list(feedid):
    try:
        res = dict()
        res['status'] = "Success"
        res['feed_id'] = feedid
        res['max_id'] = request.args.get('max_id')
        res['is_friend'] = request.args.get('is_friend')
        res['now_user_stat'] = request.args.get('now_user_stat')
        data = []
        stat_data = lkmysql.query_feed_stat(feed_id)
        if stat['total'] > 0:
            data = lkmysql.query_feed_like(
                max_id,
                is_friend,
                now_user_stat
            )
        res['total'] = total
        res['data'] = data
        return json.dumps(res)
    except Exception as e:
        return json.dumps({"status": "Failed"})


if __name__ == '__main__':
    app.run()
