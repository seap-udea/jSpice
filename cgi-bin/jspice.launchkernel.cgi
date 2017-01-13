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
#LAUNCH KERNEL
#############################################################
#os.spawnl(os.P_NOWAIT,"ls -R / &> /tmp/ls")
#print "Listo"
cmd="python cgi-bin/jspice.kernel.cgi callback=%s sessionid=%s"%(callback,sessionid)
fnull=open(os.devnull,"w")
subprocess.Popen(shlex.split(cmd),close_fds=True,stdout=fnull,stderr=subprocess.STDOUT)
print callback+"""({"cmd":"%s"})"""%cmd
