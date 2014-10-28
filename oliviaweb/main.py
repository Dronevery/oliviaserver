# coding=utf-8
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template as template
from tornado.platform.twisted import TwistedIOLoop
from twisted.internet import task
import json
import sys


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = template.Loader("./web")
        t  = loader.load("index.html")
        html = t.generate()
        self.write(html)

sendfunc = 0

def send(event,data):
    if sendfunc!= 0:
        sendfunc(event,data)
        return True
    else:
        import sys
        print >> sys.stderr, "Websocket not connected"
        return False


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def initialize(self, config,ge):
        self.config = config
        self.ge = ge
        global sendfunc
        sendfunc = self.send
        self.hearttask = task.LoopingCall(self.heartbeat)
        self.funclist = dict()

        self.addevent("actiononair",self.actiononair())

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

    def open(self):
        print "Websocket Conneted"
        self.hearttask.start(0.1)

    def on_message(self, message):
        self.proc_line_online(message)

    def on_close(self):
        print "WebSocket closed"
        global sendfunc
        sendfunc = 0
        self.hearttask.stop()

    def send(self,event,data):
        mes = dict()
        mes["event"] = event
        mes["data"] = data
        self.write_message(json.dumps(mes))

    def heartbeat(self):
        str = self.ge.gamedata()
        self.send ("gamedata" , str)

    def actiononair(self,data):
        name = data['name']
        self.ge.aircoll[name].action(data)


def init_webpanel(config,ge):
    TwistedIOLoop().install()
    import logging
    logging.getLogger("tornado.access").addHandler(lambda  x:x)
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "./static/"}),
        (r"/websocket/",WebSocketHandler,{"config":config,"ge":ge})
    ])
    application.listen(8000)
    global send
    return send
