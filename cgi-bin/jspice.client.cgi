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
# Function: jSpice client
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
flog=open(PATH+"/../log/client.log","a")
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
CONF=loadConf(PATH+"/../")

#############################################################
#CGI PARAMETERS
#############################################################
params=cgi.FieldStorage();
code=params.getvalue("code")
callback=params.getvalue("callback")

if code is None:
    iarg=1
    try:
        port=int(argv[iarg]);iarg+=1
        code=argv[iarg];iarg+=1
        timeout=float(argv[iarg]);iarg+=1
        callback="json"
    except:
        print>>stderr,"You must provide port, code and timeout: jspice.client.cgi <port> '<code>' timeout"
        sys.exit(1)
else:
    timeout=1000

logEntry(flog,"Client invoked calling to port %d with timeout %.1f"%(port,timeout))
logEntry(flog,"Client commands:\n\tCallback:%s\n\tCode:\n\t%s"%(callback,code))

#############################################################
#EXECUTION
#############################################################
context=zmq.Context()
#Traditional: socket=context.socket(zmq.REQ)
socket=Socket(context,zmq.REQ)
socket.connect("tcp://urania.udea.edu.co:%s"%port)
socket.send(code);
if "exit(" in code:
    logEntry(flog,"Exiting signal to server in port %d"%port)
else:
    #Traditional: response=socket.recv();
    response=socket.recv(timeout=timeout);
    #############################################################
    #OUTPUT
    #############################################################
    print callback+"""({"code":"%s","configuration":"%s","response":"%s"})"""%\
        (code,"{}".format(CONF),response)
    if response is None:
        logEntry(flog,"No response in port %d"%port)
        termProcess()
