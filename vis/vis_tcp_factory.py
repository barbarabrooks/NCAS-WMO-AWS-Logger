# !/usr/bin/python
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.python import log

from sys import stdout

from vis_tcp_listener import visTCPListener

class visTCPFactory(Factory):
    protocol = visTCPListener
    outfiles = {} 

    def buildProtocol(self, addr):
      d = Factory.buildProtocol(self, addr)
      d.factory = self
      return d

def main():# Listen for TCP:4005
   log.startLogging(stdout)

   reactor.listenTCP(4005, visTCPFactory())
   reactor.run()

if __name__ == '__main__':
    main() #run if this file is called directly, but not if imported
