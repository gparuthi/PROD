import redis
from json import dumps, loads

rc = redis.Redis(host='dhcp3-173.si.umich.edu', port=6379, db=0)

ps = rc.pubsub()
ps.subscribe(['user_actions','All'])

def unique(a):
    """ return the list with duplicate elements removed """
    return list(set(a))

def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))

current_operation = union;

def UnionActions(_actions, finalActions):
    #print _actions
    for a in _actions:
        if a in finalActions:
            finalActions[a] = current_operation(finalActions[a], _actions[a]) #change this function for the required operation
        else:
            finalActions[a] = _actions[a]
    return finalActions

for item in ps.listen():
    finalActions={}
    if item['type'] == 'message':
        print item['channel'] + ':' + item['data']
        if item['data'] == 'updated':
            #read the list user_action_list and send it to the function  
            user_actions = rc.hgetall("user_action_HS")
            for key in user_actions:
                finalActions = UnionActions(loads(user_actions[key]), finalActions)
            #publish it to the renderer channel
            rc.publish('renderer', dumps(finalActions))
            print finalActions
