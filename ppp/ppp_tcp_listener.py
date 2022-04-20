# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import os

from twisted.internet import reactor, protocol
from twisted.python import log
from datetime import datetime


class pppTCPListener(protocol.Protocol):
    """This is a very basic TCP listener for the Pressure sensor"""

    outpath = "/home/pi/DATA/PPP"
    __buffer = ''

    def connectionMade(self):
        self.transport.write('\r.BP\r')

    def dataReceived(self, data):
        '''reconstitutes a possibly-fragmented incoming TCP record'''
        if len(data) == 9:
           self.__buffer = data
           #log.msg(repr(self.__buffer))
           self.writedata(self.__buffer)
           self.__buffer = ''

    def writedata(self,data):
        dt = datetime.utcnow()
        today = dt.strftime('%Y-%m-%d')
        try:
           self.factory.outfiles[today].write(dt.isoformat() +',' + data)
           self.factory.outfiles[today].flush()
        except KeyError: # i.e.file does not exist yet
            try:
                os.umask(022)
                outfile = os.path.join(self.outpath,dt.strftime('%Y%m%d_ppp.csv'))
                log.msg('Creating or opening datafile ' + outfile)
                self.factory.outfiles[today] = open(outfile, 'a')
                self.factory.outfiles[today].write(dt.isoformat() +',' + data)
                self.factory.outfiles[today].flush()
            except TypeError:
                log.msg('Invalid TCP data, discarding')

def main():
    """This runs the protocol on port 4002"""
    factory = protocol.ClientFactory()
    #factory.protocol = Echo
    reactor.connectTCP('np5650-8-dtl_8732.amof', 4002,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()


