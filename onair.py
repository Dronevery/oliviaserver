# coding=utf-8
import os,sys,json
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet import task
from math import *

def inred( s ):
    return"%s[31;2m%s%s[0m"%(chr(27), s, chr(27))


class onairobj(LineReceiver):
    """This is a air obj
    Create by a socket via tcp
    暂时关闭验证功能
    X:South
    Y:North"""

    def __init__(self,ge):
        """
            初始化
        """

        #添加到核心中
        self.ge = ge
        self.iden=ge.nextiden()
        ge.addAircraft("name0",self)
        self.delimiter = "$"
        
        #初始化属性
        self.prop = dict()
        prop=self.prop
        prop["locx"]=0
        prop["locy"]=0
        prop["locz"]=0
        prop["yaw"] = 0
        prop["yaw"] = 0
        prop["pitch"] = 0
        prop["roll"] = 0
        self.status = True

        return 

    def connectionMade(self):
        """
            建立链接
        """
        resp = dict()
        resp["type"] = "auth";
        resp["data"] = "WELCOME";
        #self.senddata( dictionary=resp );
        self.addr = self.transport.getPeer()
        print "On air Connect Made {0}".format (self.addr)
        return

    def lineReceived(self, line):
        if not self.status:
            self.notloginproc(line)
        else:
            self.proc_line_online(line)

    def proc_line_online(self,line):
        """
            使用数据
        """
        try:
            pp = json.loads(line)["data"]
            prop = self.prop
            prop["locx"] = float(pp["locx"])
            prop["locy"] = float(pp["locy"])
            prop["locz"] = float(pp["locz"])
            prop["yaw"] = float(pp["yaw"])
            prop["pitch"] = float(pp["pitch"])
            prop["roll"] = float(pp["roll"])
            print(pp)
        except Exception as inst :
            print inred("OnKnown Message on {0}:\n{1}".format(self.addr,pp) )
            print inst

        return

    def notloginproc(self,line):
        """
        验证
        """
        try:
            cert = json.loads(line) 
            if cert["type"]=="auth":
                self.auth(cert)

        except Exception as inst :
            print inred("OnKnown Message on {0}".format(self.addr) )
            print inst
            return 

    def connectionLost(self,reason):
        print "On air Connect Lose {0}".format (self.addr)


class airobjFactory(Factory):

    def __init__(self, ge ):
        self.ge = ge

    def buildProtocol(self,addr):
        return onairobj(self.ge)

def startair(ge):
    reactor.listenTCP(4707,airobjFactory(ge))