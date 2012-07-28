import redis
from json import dumps

rc = redis.Redis(host='dhcp3-173.si.umich.edu', port=6379, db=0)

ps = rc.pubsub()
ps.subscribe(['renderer','All'])

for item in ps.listen():
    if item['type'] == 'message':
        print item['channel']
        print item['data']