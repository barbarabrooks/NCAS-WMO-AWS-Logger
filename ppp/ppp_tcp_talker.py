# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.internet import reactor, protocol
from twisted.python import log

class pppTCPTalker(protocol.Protocol):
    """This is a very basic TCP Talker for the Pressure sensor"""

    def datasent(self):
        # send .BP<cr>
        print('message sent')
        self.transport.write(b'.BP\r')

def main():
    """This runs the protocol on port 4002"""
    factory = protocol.ClientFactory()
    reactor.listenTCP(4002,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()


