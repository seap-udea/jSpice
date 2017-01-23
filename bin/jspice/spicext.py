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
import spiceypy.support_types as spytypes
#############################################################
#EXTERNAL MODULES
#############################################################
import time,datetime
import numpy as np
from scipy.optimize import brentq as _zero
from scipy.optimize import minimize_scalar as _minim
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

#############################################################
#CONSTANTS
#############################################################
spy.IDENTITY=np.identity(3)
spy.RAD=180/np.pi
spy.DEG=1/spy.RAD

#############################################################
#ROUTINES
#############################################################
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
    sgn=np.sign(dec)
    dec=np.abs(dec)
    H=np.floor(dec)
    mm=(dec-H)*fac
    M=np.floor(mm)
    ss=(mm-M)*60;
    S=np.floor(ss);
    H=sgn*H
    if not sep is None:
        return "%02d%s%02d%s%02.3f"%(int(H),sep[0],int(M),sep[1],ss)
    return [H,M,ss]
spy.jdec2sex=_dec2sex

def _rad():return 180/np.pi
spy.jrad=_rad

def _deg():return np.pi/180
spy.jdeg=_deg

def _obsini(body,lon,lat,alt):
    """
    lon: longitude in degree
    lat: latitude in degree
    alt: altitude in meters
    obs: observer dictionary:
       lat,lon (radians)
       alt (kilometers)
       pos (cartesian position with respect to ellipsoid ITRF93)
       norm (normal vector wrt ellipoid)
       radii (a, b, c, fe)
       LOCALtoITRF93, ITRF93toLOCAL (transformation matrices)
    """
    obs=dict(
        ITRF93toLOCAL=np.zeros((3,3)),
        LOCALtoITRF93=np.zeros((3,3)),
        radii=np.zeros(3),
        pos=np.zeros(3),
        norm=np.zeros(3),
    )
    obs["lon"]=lon*spy.DEG
    obs["lat"]=lat*spy.DEG
    obs["alt"]=alt/1000.0
    obs["body"]=body

    # Body properties
    n,obs["radii"]=spy.bodvrd(body,"RADII",3)
    obs["radii"]=np.append(obs["radii"],
                           [(obs["radii"][0]-obs["radii"][2])/obs["radii"][0]])
    obs["radii"]=np.append(obs["radii"],
                           [(obs["radii"][0]+obs["radii"][2])/2])
    
    # Position in the ellipsoid
    obs["pos"]=spy.georec(obs["lon"],obs["lat"],obs["alt"],
                          obs["radii"][0],obs["radii"][3])

    # Normal vector to location
    obs["norm"]=spy.surfnm(obs["radii"][0],obs["radii"][1],obs["radii"][2],obs["pos"])

    # Vectors
    uz=[0,0,1]
    uy=spy.ucrss(obs["norm"],uz)
    uz=obs["norm"]
    ux=spy.ucrss(uy,uz)

    # Matrices
    obs["ITRF93toLOCAL"]=np.array([ux,uy,uz])
    obs["LOCALtoITRF93"]=spy.invert(obs["ITRF93toLOCAL"]);

    return obs
spy.jobsini=_obsini

def _rotmat(t):
    mat=dict(
        ITRF93toEJ2000=np.zeros((3,3)),
        EJ2000toJ2000=np.zeros((3,3)),
        J2000toEpoch=np.zeros((3,3)),
        J2000toITRF93=np.zeros((3,3)),
    )
    mat["ITRF93toEJ2000"]=spy.pxform("ITRF93","ECLIPJ2000",t)
    mat["EJ2000toJ2000"]=spy.pxform("ECLIPJ2000","J2000",t)
    mat["J2000toEpoch"]=spy.pxform("J2000","EARTHTRUEEPOCH",t)
    mat["J2000toITRF93"]=spy.pxform("J2000","ITRF93",t)
    return mat
spy.jrotmat=_rotmat

