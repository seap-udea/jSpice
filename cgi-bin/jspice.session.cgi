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
from jspice import *
from jspice.spicext import *

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
sessionid=getArg("sessionid","0",params=params)
callback=getArg("callback","callbackJsonp",params=params)
port=int(getArg("port",5500,params=params))
proxy=getArg("proxy","*",params=params)
try:client=cgi.escape(os.environ["REMOTE_ADDR"])
except:client="*"

#############################################################
#CHECK IF SESSION IS REGISTERED
#############################################################
results=sqlExec("select port,pid from sessions where sessionid='%s'"%sessionid,DIR+"/sessions.db")
if len(results)>0:
    port=int(results[0][0])
    pid=int(results[0][1])
    print callback+"""({"pid":"%s","port":%d})"""%(pid,port)
    exit(0)

#############################################################
#LAUNCH SESSION
#############################################################
cmd="%s %s/bin/jspice.session sessionid=%s port=%d proxy='%s' client='%s'"%(CONF["python"],DIR,sessionid,port,proxy,client)
logEntry(flog,"Executing cmd:"+cmd)

ferror=open(DIR+"/log/errors.log","a")
popen=subprocess.Popen(shlex.split(cmd),close_fds=True,stdout=ferror,stderr=subprocess.STDOUT)
time.sleep(1)
exec(commands.getoutput("cat %s/sessions/%s/port"%(DIR,sessionid)),globals())
port=int(CONF["port"])
print callback+"""({"pid":"%s","port":%d,"client":"%s"})"""%(popen.pid,port,client)

