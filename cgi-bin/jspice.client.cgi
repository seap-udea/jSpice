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
        callback="json"
    except:
        print>>stderr,"You must provide port and code: jspice.client.cgi <port> '<code>'"
        sys.exit(1)

logEntry(flog,"Client invoked calling to port %d"%port)
logEntry(flog,"Client commands:\n\tCallback:%s\n\tCode:\n\t%s"%(callback,code))

#############################################################
#EXECUTION
#############################################################
context=zmq.Context()
socket=context.socket(zmq.REQ)
socket.connect("tcp://urania.udea.edu.co:%s"%port)
socket.send(code);
if "exit(" in code:
    logEntry(flog,"Exiting signal to server in port %d"%port)
else:
    response=socket.recv();
    #############################################################
    #OUTPUT
    #############################################################
    print callback+"""({"code":"%s","configuration":"%s","response":"%s"})"""%\
        (code,"{}".format(CONF),response)
