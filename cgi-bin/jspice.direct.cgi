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
from jspice.core import *

#############################################################
#CANCEL BEHAVIOR
#############################################################
def sigHandler(signal,frame):
    import sys
    logEntry(flog,"Terminating direct")
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
callback=getArg("callback","json",params=params)
sessionid=getArg("sessionid","0"*20,params=params)

sessdir="%s/sessions/%s/"%(DIR,sessionid)
if not os.path.isdir(sessdir):sessdir=DIR+"/log"
flog=open(sessdir+"/direct.log","a")
logEntry(flog,"Direct invoked",sessionid)
logEntry(flog,"Proxy commands:\n\tCallback:%s\n\tCode:\n\t%s"%(callback,code),sessionid)

#############################################################
#LOAD SPICE KERNELS
#############################################################
kernels=glob.glob(DIR+"/"+CONF["kernels_dir"]+"/*")
logEntry(flog,"Loading kernels:"+"{}".format(kernels),sessionid)
for kernel in kernels:
    spy.furnsh(kernel)
logEntry(flog,"SPICE kernels load",sessionid)

#############################################################
#EXECUTION
#############################################################
def run():

    global code
    try:
        exec(code)
        logEntry(flog,"Command succesfully executed.",sessionid)
    except Exception as e:
        logEntry(flog,"Error:\n\t"+str(e))

    #############################################################
    #OUTPUT
    #############################################################
    response=stringifyDictionary(locals())
    code=code.replace("\n","").replace("\t","")
    print callback+"""({"code":"%s","configuration":"%s","response":"%s"})"""%\
        (code,"{}".format(CONF),response.replace("\"","\\\""))

run()
