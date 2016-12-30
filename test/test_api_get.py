import time
import random
import json
import requests
from multiprocessing import Pool

def test(cases):
    t1 = time.time()
    tot = 0
    feed_id_limit = 500
    user_id_limit = 100000
    for i in range(cases):
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
                "http://127.0.0.1:5000/feed/%s" 
                % feed_id,
            params=params)
        res = json.loads(r.content.decode("utf-8"))
        print(params, res['data'])
        #print(res['data'])
        # tot += 1
        # if len(res['data']) > 0 and tot < cases:
        #     list_times = random.randrange(0, res['total'])
        #     for j in range(list_times):
        #         params['max_id'] = res['max_id']
        #         params['is_friend'] = res['is_friend']
        #         r = requests.get(
        #             "http://127.0.0.1:5000/feed/%s" 
        #             % feed_id,
        #         params=params)
        #         res = json.loads(r.content.decode("utf-8"))
        #         #print(res['data'])
        #         tot += 1
        #         if tot >= cases or len(res['data']) > 0:
        #             break
        # if tot >= cases:
        #     break
    t2 = time.time()
    print('finish cost', t2-t1)

if __name__ == '__main__':
    test(1)