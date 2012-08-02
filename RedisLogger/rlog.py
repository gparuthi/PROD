'''
Created on Aug 1, 2012

@author: gparuthi
'''
import redis
import datetime

def RedisListener(ps,rc):
    for item in ps.listen():
        finalActions={}
        if item['type'] == 'message':
            now = datetime.datetime.now()
            print now.strftime("%Y-%m-%d %H:%M") + '::::' + item['data']

if __name__ == '__main__':
    rc = redis.Redis(host='dhcp3-173.si.umich.edu', port=6379, db=0)
    ps = rc.pubsub()
    ps.subscribe(['log'])
    print('Listening...')
    RedisListener(ps,rc)