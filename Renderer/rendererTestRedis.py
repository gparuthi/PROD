import redis
from json import dumps

def redis_renderer():
    rc = redis.Redis(host='dhcp3-173.si.umich.edu', port=6379, db=0)
    
    ps = rc.pubsub()
    ps.subscribe(['renderer','All'])
    
    for item in ps.listen():
        if item['type'] == 'message':
            print item['channel']
            print item['data']
            
            

try:
    data = data[:-1]
    json.loads(data)
except ValueError:
    print 'This is not a JSON object!'
else:
    print ('JSON found!')