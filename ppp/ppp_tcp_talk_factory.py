# !/usr/bin/python
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.python import log

from ppp_tcp_talker import pppTCPTalker

class pppTCPFactory(Factory):
    protocol = pppTCPTalker

    def buildProtocol(self, addr):
      d = Factory.buildProtocol(self, addr)
      d.factory = self
      return d

def main(): # Listen for TCP:4002

   reactor.listenTCP(4002, pppTCPFactory())
   reactor.run()

if __name__ == '__main__':
    main() #run if this file is called directly, but not if imported

