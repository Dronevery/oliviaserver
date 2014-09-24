#!/usr/bin/python
#encoding:utf-8
"""
This file define gameserver for Olivia
"""
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Echo(DatagramProtocol):
    def datagramReceived(self, data, (host, port)):
        print "received length %d from %s:%d" % (len(data), host, port)
        self.transport.write(data, (host, port))

reactor.listenUDP(9999, Echo())
reactor.run()
