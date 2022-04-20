# !/usr/bin/python
from twisted.internet.protocol import Protocol, ClientFactory

from twisted.internet import reactor
from twisted.python import log

from sys import stdout

from ppp.ppp_tcp_listener import pppTCPListener

class pppTCPFactory(ClientFactory):
    protocol = pppTCPListener
    outfiles = {}

    def buildProtocol(self, addr):
      d = ClientFactory.buildProtocol(self, addr)
      d.factory = self
      return d

def main():# Listen for TCP:4002
   log.startLogging(stdout)

   factory = protocol.ClientFactory()
   #factory.protocol = Echo
   reactor.connectTCP('np5650-8-dtl_8732.amof', 4002,factory)
   reactor.run()

if __name__ == '__main__':
    main() #run if this file is called directly, but not if imported

