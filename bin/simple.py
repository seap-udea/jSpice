import numpy as np
from spiceypy import wrapper as spy

# ##################################################
# KERNELS
# ##################################################
spy.furnsh("kernels/default/de431_part-1.bsp")
spy.furnsh("kernels/default/de431_part-2.bsp")
spy.furnsh("kernels/default/naif0012.tls")
spy.furnsh("kernels/default/pck00010.tpc")
spy.furnsh("kernels/default/earth_070425_370426_predict.bpc")
spy.furnsh("kernels/default/earth_latest_high_prec.bpc")
spy.furnsh("kernels/default/earth_true_epoch.tk")

# ##################################################
# CONSTANTS
# ##################################################
RAD=180/np.pi
DEG=1/RAD
radii=np.zeros(3)
n,radii=spy.bodvrd("EARTH","RADII",3)
RE=radii[0]
RP=radii[2]
FE=(RE-RP)/RE

# ##################################################
# LOCATION AND TIME
# ##################################################
lat=+38.0 #deg
lon=-90.0 #def
alt=1000.0 #meters
t=spy.str2et('08/22/2017 00:00:000 UTC')

# ##################################################
# TRANSFORMATION MATRICES
# ##################################################
ITRF93toEJ2000=spy.pxform("ITRF93","ECLIPJ2000",t)
EJ2000toJ2000=spy.pxform("ECLIPJ2000","J2000",t)
J2000toEpoch=spy.pxform("J2000","EARTHTRUEEPOCH",t)

# ##################################################
# LOCATION OF THE OBSERVER AND EARTH
# ##################################################
obsITRF93=spy.georec(lon*DEG,lat*DEG,alt/1000.0,RE,FE)
earthSSBEJ2000,ltmp=spy.spkezr("EARTH",t,"ECLIPJ2000","NONE","SOLAR SYSTEM BARYCENTER")

# ##################################################
# LOCATION OF OBSERVER WITH RESPECT TO EJ2000
# ##################################################
obsEJ2000=spy.mxv(ITRF93toEJ2000,obsITRF93)
obsSSBEJ2000=spy.vadd(earthSSBEJ2000[:3],obsEJ2000)

# ##################################################
# LOCATION OF THE MOON RESPECT OBSERVER IN EJ2000
# ##################################################
body="MOON"
lt=1;ltold=0
while np.abs((lt-ltold)/lt)>=1e-10:
    ltold=lt
    bodySSBEJ2000,ltmp=spy.spkezr(body,t-lt,"ECLIPJ2000","NONE",
                                  "SOLAR SYSTEM BARYCENTER")
    bodyTOPOEJ2000=spy.vsub(bodySSBEJ2000[:3],obsSSBEJ2000[:3])
    lt=spy.vnorm(bodyTOPOEJ2000)/spy.clight()

# ##################################################
# LOCATION OF THE MOON RESPECT OBSERVER IN J2000
# ##################################################
bodyTOPOJ2000=spy.mxv(EJ2000toJ2000,bodyTOPOEJ2000)

# ##################################################
# COORDINATES IN J2000
# ##################################################
d,RAJ2000,DECJ2000=spy.recrad(bodyTOPOJ2000)
print "Equatorial coordinates in J2000:"
print "RA = ",RAJ2000*RAD
print "DEC = ",DECJ2000*RAD

# ##################################################
# COORDINATES AT THE EPOCH
# ##################################################
bodyTOPOEP=spy.mxv(J2000toEpoch,bodyTOPOJ2000)
d,RAEP,DECEP=spy.recrad(bodyTOPOEP)
print "Equatorial coordinates for the Epoch:"
print "RA = ",RAEP*RAD
print "DEC = ",DECEP*RAD
