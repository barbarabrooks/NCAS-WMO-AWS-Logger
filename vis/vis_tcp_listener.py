# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import os

from twisted.internet import reactor, protocol
from twisted.python import log
from datetime import datetime


class visTCPListener(protocol.Protocol):
    """This is a very basic TCP listener for Visibility sensor"""

    outpath = "/home/pi/DATA/VIS"
    __buffer = ''

    def dataReceived(self, data):
      '''reconstitutes a possibly-fragmented incoming TCP record'''
      self.__buffer = self.__buffer + data
      if self.__buffer[0:6] == 'SWS100,':
          if self.__buffer[-2:-1] != '\\r\\n': # i.e. end of dataline <cr><lf>
             # Incomplete; wait for more data
              log.msg('Buffered %s bytes' % len(self.__buffer))
              return
      else:
          #log.msg('Message length %s bytes' % len(self.__buffer))
          # Drops TCP connection to console
          # so stream from it restarts "clean"
          if len(self.__buffer) <= 56:
             log.msg(repr(self.__buffer))
             self.writedata(self.__buffer)
             self.__buffer=''
          self.transport.loseConnection()

    def writedata(self,data):
        dt = datetime.utcnow()
        today = dt.strftime('%Y-%m-%d')
        try:
           self.factory.outfiles[today].write(dt.isoformat() +',' + data)
           self.factory.outfiles[today].flush()
        except KeyError: # i.e.file does not exist yet
            try:
                os.umask(022)
                outfile = os.path.join(self.outpath,dt.strftime('%Y%m%d_vis.csv')) 
                log.msg('Creating or opening datafile ' + outfile)
                self.factory.outfiles[today] = open(outfile, 'a')
                self.factory.outfiles[today].write(dt.isoformat() +',' + data)
                self.factory.outfiles[today].flush()
            except TypeError:
                log.msg('Invalid TCP data, discarding')

def main():
    """This runs the protocol on port 4005"""
    factory = protocol.ServerFactory()
    #factory.protocol = Echo
    reactor.listenTCP(4005,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()

