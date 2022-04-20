# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import os

from twisted.internet import reactor, protocol
from twisted.python import log
from datetime import datetime


class disTCPListener(protocol.Protocol):
    """This is a very basic TCP listener for Distrometer sensor"""

    outpath = "/home/pi/DATA/DIS"
    __buffer = ''
    __buffer2 = ''

    def dataReceived(self, data):
      '''reconstitutes a possibly-fragmented incoming TCP record'''
      self.__buffer = self.__buffer + data
      if self.__buffer[0] == '\x02': # start of transmission <STX> = <\x02> 
          if self.__buffer[-1] != '\x03': # i.e. end of transmission <ETX> = <\x03>
             # Incomplete; wait for more data
              #log.msg('Buffered %s bytes' % len(self.__buffer))
              return
      st = self.__buffer.find('\x02')
      ed = self.__buffer.find('\x03')
      if ((ed > -1) and (st > -1)):
          self.__buffer2 = self.__buffer[st:ed]
          self.__buffer2 = self.__buffer2.replace(";" , ",") #raw data uses ; as the deliminater change it to
          log.msg(repr(self.__buffer2))
          self.writedata(self.__buffer2)
          self.__buffer = ''
          self.__buffer2 = ''
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
                outfile = os.path.join(self.outpath,dt.strftime('%Y%m%d_dis.csv'))
                log.msg('Creating or opening datafile ' + outfile)
                self.factory.outfiles[today] = open(outfile, 'a')
                self.factory.outfiles[today].write(dt.isoformat() +',' + data)
                self.factory.outfiles[today].flush()
            except TypeError:
                log.msg('Invalid TCP data, discarding')

def main():
    """This runs the protocol on port 4006"""
    factory = protocol.ServerFactory()
    #factory.protocol = Echo
    reactor.listenTCP(4006,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()

