import time
import random
import json
import requests
import argparse
import threading

class Worker(threading.Thread):
    def __init__(self, cases):
        threading.Thread.__init__(self)
        self.cases = cases
        self.start()

    def run(self):
        tot = 0
        feed_id_limit = 500
        user_id_limit = 100000
        for i in range(self.cases):
            feed_id = random.randrange(1, feed_id_limit+1)
            user_id = random.randrange(1, user_id_limit+1)
            is_friend = 1
            max_id = 0
            params = dict(
                user_id=user_id,
                is_friend=is_friend,
                max_id=max_id
            )
            r = requests.get(
                    "http://127.0.0.1:5000/v1/feed/%s/likes" 
                    % feed_id,
                params=params)
            res = json.loads(r.content.decode("utf-8"))
            tot += 1
            if len(res['data']) > 0 and tot < self.cases:
                list_times = random.randrange(0, res['total'])
                for j in range(list_times):
                    params['max_id'] = res['max_id']
                    params['is_friend'] = res['is_friend']
                    r = requests.get(
                        "http://127.0.0.1:5000/v1/feed/%s/likes" 
                        % feed_id,
                    params=params)
                    res = json.loads(r.content.decode("utf-8"))
                    tot += 1
                    if tot >= self.cases or len(res['data']) > 0:
                        break
            if tot >= self.cases:
                break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="test_api")
    parser.add_argument("-n", dest="num", type=int, default=1,
                    help="thread number")
    parser.add_argument("-c", dest="cases", type=int, default=1,
                    help="test cases")
    args = parser.parse_args()
    workers = []
    t1 = time.time()
    for i in range(args.num):
        workers.append(Worker(args.cases))
    for worker in workers:
        worker.join()
    t2 = time.time()
    print("tot cost", t2-t1)