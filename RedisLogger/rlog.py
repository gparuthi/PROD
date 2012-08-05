'''
Created on Aug 1, 2012

@author: gparuthi
'''
import redis
import datetime

REDIS_SERVER_URL = 'dhcp2-236.si.umich.edu'

def RedisListener(ps,rc):
    for item in ps.listen():
        finalActions={}
        if item['type'] == 'message':
            now = datetime.datetime.now()
            print now.strftime("%Y-%m-%d %H:%M") + '::::' + item['data']

if __name__ == '__main__':
    rc = redis.Redis(host=REDIS_SERVER_URL, port=6379, db=0)
    ps = rc.pubsub()
    ps.subscribe(['log'])
    print('Listening...')
    RedisListener(ps,rc)