#!/usr/bin/python
#encoding:utf-8
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor,task
from math import *

class MulticastPingClient(DatagramProtocol):
    def mkqueue(self):
        queue = []
        for i in range(5):
            for j in range(10):
                length = int(pow(10,i))
                queue.append(bytearray(length))
        return queue

    def startProtocol(self):
        self.transport.write('NETWORK TEST', ("127.0.0.1", 9999))
        self.count = 0
        self.queue = self.mkqueue()
        self.l =  task.LoopingCall(self.task5hz)
        self.l.start(0.2)

    def task5hz(this):
        """
        Sending 5 hz test data
        """
        if this.count >= len(this.queue):
            this.l.stop()
            return 

        this.transport.write(this.queue[this.count], ("127.0.0.1", 9999))
        this.count = this.count+1
        return



reactor.listenMulticast(9998, MulticastPingClient(), listenMultiple=True)
reactor.run()
