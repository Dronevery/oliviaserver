from onair import *
import json
import  sys
import eventbase

class mavonair(onairobj,eventbase):
    def __init__(self,ge):
        onairobj.__init__(self,ge)
        self.addevent("GLOBAL_POSITION_INT",self.update_pos)
        self.addevent("ATTITUDE",self.update_att)
        self.addevent('arm',self.arm)

    def update_pos(self,data):
        prop = self.prop
        prop['lon'] = float(data['lon']) /10000000
        prop['lat'] = float(data['lat']) /10000000
        prop['height'] = float(data['alt']) /1000
        prop['vx'] = float(data['vx'])
        prop['vy'] = float(data['vy'])
        prop['vz'] = float(data['vz'])

    def update_att(self,data):
        prop= self.prop
        prop['roll'] =  float(data['roll'])
        prop['pitch'] =  float(data['pitch'])
        prop['yaw'] =  float(data['yaw'])
    def arm(self,data):
        res= dict()
        res['type'] = "arm"
        res['action']=data


    def action(self,data):
        print "recive action:{0}".format(data)
        self.runevent(data['type'],data['action'])

def listenmav(ge,port):
    reactor.listenTCP(port,airobjFactory(ge,mavonair))