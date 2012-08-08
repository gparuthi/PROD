'''
Created on Jul 28, 2012

@author: gparuthi
'''

import redis
from json import dumps, loads
from websocket import create_connection
from listoperations import union
import outputAppHandlers
from PROD2.com.exceptionhandling import * 
from PROD2.com.retry_decorator import Retry


REDIS_SERVER_URL = 'dhcp2-236.si.umich.edu'

REDIS_SERVER_PORT = 6379
CURRENT_OPERATION = union;

def FinalActionsCalc(_actions, finalActions):
    #print _actions
    for a in _actions:
        if a in finalActions:
            finalActions[a] = CURRENT_OPERATION(finalActions[a], _actions[a]) #change this function for the required operation
        else:
            finalActions[a] = _actions[a]
    return finalActions

#@handle_exception(wssError)
    
def RedisListener(ps,rc):
    for item in ps.listen():
        finalActions={}
        if item['type'] == 'message':
            print item['channel'] + ':' + item['data']
            if item['data'] == 'updated':
                print("sending to redis...")
                #read the list user_action_list and send it to the function  
                user_actions = rc.hgetall("user_action_HS")
                for key in user_actions:
                    finalActions = FinalActionsCalc(loads(user_actions[key]), finalActions)
                #publish it to the renderer channel
                rc.publish('renderer', dumps(finalActions))
                print finalActions
                #SendToWSServer(finalActions)

#@Retry(86400,delay=5)
def main():
    #main code starts here
    print('ContentProvider: Connecting...')
    rc = redis.Redis(host=REDIS_SERVER_URL, port=REDIS_SERVER_PORT, db=0)
    print('OK')
    ps = rc.pubsub()
    ps.subscribe(['user_actions','All'])
    print('Listening...')
    RedisListener(ps,rc)
            

main()
