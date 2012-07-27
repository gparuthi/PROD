import redis
from json import loads, dumps

rc = redis.Redis(host='dhcp3-173.si.umich.edu', port=6379, db=0)

rc.delete('user_action_HS')

data={'twitter_ids':['gparuthi','armuro'],'twitter_tags':['tom cruise'],'flickr_ids':['59456648@N00','52723107@N00']}
data2={'twitter_ids':['gparuthi','temp2'],'twitter_tags':['#olympics2012','#weird'],'flickr_tags':['dogs','cats']}

rc.hset('user_action_HS','adam',dumps(data))
rc.hset('user_action_HS','gparuthi',dumps(data2))

rc.publish('user_actions', 'updated')

