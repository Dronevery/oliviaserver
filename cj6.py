#!/usr/bin/python
# coding=utf-8
from onair import *
class cj6(onairobj):
    def proc_line_online(self,line):
        """
            使用数据
        """
        try:
            pp = json.loads(line)["data"]
            prop = self.prop
            for a in pp:
                try:
                    prop[a] = float(pp[a])
                except:
                    prop[a] = pp[a]
                    """
            prop["locx"] = float(pp["locx"])
            prop["locy"] = float(pp["locy"])
            prop["locz"] = float(pp["locz"])
            prop["yaw"] = float(pp["yaw"])
            prop["pitch"] = float(pp["pitch"])
            prop["roll"] = float(pp["roll"])
            """
        except Exception as inst :
            print inred("OnKnown Message on {0}:\n".format(self.addr) )
            print inst

        return

def listencj6(ge,port):
    reactor.listenTCP(port,airobjFactory(ge,cj6))
