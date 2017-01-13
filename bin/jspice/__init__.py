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
import sys,os,inspect,zmq,cgi,glob,signal,commands
from functools import update_wrapper

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#USEFUL MODULES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import datetime

#############################################################
#MACROS
#############################################################
argv=sys.argv
stderr=sys.stderr
stdout=sys.stdout
exit=sys.exit

#############################################################
#UTIL ROUTINES
#############################################################
def loadConf(path):
    conf=dict()
    execfile(path+"/server.cfg",{},conf)
    return conf

def logEntry(flog,entry,instance="root"):
    time=datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
    log="[%s] [%s] %s\n"%(time,instance,entry)
    flog.write(log)
    flog.flush()
    #print>>stderr,log,

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
