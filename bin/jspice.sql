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
#EXTERNAL MODULES
#############################################################
import sys,os,inspect
PATH=os.path.realpath(
    os.path.abspath(os.path.split(
        inspect.getfile(
            inspect.currentframe()))[0]))
DIR=PATH+"/.."
sys.path.insert(0,DIR+"/bin")
from jspice import *

#############################################################
#LOG FILE
#############################################################
flog=open(DIR+"/log/database.log","a")

#############################################################
#CANCEL BEHAVIOR
#############################################################
def sigHandler(signal,frame):
    import sys
    logEntry(flog,"Terminating test")
    sys.exit(0)
signal.signal(signal.SIGINT,sigHandler)

#############################################################
#EXTERNAL MODULES
#############################################################
loadConf(DIR+"/jspice.cfg")

#############################################################
#PARAMETERS
#############################################################
action=getArg("action")
checkArgs()

#############################################################
#CONNECT
#############################################################
connect=sqlite.connect("sessions.db")
with connect:
    db=connect.cursor()

    if action=="reset":
        logEntry(flog,"Creating tables","create")
        print "Creating tables..."
        
        #Sessions table
        db.execute("drop table if exists sessions")
        db.execute("""
        create table sessions(
        sessionid varchar(20),
        port varchar(6),
        timestart varchar(50),
        pid varchar(6),
        proxy varchar(50),
        client varchar(50),
        primary key (sessionid)
        );
        """)

        #Statistics table
        db.execute("drop table if exists statistics")
        db.execute("""
        create table statistics(
        sessionid varchar(20),
        port varchar(6),
        proxy varchar(50),
        client varchar(50),
        timelife varchar(50),
        ncommands varchar(10),
        memory varchar(10)
        );
        """)
