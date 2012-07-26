import redis
from json import loads, dumps

rc = redis.Redis(host='dhcp3-173.si.umich.edu', port=6379, db=0)

rc.delete('user_action_HS')

data={'twitter_ids':['gparuthi','armuro'],'twitter_tags':['#sports']}
data2={'twitter_ids':['gparuthi','temp2'],'twitter_tags':['#news','#india']}

rc.hset('user_action_HS','adam',dumps(data))
rc.hset('user_action_HS','gparuthi',dumps(data2))


rc.publish('user_actions', 'updated')

