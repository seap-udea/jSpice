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
# Function: jSpice session
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
flog=open(DIR+"/log/sessions.log","a")

#############################################################
#CANCEL BEHAVIOR
#############################################################
def sigHandler(signal,frame):
    import sys
    logEntry(flog,"Terminating server in port %d"%port)
    sys.exit(0)
for sig in SIGNALS:signal.signal(sig,sigHandler)

#############################################################
#READ CONFIGURATION FILE
#############################################################
loadConf(DIR+"/jspice.cfg")

#############################################################
#CGI PARAMETERS
#############################################################
params=cgi.FieldStorage();
sessionid=getArg("sessionid","0"*20,params=params)
callback=getArg("callback","callbackJsonp",params=params)
port=int(getArg("port",5500,params=params))
proxy=getArg("proxy","127.0.0.1",params=params)
