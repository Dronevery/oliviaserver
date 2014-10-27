from onair import *
import json
import  sys

class mavonair(onairobj):
    def __init__(self,ge):
        onairobj.__init__(self,ge)
        self.funclist = dict()
        self.addevent("GLOBAL_POSITION_INT",self.update_pos)
    def runevent(self,event,data):
        if event in self.funclist:
            self.funclist[event] (data)
        else:
            print >>sys.stderr,"No SUCH EVENT {0}".format(event)

    def addevent(self,event,func):
        self.funclist[event] = func

    def proc_line_online(self,line):
        #print line
        try:
            res = json.loads(line)
            type = res['type']
            data = res['data']
        except Exception as inst :
            print >>sys.stderr , "Error {0} while parse {1}".format(inst,line)
            return
        self.runevent(type,data)
        self.sendLine(line)

    def update_pos(self,data):
        prop = self.prop
        prop['lon'] = float(data['lon']) /10000000
        prop['lat'] = float(data['lat']) /10000000
        prop['height'] = float(data['alt']) /1000
        prop['vx'] = float(data['vx'])
        prop['vy'] = float(data['vy'])
        prop['vz'] = float(data['vz'])

def listenmav(ge,port):
    reactor.listenTCP(port,airobjFactory(ge,mavonair))