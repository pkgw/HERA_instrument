import matplotlib.pyplot as plt
import numpy as np

kperp = np.logspace(-3,-1,100)
kperp = np.linspace(0,.1,100)
kzero = np.zeros(len(kperp))
kflat = np.ones(len(kperp))*0.06
#plt.plot(kperp,kflat)
plt.fill_between(kperp,kzero,kflat,color='k',alpha='0.5')

khoriz = 7.5*kperp
g = np.where(khoriz < max(kflat))
khoriz[g] = max(kflat)
#plt.plot(kperp,khoriz)
plt.fill_between(kperp,kflat,khoriz,color='b',alpha='0.5')
#1ksys = khoriz + 0.05 + 1.1e-3/(kperp+1e-4)
#1ksys[g] = ksys[g[0][-1]+1]*np.ones(len(g[0]))
#2ksys = 4.1*(kperp+0.00) + 0.15
x = [0.0,0.01,0.09]
y = [0.15, 0.18, 0.50]
#x = [-2.,1.,2.]
#y = [7.,10.,27.]
num = (y[2]-y[0]) - (y[1]-y[0])*(x[2]**2-x[0]**2)/(x[1]**2-x[0]**2)
den = (x[2]-x[0]) - (x[1]-x[0])*(x[2]**2-x[0]**2)/(x[1]**2-x[0]**2)
B = num/den
A = (y[1]-y[0] - B*(x[1]-x[0]))/(x[1]**2-x[0]**2)
C = y[0] - A*x[0]**2 - B*x[0]
print 'A,B,C'
print A,B,C
ksys = A*kperp**2 + B*kperp + C  ###Curved
ksys = 8.5*kperp + 0.08 ###Straight
#plt.plot(kperp,ksys,'r--')
plt.fill_between(kperp,khoriz,ksys,color='r',alpha='0.2')
plt.axis([0.0,0.1,.0,1])#.55])
plt.xlabel(r'k$_\perp [h$/Mpc]',fontsize=14)
plt.ylabel(r'k$_{||} [h$/Mpc]',fontsize=14)

useCables = False
if useCables:
    kperp_cables = [0,0.085]
    kpam = 0.45
    kpar_cables1 = [kpam,kpam]
    plt.plot(kperp_cables,kpar_cables1,'r--')
    kpam = 0.465
    kpar_cables2 = [kpam,kpam]
    plt.plot(kperp_cables,kpar_cables2,'r--')
    plt.fill_between(kperp_cables,kpar_cables1,kpar_cables2,color='r',alpha='0.2')



