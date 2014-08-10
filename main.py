#!/usr/bin/python

import os,sys,json
from onair import onairset,onairobj

config = 0

def load_config(filepath):
    try:
        fstr = open(filepath).read()
        if fstr == "":
            raise NameError("File is Empty")
    except:
        print "Error While loading Config file: {0}".format(filepath)
    print fstr
    global config
    config = json.loads(fstr)
    print config["onairmethod"]
    return

def init_onair():

    return

def init_server():
    return

if __name__=="__main__":
    """
    Main function for olivia server
    
    argv:
        config path a json file
        default is config.json
    """

    #Load Config
    if len(sys.argv) > 1:
        configpath = sys.argv[1]
    else:
        configpath = "config.json"

    load_config(configpath)
    
    init_onair()
    
    init_server()

    wait_server()

