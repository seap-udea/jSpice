# Observer
obs=spy.jobsini('EARTH',[[lon]],[[lat]],0.0)
lat=[[lat]]
# Routines
def angDist(t,obs):
    return spy.jangdis('MOON','SUN',t,obs)
def contactFunction(t,obs,k):
    return spy.jangdis('MOON','SUN',t,obs,k=k)
# Maximum time
t1=spy.str2et('08/21/2017 00:00:00 UTC')
t2=spy.str2et('08/21/2017 23:59:59 UTC')
tecl=spy.jminim(angDist,(t1,t2),method='brent',args=(obs,),tol=1e-13).x
cal_max=spy.timout(tecl,'MM/DD/YYYY HR:MN:SC.###### UTC',100)
# Ephemeris of the sun at teclipse
mat=spy.jrotmat(tecl)
ephem_sun=spy.jephem('SUN',tecl,obs,mat)
# Contact times
tc1=spy.jzero(contactFunction,t1,tecl,args=(obs,+1))
cal_c1=spy.timout(tc1,'MM/DD/YYYY HR:MN:SC.###### UTC',100)
try:
    tc2=spy.jzero(contactFunction,t1,tecl,args=(obs,-1))
    cal_c2=spy.timout(tc2,'MM/DD/YYYY HR:MN:SC.###### UTC',100)
except:cal_c2='';
try:
    tc3=spy.jzero(contactFunction,tecl,t2,args=(obs,-1))
    cal_c3=spy.timout(tc3,'MM/DD/YYYY HR:MN:SC.###### UTC',100)
except:cal_c3='';
tc4=spy.jzero(contactFunction,tecl,t2,args=(obs,+1))
cal_c4=spy.timout(tc4,'MM/DD/YYYY HR:MN:SC.###### UTC',100)

