'''
Created on Jul 28, 2012

@author: gparuthi
'''

import redis
from json import dumps, loads
from websocket import create_connection
from listoperations import union
import outputAppHandlers
from com.exceptionhandling import * 
from com.retry_decorator import Retry

REDIS_SERVER_URL = 'dhcp3-173.si.umich.edu'
REDIS_SERVER_PORT = 6379
WEBSOCKET_SERVER_URL = 'ws://dhcp3-173.si.umich.edu:9000'#"ws://localhost:9000";#'dhcp3-173.si.umich.edu:9000'
CURRENT_OPERATION = union;

def FinalActionsCalc(_actions, finalActions):
    #print _actions
    for a in _actions:
        if a in finalActions:
            finalActions[a] = CURRENT_OPERATION(finalActions[a], _actions[a]) #change this function for the required operation
        else:
            finalActions[a] = _actions[a]
    return finalActions

@handle_exception(wssError)
def SendToWSServer(finalActions):
    ws = create_connection(WEBSOCKET_SERVER_URL)
    ws.send("RESET");

    for ac in finalActions:
        #print "key:" + ac
        if(ac=="twitter_ids"):
            #3 according to the output application, load the js code for each widget and broadcast it to the browser
            msg = outputAppHandlers.TwitterIdJS(finalActions[ac])
            print msg
            ws.send(msg)
        if(ac=="twitter_tags"):
            #3 according to the output application, load the js code for each widget and broadcast it to the browser
            msg = outputAppHandlers.TwitterTagsJS(finalActions[ac])
            print msg
            ws.send(msg)
            
        if(ac=="flickr_tags"):            
            #3 according to the output application, load the js code for each widget and broadcast it to the browser
            msg = outputAppHandlers.FlickrTags(finalActions[ac])
            print msg
            ws.send(msg)
            
        if(ac=="flickr_ids"):            
            #3 according to the output application, load the js code for each widget and broadcast it to the browser
            msg = outputAppHandlers.FlickrTags(finalActions[ac])
            print msg
            ws.send(msg)
         
    ws.close()
    
def RedisListener(ps,rc):
    for item in ps.listen():
        finalActions={}
        if item['type'] == 'message':
            print item['channel'] + ':' + item['data']
            if item['data'] == 'updated':
                #read the list user_action_list and send it to the function  
                user_actions = rc.hgetall("user_action_HS")
                for key in user_actions:
                    finalActions = FinalActionsCalc(loads(user_actions[key]), finalActions)
                #publish it to the renderer channel
                rc.publish('renderer', dumps(finalActions))
                print finalActions
            SendToWSServer(finalActions)    

@Retry(86400,delay=5)
def main():
    #main code starts here
    print('Connecting...')
    rc = redis.Redis(host=REDIS_SERVER_URL, port=REDIS_SERVER_PORT, db=0)
    print('OK')
    ps = rc.pubsub()
    ps.subscribe(['user_actions','All'])
    print('Listening...')
    RedisListener(ps,rc)
            

main()
