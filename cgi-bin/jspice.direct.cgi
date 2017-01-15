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
# Function: jSpice proxy
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
DIR=PATH+"/../"
from jspice import *

#############################################################
#CANCEL BEHAVIOR
#############################################################
def sigHandler(signal,frame):
    import sys
    logEntry(flog,"Terminating client")
    sys.exit(0)
signal.signal(signal.SIGINT,sigHandler)

#############################################################
#READ CONFIGURATION FILE
#############################################################
loadConf(DIR+"/jspice.cfg")

#############################################################
#PARAMETERS
#############################################################
params=cgi.FieldStorage();

# Mandatory
code=getArg("code",params=params)
if code=="jspice=True":logEntry=logEntryClean
port=int(getArg("port",params=params))

# Optional
timeout=float(getArg("timeout",0.1,params=params))
callback=getArg("callback","json",params=params)
server=getArg("server","127.0.0.1",params=params)
sessionid=getArg("sessionid","0"*20,params=params)

sessdir="%s/sessions/%s/"%(DIR,sessionid)
if not os.path.isdir(sessdir):sessdir=DIR+"/log"
flog=open(sessdir+"/proxy.log","a")
logEntry(flog,"Proxy invoked calling to port %d of server %s with timeout %.1f"%(port,server,timeout),sessionid)
logEntry(flog,"Proxy commands:\n\tCallback:%s\n\tCode:\n\t%s"%(callback,code),sessionid)

#############################################################
#EXECUTION
#############################################################
context=zmq.Context()
socket=Socket(context,zmq.REQ)
socket.connect("tcp://%s:%s"%(server,port))
socket.send(code);
if "exit(" in code:
    logEntry(flog,"Exiting signal to server in port %d"%port)
    print "Exit with code:%s"%code
else:
    response=socket.recv(timeout=timeout);

    #############################################################
    #OUTPUT
    #############################################################
    code=code.replace("\n","").replace("\t","")
    print callback+"""({"code":"%s","configuration":"%s","response":"%s"})"""%\
        (code,"{}".format(CONF),response.replace("\"","\\\""))

    if response is None:
        logEntry(flog,"No response in port %d"%port)
        termProcess()
