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
#Function: jSpice basic python routines
#############################################################

#############################################################
#EXTERNAL MODULES
#############################################################

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#SENSIBLE MODULES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import sys,os,inspect,zmq,cgi,glob,signal
import commands,json,shlex,subprocess,time,jsonpickle
import sqlite3 as sqlite
from functools import update_wrapper

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#USEFUL MODULES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import datetime

#############################################################
#MACROS AND GLOBAL VARIABLES
#############################################################
#Macros
argv=sys.argv
stderr=sys.stderr
stdout=sys.stdout
exit=sys.exit

#Globals
CONF={}
DB=None
CON=None
SIGNALS=[signal.SIGABRT,signal.SIGFPE,signal.SIGILL,
         signal.SIGINT,signal.SIGSEGV,signal.SIGTERM]
MIN=60.0
HOUR=60*MIN
DAY=24*HOUR
YEAR=365.25*DAY

#############################################################
#UTIL ROUTINES
#############################################################
def jsonpCallback(parameters):
    global CONF
    CONF.update(parameters)

def loadConf(filecfg):
    conf=dict()
    execfile(filecfg,globals(),conf)
    return conf

def logEntry(flog,entry,instance="root"):
    """
    time=datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
    log="[%s] [%s] %s\n"%(time,instance,entry)
    flog.write(log)
    flog.flush()
    #print>>stderr,log,
    #"""

def logEntryClean(flog,entry,instance="root"):
    pass

def termProcess():
    #os.kill(os.getpid(), signal.SIGTERM)
    os.kill(os.getpid(), signal.SIGTERM)
    
class Socket(zmq.Socket):

    default_timeout=100
    
    def __init__(self, ctx, type, default_timeout=None):
        zmq.Socket.__init__(self, ctx, type)
        self.default_timeout = default_timeout

    def on_timeout(self):
        termProcess()
        return None

    def _timeout_wrapper(f):
        def wrapper(self, *args, **kwargs):
            timeout = kwargs.pop('timeout', self.default_timeout)
            if timeout is not None:
                timeout = int(timeout * 1000)
                poller = zmq.Poller()
                poller.register(self)
                if not poller.poll(timeout):
                    return self.on_timeout()
            return f(self, *args, **kwargs)
        return update_wrapper(wrapper, f, ('__name__', '__doc__'))

    for _meth in dir(zmq.Socket):
        if _meth.startswith(('send', 'recv')):
            locals()[_meth] = _timeout_wrapper(getattr(zmq.Socket, _meth))

    del _meth, _timeout_wrapper

OPTIONS=None
def getArg(option,default=None,params=None):

    if not params is None:
        value=params.getvalue(option)
        if not (value is None):return value

    global OPTIONS
    if OPTIONS is None:
        OPTIONS={}
        for i in xrange(1,len(argv[1:])+1):
            opts=argv[i]
            if "=" in opts:
                parts=opts.split("=")
                opt=parts[0]
                val=parts[1:]
                if type(val)==list:val="=".join(val)
            else:
                opt=opts
                val=True
            OPTIONS[opt]=val

    if not (option in OPTIONS.keys()):
        if default is None:
            OPTIONS[option]=False
        else:
            OPTIONS[option]=default

    return OPTIONS[option]

def checkArgs():
    qerror=False
    for arg in OPTIONS.keys():
        if not OPTIONS[arg]:
            print "Missing argument %s"%arg
            qerror=True
    return qerror

class dict2obj(object):
    def __init__(self,dic={}):self.__dict__.update(dic)
    def __add__(self,other):
        for attr in other.__dict__.keys():
            exec("self.%s=other.%s"%(attr,attr))
        return self

def sqlExec(sql,dbfile):
    global CON,DB
    if DB is None:
        CON=sqlite.connect(dbfile)
        DB=CON.cursor()
    DB.execute(sql)
    CON.commit()
    rows=DB.fetchall()
    return rows

def registerSession(session,dbfile):
    fields=""
    values=""
    for key in session.keys():
        fields+=key+","
        values+="'%s',"%(str(session[key]))
    fields=fields.strip(",")
    values=values.strip(",")
    sqlExec("insert or replace into sessions (%s) values (%s)"%(fields,values),dbfile)

def unregisterSession(sessionid,sessdir,dbfile):
    out=sqlExec("select timestart,pid,port,proxy,client from sessions where sessionid='%s'"%sessionid,dbfile)
    timestart=int(out[0][0])
    pid=out[0][1]
    port=out[0][2]
    proxy=out[0][3]
    client=out[0][4]
    timeend=int(time.mktime(datetime.datetime.now().timetuple()))
    timelife=timeend-timestart
    vmsize=commands.getoutput("cat /proc/%s/status |grep VmRSS"%pid)
    ncom=commands.getoutput("grep 'Command received' %s/sessions/%s/session.log |wc -l"%(sessdir,sessionid))
    mem=vmsize.split()[1]
    sqlExec("insert into statistics (sessionid,port,timelife,ncommands,memory,proxy,client) values ('%s','%s','%s','%s','%s','%s','%s')"%(str(sessionid),str(port),str(timelife),str(ncom),str(mem),str(proxy),str(client)),dbfile)
    sqlExec("delete from sessions where sessionid='%s'"%sessionid,dbfile)
    
def encodeLocals(local):
    r=dict()
    for key in local.keys():
        r[key]=str(local[key]).replace("'",'\\"')
    final="{}".format(r)
    return final

def stringifyDictionary(dictionary):
    d={k:repr(v).replace("'",'') for k,v in dictionary.items()}
    return "{}".format(d)

def getTime():
    unixt=time.mktime(datetime.datetime.now().timetuple())    
    return unixt
