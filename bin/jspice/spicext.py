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
#Function: an axtension to SpiceyPy
#############################################################
from spiceypy import wrapper as spy

#############################################################
#EXTERNAL MODULES
#############################################################
import time,datetime
import numpy as np
np.set_printoptions(threshold='nan')	

#############################################################
#EXTEND SPICE
#############################################################
"""

This routines are intended to extend SPICE and include new
functionalities.

Convention:
    def _<jroutine>(*args): Private routine
    spy.j<routine>: Extended routine

Use in your code instead of:

    from spiceypy import wrapper as spy

This code:

    from spicext import *

SpiceyPy and Spicext can be invoked as:

    spy.<routine>
    spy.j<routine>
"""

def _utcnow():
    utc=datetime.datetime.utcnow()
    now=utc.strftime("%m/%d/%y %H:%M:%S.%f UTC")
    return now
spy.jutcnow=_utcnow

def _locnow():
    loc=datetime.datetime.now()
    now=loc.strftime("%m/%d/%y %H:%M:%S.%f")
    return now
spy.jlocnow=_locnow

def _etnow():
    return spy.str2et(spy.jlocnow())
spy.jetnow=_etnow

def _et2str(et):
    deltet=spy.deltet(et,"ET")
    cal=spy.etcal(et-deltet,100)
    return cal
spy.jet2str=_et2str

def _dec2sex(dec,sep=None,day=False):
    if day:fac=24
    else:fac=60
    H=np.floor(dec)
    mm=(dec-H)*fac
    M=np.floor(mm)
    ss=(mm-M)*60;
    S=np.floor(ss);
    if not sep is None:
        return "%02d%s%02d%s%02.3f"%(int(H),sep[0],int(M),sep[1],ss)
    return [H,M,ss]
spy.jdec2sex=_dec2sex

def _rad():return 180/np.pi
spy.jrad=_rad

def _deg():return np.pi/180
spy.jdeg=_deg

