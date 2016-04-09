import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import sys, os, os.path
basedir = os.getenv('UBDIR')
sys.path.append(os.path.join(basedir,'Code/Lib'))
import fitlib
c = 3.0E8

def d2tau(d,fd=0.32):
    return 2.0*fd*d/c*1E9  # m to ns
def tau2d(tau,fd=0.32):
    return c*(tau/1E9)/(2*fd)  # ns to m

xlh = [6.5,26]
d331 = 5.551
delayLimSpec = 60.0
delay2LimDiam = tau2d(delayLimSpec/2.0)
delayLimPlt = np.array([[xlh[0],delayLimSpec],[xlh[1],delayLimSpec]])
delayDiamPlt = np.array([[delay2LimDiam,0.0],[delay2LimDiam,delayLimSpec]])

d = np.loadtxt('costfig_summary_newscale.dat')
cp = d[:,2]/d331
diam = d[:,1]
delay = d2tau(d[:,1])

###First version
fg1 = plt.figure(1)
ax1 = fg1.add_subplot(111)
ax2 = ax1.twinx()
ax2.plot(d[:,1],delay,linestyle='--',color='r')
ax2.plot(d[:,1],delay*2,linestyle='--',color='r')
ax2.plot(d[:,1],delay*3,linestyle='--',color='r')
ax2.plot(delayLimPlt[:,0],delayLimPlt[:,1],linestyle='--',color='k')
ax2.plot(delayDiamPlt[:,0],delayDiamPlt[:,1],linestyle=':',color='k')
ax2.text(19,d2tau(19.0+1.0),'1',fontsize=14)
ax2.text(17,d2tau(2.0*17.0+1.0),'2',fontsize=14)
ax2.text(14,d2tau(3.0*14.0+1.0),'3',fontsize=14)
ax2.set_ylabel('Delay [ns] (dashed)',fontsize=14)
ax2.set_ylim( (0,120) )

ax1.plot(d[:,1],cp,color='b',lw=3)
ax1.plot(d[:,1],cp,color='g',marker='o')
ax1.plot([14.0],1.0,'o',markersize=8,color='r')
ax1.set_ylabel('Cost/Performance (solid)',fontsize=14)
ax1.set_xlim( xlh )

ax1.set_xlabel('Diameter [m]',fontsize=14)
plt.show()

###Smooth version
pxmin = 6.0
pxmax = 25.0
xr = np.arange(5.5,25,0.1)
plt.figure(10)
plt.subplot(122)
f = interpolate.interp1d(diam,cp,kind=3,bounds_error=False,fill_value=2000)
yr_cost = f(xr)
xr_cost = xr
plt.plot(xr,yr_cost,label='HERA',linewidth=4)
plt.ylabel('Cost/Performance',fontsize=14)
plt.xlabel('Diameter [m]',fontsize=14)
#plt.plot(diam,cp,'o')
#plt.axis([5,25,.9,1.7])
#a = fitlib.fit(diam,cp,9)
#add old version onto it for memo
d331_m = 5.520
d_m = np.loadtxt('costfig_summary_mellema.dat')
cp_m = d_m[:,2]/d331_m
diam_m = d_m[:,1]
f = interpolate.interp1d(diam_m,cp_m,kind=3,bounds_error=False,fill_value=2000)
yr = f(xr)
plt.plot(xr,yr,'--',label='Mellema et al')
plt.grid()
plt.legend()
plt.axis([pxmin,pxmax,0,2])
plt.plot([14.0],[1.0],'o',markersize=8,color='r')

###N vs D curves
#plt.figure(11)
plt.subplot(121)
f = interpolate.interp1d(diam,d[:,0],kind=3,bounds_error=False,fill_value=2000)
yr = f(xr)
plt.plot(xr,yr,label='HERA',linewidth=4)
f = interpolate.interp1d(diam_m,d_m[:,0],kind=3,bounds_error=False,fill_value=2000)
yr = f(xr)
plt.plot(xr,yr,'--',label='Mellema et al')
plt.grid()
plt.legend()
plt.xlabel('Diameter [m]',fontsize=14)
plt.ylabel('# at fixed performance',fontsize=14)
plt.axis([pxmin,pxmax,0,1000])
plt.plot([14.0],[331.0],'o',markersize=8,color='r')

###Just a look
plt.figure(2)
plt.plot(delay,d[:,2])
plt.plot(delay*2,d[:,2])
plt.plot(delay*3,d[:,2])

###Using this one...
plt.figure(3)
plt.plot([14,14],[0,60],linestyle='--',color='w',lw=3)
plt.plot(d[:,1],delay,linestyle='--',color='k',lw=3)
plt.plot(d[:,1],delay*2,linestyle='-',color='k',lw=3)
plt.plot(d[:,1],delay*3,linestyle='--',color='k',lw=3)
#plt.plot(xr_cost,(yr_cost-.9)*100.,color='w',lw=2)

plt.xlabel('Diameter [m]',fontsize=14)
plt.ylabel('Round-trip Delay [ns]',fontsize=14)

costimsize = [7,30,0,85]
costim = np.zeros((costimsize[3]-costimsize[2],costimsize[1]-costimsize[0]))

fc = interpolate.interp1d(np.flipud(d[:,1]),np.flipud(cp))
mult = 1.0
uselog=False
clip=1.25*mult
#clip = max(cp)*mult
if uselog:
    clip=np.log(clip)
for i in range(costim.shape[1]):
    diam = 7.0+i
    cv = fc(diam)*mult
    if uselog:
        cv = np.log(cv)
    if cv>clip:
        cv=clip
    jtrans = 0
    for j in range(costim.shape[0]):
        if float(j) > 0.9*delayLimSpec:
            cvadd = jtrans**(1.5)/100.0
            jtrans+=1
        else:
            cvadd = 0.0
        cvsum = cv+cvadd
        if cvsum>clip:
            cvsum = clip
        costim[j,i] = cvsum
usecmap = 'gist_yarg'
usecmap = 'Spectral'
usecmap = 'rainbow'
plt.imshow(costim,origin='lower',aspect='auto',extent=costimsize,cmap=usecmap)
plt.colorbar()
plt.axis(xmax=25,ymax=85)
plt.text(19,d2tau(19.0+1.0),'1',fontsize=15)
plt.text(15,d2tau(2.0*15.0-1.2),'2',fontsize=14,color='k')
plt.text(10,d2tau(3.0*10.0-1.8),'3',fontsize=14,color='k')
