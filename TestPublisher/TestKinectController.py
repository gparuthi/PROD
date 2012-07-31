import redis
from json import dumps
import sched, time
from PROD2.com.retry_decorator import Retry

REDIS_SERVER_URL = 'dhcp3-173.si.umich.edu'
REDIS_SERVER_PORT = 6379

def RedisListener(ps,rc):
    for item in ps.listen():
        finalActions={}
        if item['type'] == 'message':
            print item['channel'] + ':' + item['data']
            if(item['data']=="RightHello"):
                print('righthello')
                rc.delete('user_action_HS')
                data2={'twitter_tags':['#PeopleIHaveSeenLive',],'flickr_tags':['dogs']}
                rc.hset('user_action_HS','user',dumps(data2))
            if(item['data']=="LeftHello"):
                print('lefthello')
                rc.delete('user_action_HS')
                data2={'twitter_tags':['#Olympics',],'flickr_tags':['Olympics']}
                rc.hset('user_action_HS','user',dumps(data2))
            if(item['data']=="Standing"):
                print('standing')
                rc.delete('user_action_HS')
                data2={'twitter_tags':['#Olympics',],'flickr_tags':['cats']}
                rc.hset('user_action_HS','user',dumps(data2))
            rc.publish('user_actions', 'updated')
                
            #print("sending to redis..")
            #read the list user_action_list and send it to the function  

       

def main():
    #main code starts here
    print('KinectController: Connecting...')
    rc = redis.Redis(host=REDIS_SERVER_URL, port=REDIS_SERVER_PORT, db=0)
    print('OK')
    ps = rc.pubsub()
    ps.subscribe(['user_gesture','All'])
    print('Listening...')
    RedisListener(ps,rc)
    

main()