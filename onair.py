import os,sys,json
from math import *

class onairobj:
    """
    This is a air obj
    X:South
    Y:North
    """

    def __init__(self,iden,a=5000,theta=0,omega=0.1):
        self.prop = dict()
        self.iden=iden
        prop=self.prop
        prop["locx"]=0
        prop["locy"]=0
        prop["locz"]=0
        prop["yaw"] = 0
        self.a = a
        self.theta = theta
        self.omega = omega
        return 

    def send_client(self):
        return 

    def set(self,json):
        return

    def heart(self,dt):
        #r=a(1-sin\theta)
        omega = self.omega
        a = self.a 

        self.theta += dt*omega
        theta = self.theta

        r = a *(1- sin(theta) )

        prop=self.prop
        dx = prop["locx"] - r * sin(theta)
        dy = prop["locy"] - r * cos(theta)
        prop["locx"] = r * sin(theta)
        prop["locy"] = r * cos(theta)
        prop["locz"] = 1000 * sin(theta) +100

        yaw = 0

        if dy > 0:
            yaw = atan(dx/dy)/3.1415926*180
        else:
            yaw = atan(dx/dy)/3.1415926*180+180;
        prop["yaw"]=yaw
        return
