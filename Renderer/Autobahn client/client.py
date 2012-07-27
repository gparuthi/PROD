###############################################################################
##
##  Copyright 2011,2012 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

import sys
from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, \
                               WebSocketClientProtocol, \
                               connectWS
import redis
from json import dumps,loads
import threading

import cmd

def monitor():
    rc = redis.Redis(host='dhcp3-173.si.umich.edu', port=6379, db=0)
    ps = rc.pubsub()
    ps.subscribe(['renderer', 'All'])
    
    print 'monitoring channel', 'renderer'
    
    for item in ps.listen():
          if item['type'] == 'message':
              print item['channel']
              print item['data']
              #2 read the json and get twitterids, etc
              outputConf = loads(item['data'])
              for key in outputConf:
                  print key
                  if(key=="twitter_ids"):
                      message = "hello there!"           
                      #3 according to the output application, load the js code for each widget and broadcast it to the browser
                      
                      self.sendHello()
                      print "hello should be sent"  
               

class my_cmd(cmd.Cmd):
    """Simple command processor example."""

    def do_start(self, line):
        my_thread.start()

    def do_EOF(self, line):
        return True
    
class BroadcastClientProtocol(WebSocketClientProtocol):
   """
   Simple client that connects to a WebSocket server, send a HELLO
   message every 2 seconds and print everything it receives.
   """
   message = "ha"

   def sendHello(self):
       print self.message
       self.sendMessage("hello from..")
       #reactor.callLater(2, self.sendHello)

   def onOpen(self):
      #1 subscribe to the renderer channel on redis
      self.sendHello()



   def onMessage(self, msg, binary):
      print "Got message: " + msg


if __name__ == '__main__':

   factory = WebSocketClientFactory("ws://localhost:9000")
   factory.protocol = BroadcastClientProtocol
   connectWS(factory)
   
   my_thread = threading.Thread(target=monitor)
   my_thread.setDaemon(True)
   my_cmd().do_start('renderer')
      
   reactor.run()
   