#!/usr/bin/python
#encoding:utf-8
"""
This file define gameserver for Olivia
"""
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet import task
import json
from onair import *

def inred( s ):
    return"%s[31;2m%s%s[0m"%(chr(27), s, chr(27))

class gameConnect(LineReceiver):

    def senddata(self,mes=None,dictionary=None):
        if mes:
            self.sendLine( mes )
        elif dictionary:
            self.sendLine( json.dumps(dictionary) )

    def lineReceived(self, line):
        if not self.status:
            self.notloginproc(line)
        else:
            self.proc_line_online(line)

    def proc_line_online(self,line):
        try:
            cert = json.loads(line) 
            if cert["type"]=="status":
                self.procstatus(cert)

        except Exception as inst :
            print inred("OnKnown Message on {0}".format(self.addr) )
            print inst
            print line
            return

    def __init__(self,ge):
        self.l =  task.LoopingCall(self.run30hz)
        self.status = False
        self.ge=ge
        self.delimiter = "$"


    def connectionMade(self):
        resp = dict()
        resp["type"] = "auth"
        resp["data"] = "WELCOME"
        self.senddata( dictionary=resp )
        self.addr = self.transport.getPeer()

    def connectionLost(self,reason):
        print "Connect Lose {0}".format (self.addr)

    def authuser(self,user,pwd):
        """
        auth user 
        """
        if ( user== "admin") and ( pwd == "qiaochu"):
            return True
        return False

    def auth(self,cert):
        """
        auth
        """
        try:

            print "user:{0} via {1}".format(cert["username"] ,self.addr)

            if self.authuser(cert["username"],cert["passwd"] ):
                resp = dict()
                resp["type"] = "auth"
                resp["data"] = "CONFIRM"

                resp["loadwidth"] =  2*10
                resp["basei"] = 109650
                resp["basej"] = 49050
                resp["lengthmesh"] = 2304.68

                self.status = True

                self.senddata(dictionary = resp)
                print "已接受 来自 {0} 的连接请求".format(self.addr)
            else:
                print "Auth Failed:Invaild user or Passwd"

        except Exception as inst :
            print inred("Auth Failed:Wrong Message")
            print inst

    def procstatus(self,status):
        try:
            if status['status'] =="ready":
                self.l.start(0.0333)
                print "{0} is ready now".format(self.addr)

        except Exception as inst :
            print inred("OnKnown Message on {0}".format(self.addr) )
            print inst
            return


    def notloginproc(self,line):
        try:
            cert = json.loads(line) 
            if cert["event"]=="auth":
                self.auth(cert)

        except Exception as inst :
            print inred("OnKnown Message on {0}".format(self.addr) )
            print inst
            print line
            return 


    def run30hz(self):
        data = dict()
        data["event"] = "gamedata"
        data["data"] = self.ge.gamedata()
        self.senddata(dictionary = data)
        #print json.dumps(data)
        return

class gameFactory(Factory):
    def __init__(self,ge):
        self.ge=ge
    def buildProtocol(self, addr):
        return gameConnect(self.ge)

def gameServerStart(port,ge):
    print "Start game TCP server at port :{0}".format(port)
    reactor.listenTCP(int(port),gameFactory(ge));

class gameEngine():
    """
    整个游戏引擎的核心在此
    """

    def __init__(self,port):
        gameServerStart(port,self)
        self.aircoll=dict()
        self.task30hz=task.LoopingCall(self.update30hz)
        self.task30hz.start(0.03)
        self.maxiden = 0

    def addAircraft(self,name,air):
        #add aircraft
        self.aircoll[name]=air
        print len(self.aircoll)

    def update30hz(self):
        dt = 0.03333

    def test30(self):
        for a in self.aircoll:
            dt = 0.033
            air=self.aircoll[a]
            air.heart(dt)

    def gamedata(self):
        #Convert All Aircraft to json
        res = dict()
        for a in self.aircoll:
            air=self.aircoll[a]
            res[a]=air.prop
        return res

    def starttest(self):
        self.addAircraft("qiaochu",onairobj(01))

    def nextiden(self):
        self.maxiden += 1
        return self.maxiden -1


def test():
    test=gameEngine(1026)
    qiaochu = onairobj(01)
    for i in range(100):
        qiaochu.heart(0.03)
    test.addAircraft("qiaochu",qiaochu)
    test.addAircraft("qichu",onairobj(01))
    print json.dumps(test.gamedata())

if __name__=="__main__":
    test()
