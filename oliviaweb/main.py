# coding=utf-8
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template as template
from tornado.platform.twisted import TwistedIOLoop
from twisted.internet import task
import json


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


    def open(self):
        print "Websocket Conneted"
        self.hearttask.start(0.1)

    def on_message(self, message):
        print u"You said: " + message

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
