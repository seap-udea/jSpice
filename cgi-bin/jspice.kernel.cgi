#!/usr/bin/python
#############################################################
#             /######            /##                        #
#            /##__  ##          |__/                        #
#        /##| ##  \__/  /######  /##  /#######  /######     #
#       |__/|  ######  /##__  ##| ## /##_____/ /##__  ##    #
#        /## \____  ##| ##  \ ##| ##| ##      | ########    #
#       | ## /##  \ ##| ##  | ##| ##| ##      | ##_____/    #
#       | ##|  ######/| #######/| ##|  #######|  #######    #
#       | ## \______/ | ##____/ |__/ \_______/ \_______/    #
#  /##  | ##          | ##                                  #
# |  ######/          | ##                                  #
#  \______/           |__/                                  #
#							    #
#                 Jorge I. Zuluaga (C) 2016		    #
#############################################################
# Function: jSpice kernel
#############################################################

#############################################################
#HEADER
#############################################################
print "Content-Type: text/html\n\n";

#############################################################
#EXTERNAL MODULES
#############################################################
import sys,os,inspect
PATH=os.path.realpath(
    os.path.abspath(os.path.split(
        inspect.getfile(
            inspect.currentframe()))[0]))
sys.path.insert(0,PATH+"/../bin")
flog=open(PATH+"/../log/server.log","a")
from jspice.core import *

#############################################################
#CANCEL BEHAVIOR
#############################################################
def sigHandler(signal,frame):
    import sys
    logEntry(flog,"Terminating server in port %d"%port)
    sys.exit(0)
signal.signal(signal.SIGINT,sigHandler)

#############################################################
#READ CONFIGURATION FILE
#############################################################
CONF=loadConf(PATH+"/../")

#############################################################
#CGI PARAMETERS
#############################################################
params=cgi.FieldStorage();
callback=params.getvalue("callback")

#############################################################
#LOAD SPICE KERNELS
#############################################################
for kernel in glob.glob(PATH+"/../"+CONF["kernels_dir"]+"/*"):
    spy.furnsh(kernel)

#############################################################
#INITIALIZE COMMUNICATIONS
#############################################################
for port in xrange(CONF["port_range"][0],CONF["port_range"][1]):
    try:
        context=zmq.Context()
        socket=context.socket(zmq.REP)
        socket.bind("tcp://*:%d"%port)
        logEntry(flog,"Listening in port %d"%port)
        break
    except zmq.error.ZMQError:
        logEntry(flog,"Error with port %d"%port)

#############################################################
#REMOVE AND ADD MODULES
#############################################################
#REMOVE SENSIBLE MODULES
exec("del(%s)"%CONF["sensible_modules"])
#ADD NEW MODULES
for mod in CONF["numerical_modules"]:exec(mod)

#############################################################
#RECEIVE
#############################################################
i=0
instance="server in port %d"%port
logEntry(flog,"Starting server...",instance)
while True:
    cmd=socket.recv()
    logEntry(flog,"Command received: %s"%cmd,instance)
    if "exit(" in cmd:break
    try:
        exec(cmd)
        logEntry(flog,"Command succesfully executed.",instance)
    except Exception as e:
        logEntry(flog,"Error:\n\t"+str(e))
    socket.send("{}".format(globals()))
    i+=1
logEntry(flog,"Exiting server",instance)
