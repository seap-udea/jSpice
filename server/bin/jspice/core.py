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
#Function: jSpice core routines
#############################################################

#############################################################
#EXTERNAL MODULES
#############################################################

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#BASIC
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#It includes: os, sys, inspect
from jspice import *

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#BASIC
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
from spiceypy import wrapper as spy

#############################################################
#EXTEND SPICE
#############################################################
"""

This routines are intended to extend SPICE and include new
functionalities.

Convention:
    def _jroutine(*args): Private routine
    spy.jroutine: Extended routine

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
