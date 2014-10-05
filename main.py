#!/usr/bin/python
#encoding:utf-8

import os,sys,json
from onair import onairobj
from twisted.internet import reactor
from tornado.platform.twisted import TwistedIOLoop

config = 0


def inred(s):
    return"%s[31;2m%s%s[0m"%(chr(27), s, chr(27))


def load_config(filepath):
    try:
        fstr = open(filepath).read()
        if fstr == "":
            raise NameError("File is Empty")
    except:
        print inred("Error While loading Config file: {0}".format(filepath))

    global config
    config = json.loads(fstr)

    return


def init_onair():
    """
    Initialize On air device
    
    """
    #if config["onairmethod"]
    return


def init_game_server(port="1026"):
    from gameserver import gameEngine
    ge = gameEngine(port)
    ge.starttest()
    return


def init_webserver():
    TwistedIOLoop().install()
    from oliviaweb.main import init_web
    init_web()


def run_server():
    from twisted.internet import reactor
    reactor.run()
    return


if __name__ == "__main__":
    """
    Main function for olivia server
    
    ARGV:
        config path a json file
        default is config.json
    """

    #Load Config
    print """Hello,Commander
Welcome Olivia Server Version 0.1"""

    try:
        if len(sys.argv) > 1:
            configpath = sys.argv[1]
        else:
            configpath = "config.json"
    
        load_config(configpath)
    
        
        init_onair()
    
        init_game_server(config["gameport"])

        init_webserver()
    
        #init_webserver()
    except Exception as inst :
        print inred("Initialize Failed")
        print inst

    print "Initialization Finished\nWaiting for connect"

    run_server()