def _ephem(target,t,obs,mat,depth='epoch'):
    """
    Parameters:
    body: string for target body
    t: ephemeris time
    obs: observer dictionary
    mat: rotation matrices
    
    Return:
    ephem: dictionary with ephemeris
    obsSSBEJ2000: Coordinate of the Observer wrt SSB in ELIPJ2000
    targetSSBEJ2000: Coordinate of the target wrt SSB in ECLIPJ2000
    targetSSBJ2000: Coordinate of the target wrt SSB in J2000
    targetOBSEJ2000: Coordinate of the target wrt observer in ECLIPJ2000
    targetOBSJ2000: Coordinate of the target wrt observer in J2000
    targetOBST: Coordinate of the target wrt observer at Epoch
    targetOBSITRF93: Coordinate of the target wrt observer in ITRF93
    targetOBSLOCAL: Coordinate of the target wrt observer in Local coordinates

    distance: distance from target to observer

    RA (radians): J2000
    DEC (radians): J2000

    RAt (radians): at epoch
    DECt (radians): at epoch

    az (radians): Azimuth
    el (radians): elevation

    """
    ephem=dict(
        target=target,
        targetSSBEJ2000=np.zeros([0,0,0]),
        targetOBSEJ2000=np.zeros([0,0,0]),
        targetOBSJ2000=np.zeros([0,0,0]),
        distance=0,
        RAJ2000=0,
        DECJ2000=0,
    )
    
    bodySSBEJ2000,ltmp=spy.spkezr(obs["body"],t,
                                  "ECLIPJ2000","NONE","SOLAR SYSTEM BARYCENTER")

    obsEJ2000=spy.mxv(mat["ITRF93toEJ2000"],obs["pos"])
    ephem["obsSSBEJ2000"]=spy.vadd(bodySSBEJ2000[:3],obsEJ2000)

    # Position of target corrected by light-time
    n,ephem["radii"]=spy.bodvrd(target,"RADII",3)
    ephem["radii"]=np.append(ephem["radii"],
                           [(ephem["radii"][0]-ephem["radii"][2])/ephem["radii"][0]])
    ephem["radii"]=np.append(ephem["radii"],
                           [(ephem["radii"][0]+ephem["radii"][2])/2])
    lt=1;ltold=0
    while np.abs((lt-ltold)/lt)>=1e-10:
        ltold=lt
        ephem["targetSSBEJ2000"],ltmp=spy.spkezr(target,t-lt,"ECLIPJ2000","NONE",
                                                 "SOLAR SYSTEM BARYCENTER")
        ephem["targetOBSEJ2000"]=spy.vsub(ephem["targetSSBEJ2000"][:3],
                                          ephem["obsSSBEJ2000"])
        lt=spy.vnorm(ephem["targetOBSEJ2000"])/spy.clight()

    # Ecliptic coordinates at J2000
    ephem["distance"],ephem["eclon"],ephem["eclat"]=spy.recrad(ephem["targetOBSEJ2000"])

    # Equator J2000
    ephem["targetOBSJ2000"]=spy.mxv(mat["EJ2000toJ2000"],ephem["targetOBSEJ2000"])

    # Coordinates at J2000
    ephem["distance"],ephem["RA"],ephem["DEC"]=spy.recrad(ephem["targetOBSJ2000"])
    ephem["angsize"]=2*(ephem["radii"][4]/ephem["distance"])*spy.jrad()*3600

    # Coordinates at Epoch
    ephem["targetOBST"]=spy.mxv(mat["J2000toEpoch"],ephem["targetOBSJ2000"])
    d,ephem["RAt"],ephem["DECt"]=spy.recrad(ephem["targetOBST"])

    # Topocentric coordinates
    ephem["targetOBSITRF93"]=spy.mxv(mat["J2000toITRF93"],ephem["targetOBSJ2000"])
    ephem["targetOBSLOCAL"]=spy.mxv(obs["ITRF93toLOCAL"],ephem["targetOBSITRF93"])
    udir,mag=spy.unorm(ephem["targetOBSLOCAL"])
    udir[1]*=-1
    d,az,el=spy.reclat(udir)
    if(az<0):az+=2*np.pi
    ephem["el"]=el
    ephem["z"]=np.pi/2-ephem["el"]
    ephem["az"]=az

    return ephem
spy.jephem=_ephem

# Find zeros
spy.jzero=_zero
spy.jminim=_minim

# Angular distance
def _gcdist(lam1,lam2,phi1,phi2):
  sf=np.sin((phi2-phi1)/2)
  sl=np.sin((lam2-lam1)/2)
  d=2*np.arcsin((sf*sf+np.cos(phi1)*np.cos(phi2)*sl*sl)**0.5)
  return d
spy.jgcdist=_gcdist

def _angdis(body1,body2,t,obs,k=0):
    """Calculate the angular distance of the contact-function (fk) of two
    objects as observed from observatory obs

    Parameters:
    body1: Body 1 string (largest body)
    body2: Body 2 string
    t: ephemeris time
    obs: observer dictionary
    k: k-parameter of the contact-function. k=0 (angular distance),
       k=+1 (external contact), k=-1 (internal contact)


    Returns:
    if k==0: Angular distance
    if k!=0: angdist-rad1-k*rad2
    """
    mat=spy.jrotmat(t)
    ephem1=spy.jephem(body1,t,obs,mat)
    ephem2=spy.jephem(body2,t,obs,mat)
    angdist=spy.jgcdist(ephem1["RA"],ephem2["RA"],ephem1["DEC"],ephem2["DEC"])
    if k==0:
        return angdist
    else:
        rad1=ephem1["angsize"]/2
        rad2=ephem2["angsize"]/2
        fk=angdist*spy.jrad()*3600.0-rad1-k*rad2
        return fk
spy.jangdis=_angdis
