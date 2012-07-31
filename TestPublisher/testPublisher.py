import redis
from json import dumps
import sched, time
from PROD2.com.retry_decorator import Retry


rc = redis.Redis(host='dhcp3-173.si.umich.edu', port=6379, db=0)

rc.delete('user_action_HS')

data={'twitter_ids':['gparuthi','armuro'],'flickr_ids':['59456648@N00','52723107@N00']}
data2={'twitter_tags':['Olympics','cats,dogs'],'flickr_tags':['Olympics','cats,dogs']}

data3={'twitter_ids':['india','sachin']}
data4={'twitter_tags':['india','taj, vegas'],'flickr_tags':['india','taj, vegas']}

rc.hset('user_action_HS','adam',dumps(data))
rc.hset('user_action_HS','gparuthi',dumps(data2))

rc.publish('user_actions', 'updated')

def do_something(sc): 
    print "Doing stuff..."
    rc.hset('user_action_HS','adam',dumps(data))
    rc.hset('user_action_HS','gparuthi',dumps(data2))

    rc.publish('user_actions', 'updated')
    # do your stuff
    sc.enter(4, 1, do_something_diff, (sc,))

def do_something_diff(sc): 
    print "Doing stuff..."
    rc.hset('user_action_HS','adam',dumps(data3))
    rc.hset('user_action_HS','gparuthi',dumps(data4))

    rc.publish('user_actions', 'updated')
    # do your stuff
    sc.enter(4, 1, do_something, (sc,))

#@Retry(86400,delay=5)
def main(): 
    s = sched.scheduler(time.time, time.sleep)
    s.enter(2, 1, do_something, (s,))
    s.run()
    
main()