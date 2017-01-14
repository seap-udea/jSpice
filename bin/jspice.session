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
DIR=PATH+"/../"
sys.path.insert(0,DIR+"/bin")
from jspice.core import *

#############################################################
#LOG FILE
#############################################################
flog=open(DIR+"/log/server.log","a")

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
CONF=loadConf(DIR)
jspice=dict2obj({})
jspiced=jspice.__dict__

#############################################################
#CGI PARAMETERS
#############################################################
params=cgi.FieldStorage();
sessionid=getArg("sessionid","1",params=params)
callback=getArg("callback","json",params=params)

#############################################################
#LOAD SPICE KERNELS
#############################################################
for kernel in glob.glob(DIR+"/"+CONF["kernels_dir"]+"/*"):
    spy.furnsh(kernel)

#############################################################
#INITIALIZE COMMUNICATIONS
#############################################################
qserving=False
for port in xrange(CONF["port_range"][0],CONF["port_range"][1]):
    try:
        context=zmq.Context()
        #Traditional: socket=context.socket(zmq.REP)
        socket=context.socket(zmq.REP)
        #With timeout:
        socket.bind("tcp://*:%d"%port)
        logEntry(flog,"Listening in port %d to sessionid %s"%(port,sessionid))
        os.system("mkdir -p %s/sessions/%s"%(DIR,sessionid))
        f=open("%s/sessions/%s/port"%(DIR,sessionid),"w")
        f.write('jsonpCallback({"port":%d})'%port)
        f.close()
        qserving=True
        break
    except zmq.error.ZMQError:
        logEntry(flog,"Error with port %d"%port)
instance="server in port %d"%port

if not qserving:
    logEntry(flog,"No available ports")
    print callback+"""({"status":"no port"})"""
    exit(1)
else:
    print callback+"""({"status":"listening on port %d"})"""%port

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
logEntry(flog,"Starting server...",instance)
while True:
    cmd=socket.recv()
    if cmd=="jspice=True":
        rlogEntry=logEntryClean
    else:
        rlogEntry=logEntry

    rlogEntry(flog,"Command received: %s"%cmd,instance)
    if "exit(" in cmd:break
    try:
        exec(cmd)
        rlogEntry(flog,"Command succesfully executed.",instance)
    except Exception as e:
        rlogEntry(flog,"Error:\n\t"+str(e))
    socket.send("{}".format(globals()))
    i+=1

rlogEntry(flog,"Exiting server",instance)
print callback+"""{"kill":true}""" 
