'''
Created on Jul 30, 2012

@author: gparuthi
'''
import redis
from json import loads, dumps
from websocket import create_connection
import outputAppHandlers

REDIS_SERVER_URL = 'dhcp2-236.si.umich.edu'
REDIS_SERVER_PORT = 6379
WEBSOCKET_SERVER_URL = 'ws://gauravparuthi.com:9000'#"ws://localhost:9000";#'dhcp3-173.si.umich.edu:9000'
#OUTPUT_JSON_SPEC = {'twitter_ids':[],'twitter_tags':[],'flickr_ids':[]}

_curConf = {}
nextDivId = 0



def getId(div_id):
    return 'id' + str(div_id)

class Renderer:
    DontAddList = {}
    CurConf = {}
    def Remove(self, div_id):
        # send message to web socket to remove the div_id
        print('removing...')
        
    def Add(self, div_id, source, width, height ):
        """
        send message to add a div_id with given source
        """
    def getRemoveJSON(self, div_id):
        ret = {'f':'R', 'id':getId(div_id)  }
        return ret
    
    def getAddJSON(self, div_id, source, width, height):
        ret = {'f':'A', 'id':getId(div_id), 'src':source, 'w':width, 'h':height  }
        return ret

def GetSource(output_type,conf):
    msg = ""
    if(output_type=="twitter_ids"):
        msg = outputAppHandlers.TwitterIdJS(conf)
    elif(output_type=="twitter_tags"):
        msg = outputAppHandlers.TwitterTagsJS(conf)
    elif(output_type=="flickr_tags"):            
        msg = outputAppHandlers.FlickrTags(conf)
    elif(output_type=="flickr_ids"):            
        msg = outputAppHandlers.FlickrTags(conf)
    return msg

def SendToWSServer(finalActions):
    print finalActions
    ws = create_connection(WEBSOCKET_SERVER_URL)
    global nextDivId
    global _curConf
    height = 400
    width = 300
    _dontAdd = {}
    _nextConf = {}
    r= Renderer()
    
    for ac in finalActions:
        print "key:" + ac + "| value:" 
        t = {}
        print finalActions[ac]
        for c in finalActions[ac]:
            t[c] = nextDivId
            nextDivId+=1
        _nextConf[ac] = t
        _dontAdd[ac] = {}
    
    # remove un needed divs
    for ac in _curConf:
        if ac in _nextConf:
            print 'key found in the new conf:'+ac
            for c in _curConf[ac]:
                #print "value in old conf:"+c
                if c in _nextConf[ac]:
                    print "value found in new conf:"+c
                    # change the id to the one already set
                    _nextConf[ac][c]=_curConf[ac][c]
                    # add the id to _dontAdd
                    _dontAdd[ac][c] = 1
                else:
                    # remove the div element from the renderer
                    #Renderer.Remove(_curConf[c])
                    print "removing conf:"+_curConf[ac][c]
                    ws.send(dumps(r.getRemoveJSON(_curConf[ac][c])))
        else:
            print "removing conf:"
            print _curConf[ac]
            # send remove command for all the values for current ac.. ac is flickr_tags, c is 'dogs,cats' etc
            for c in _curConf[ac]:
                ws.send(dumps(r.getRemoveJSON(_curConf[ac][c])))
        
    # add the ones in nextConf to the renderer, and those not in dontAdd
    for ac in _nextConf:
        for c in _nextConf[ac]:
            if c not in _dontAdd[ac]:
                add_json = r.getAddJSON(_nextConf[ac][c], GetSource(ac, c), width, height)
                print "adding json:" + dumps(add_json)
                ws.send(dumps(add_json))
    
    _curConf = _nextConf
    
    ws.close()

def RedisListener(ps,rc):
    for item in ps.listen():
        finalActions={}
        if item['type'] == 'message':
            print item['channel'] + ':' + item['data']
            finalActions = loads(item['data'])            
            SendToWSServer(finalActions) 

def main():
    #main code starts here
    # create hs for each conf in input type
    
    
    print('RendererController: Connecting...')
    rc = redis.Redis(host=REDIS_SERVER_URL, port=REDIS_SERVER_PORT, db=0)
    print('OK')
    ps = rc.pubsub()
    ps.subscribe(['renderer'])
    print('Listening...')
    RedisListener(ps,rc)


# read from redis and see what changed
print nextDivId
nextDivId +=1
results = main()

