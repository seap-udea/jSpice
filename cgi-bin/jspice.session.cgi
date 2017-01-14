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
print "Content-Type: text/html";

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
signal.signal(signal.SIGINT,sigHandler)

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

#############################################################
#LAUNCH SESSION
#############################################################
cmd="%s %s/bin/jspice.session sessionid=%s"%(CONF["python"],DIR,sessionid)
logEntry(flog,"Executing cmd:"+cmd)

sys.exit(0)
ferror=open(DIR+"/log/errors.log","a")
popen=subprocess.Popen(shlex.split(cmd),close_fds=True,stdout=ferror,stderr=subprocess.STDOUT)
print callback+"""({"cmd":"%s","pid":"%s"})"""%(cmd,popen.pid)
