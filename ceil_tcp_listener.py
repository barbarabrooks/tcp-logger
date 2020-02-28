
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import os
from curses import ascii
from twisted.internet import reactor, protocol
from twisted.python import log
from datetime import datetime


class ceilTCPListener(protocol.Protocol):
    """This is a very basic TCP listener for the Ceilometer"""

    outpath= "/data/ncas-ceil-1"
    __buffer = ''
    
    def dataReceived(self, data):
      '''reconstitutes a possibly-fragmented incoming TCP record'''

      self.__buffer = self.__buffer + data
     
      if chr(1) in self.__buffer: #start of Header
	  splotdata = self.__buffer.split(chr(1))
	  self.__buffer = chr(1)+splotdata[1].strip()
          if not chr(4) in self.__buffer: #i.e. end of dataline
             #Incomplete; wait for more data
              log.msg('Buffered %s bytes' % len(self.__buffer))
              return
          else:
	      splitdata = self.__buffer.split(chr(4))
              self.writedata(splitdata[0])
              self.__buffer=splitdata[1]
      else:    
          log.msg('Discarded %s bytes' % len(self.__buffer))
          #Drops TCP connection to console
          # so stream from it restarts "clean"
          log.msg(repr(self.__buffer))
          self.transport.loseConnection()

    def writedata(self,data):
        dt = datetime.utcnow()
        today = dt.strftime('%Y-%m-%d')
        try:
            self.factory.outfiles[today].write(dt.isoformat() +',' + data + "\n")
            self.factory.outfiles[today].flush()
        except KeyError: #i.e.file does not exist yet
            try:
                os.umask(022)
                outfile = os.path.join(self.outpath,dt.strftime('%Y%m%d_ceilometer.csv'))
                log.msg('Creating datafile ' + outfile)
                self.factory.outfiles[today] = open(outfile, 'a')
                self.factory.outfiles[today].write(dt.isoformat() +',' + data)
                self.factory.outfiles[today].flush()

            except TypeError:
                log.msg('Invalid TCP data, discarding')

def main():
    """This runs the protocol on port 4002"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(4002,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
