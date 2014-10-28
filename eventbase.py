import sys
class eventbash():
    def __init__(self):
        self.funclist=dict()
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
