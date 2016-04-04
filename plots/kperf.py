import sys
sys.path.append('/Users/ddeboer/Documents/ubase/Code/cosmo')
import nedclass
import matplotlib.pyplot as plt
import math
import numpy as np

n = nedclass.ned(H0=100.0)

def get_dz(z,B,rest=1420.):
    return B*(1+z)**2/rest

def mkPlot(restFreq,BW,b,coeff):
    X = []  # X Mpc/rad
    Xb = [] # scaled version
    Xinstr = []  # observed extent in Mpc
    Y = []  # Y Mpc/GHz
    DA = [] # angular scale term
    E = []  # Hubble parameter evolution
    #Below are just used to get a power-law fit and then plot it post facto
    apX = []    # approximated X (post-fit numbers put back in)
    apY = []    # approximated Y ( " )
    z2fit = []  # range of z's to fit for approximation
    X2fit = []  #     "    X's   "
    Y2fit = []  #     "    Y's   "

    # Loop over red-shift
    z = np.arange(0.1,25.0,.1)
    for zi in z:
        DAi = n.calcUniverse(zi)
        DA.append(DAi)
        Xi = DAi*(1.+zi)
        obsFreq = restFreq/(1.+zi)
        obsWavelength = 0.3/obsFreq
        Xbi = Xi/((180.0/math.pi)*1.0)  #convert to degrees
        X.append(Xi)
        Xb.append(Xbi)
        Xbi = Xi*coeff*obsWavelength/b
        Xinstr.append(Xbi)
        apX.append(4670.*pow(1.+zi,0.312))
        E.append(n.Ez)
        Yi = ( n.Ynu )/restFreq
        Y.append(Yi)
        apY.append(64.*pow(1.+zi,0.56))
        if zi > 6.0 and zi < 9.0:
            z2fit.append(zi)
            X2fit.append(Xi)
            Y2fit.append(Yi)
    Y = np.array(Y)
    Xinstr = np.array(Xinstr)
    kperp = 2.0*np.pi/Xinstr
    kpar = 2.0*np.pi/(BW*Y)
    ktot = np.sqrt(2.0*kperp**2 + kpar**2)
    return z,kperp,kpar,ktot

restFreq = 1.42
coeff = 1.2

###Make plot
#zeroth part
zhera = [6,13]
khera1 = [.14,.14]
plt.semilogy(zhera,khera1,'w')
khera2 = [20,20]
plt.semilogy(zhera,khera2,'w') 
plt.fill_between(zhera,khera1,khera2,color='w',alpha='0.65')

#first part (k_tot)
BW_list = [0.02,.002]
D_list = [14.6,25.3]
#txtloc = [[9,.02,-4],[7,.32,-5]]  #wide
txtloc = [[9.3,.02,-7],[6.0,.34,-10]]  #narrow
lsc = ['g-','g-']
tclr = ['g','g']
for i,BW in enumerate(BW_list):
    z,kperp,kper,ktot = mkPlot(restFreq,BW,D_list[i],coeff)
    if i==0:
        savek = ktot
    show_label='%.0f MHz, %.1fm' % (1000.*BW,D_list[i])
    lbl = r'${\bf |k|}$ @%s' % (show_label)
    plt.semilogy(z,ktot,lsc[i],label=show_label,lw=2) 
    plt.text(txtloc[i][0],txtloc[i][1],lbl,rotation=txtloc[i][2],color=tclr[i],fontsize=16)
ktottop = 10.*np.ones(len(z))
plt.fill_between(z,savek,ktottop,color='g',alpha='0.25')
plt.fill_between(zhera,khera1,khera2,color='w',alpha='0.65')  ###AND REDO LINE 63

#second part  (k_perp)
BW = 0.01
D_list = [14.60,300.0]
lsc = ['k-','k-']
#txtloc = [[6,9.8e-3,-17],[13.2,.085,-8]]  #wide
txtloc = [[6,9.8e-3,-24],[13.2,.085,-14]]  #narrow
for i,D in enumerate(D_list):
    show_label = '%.1fm' % (D)
    z,kperp,kpar,ktot = mkPlot(restFreq,BW,D,coeff)
    lbl = r'$k_{\perp}$ @%s' % (show_label)
    plt.semilogy(z,kperp,lsc[i],label=lbl,linewidth=3)
    plt.text(txtloc[i][0],txtloc[i][1],lbl,rotation=txtloc[i][2],color='k',fontsize=16)
#plt.fill_between(z,p[0],p[1],color='grey',alpha='0.65')


#third part  (k_par)
D = 14.6
BW_list = [0.1,0.01,.001]
lsc = ['b--','b-','b-']
txtloc = [[6.0,4.6e-3,-9],[6,.07,-11],[15.3,.475,-5]]
BW_show = ['100MHz','10MHz', '1MHz']
for i,BW in enumerate(BW_list):
    show_label = BW_show[i]
    z,kperp,kpar,ktot = mkPlot(restFreq,BW,D,coeff)
    lbl = r'$k_{||}$ @%s' % (show_label)
    plt.semilogy(z,kpar,lsc[i],label=lbl,linewidth=3)
    plt.text(txtloc[i][0],txtloc[i][1],lbl,rotation=txtloc[i][2],color='b',fontsize=16)
#plt.fill_between(z,p[0],p[1],color='b',alpha='0.25')

#fourth part (redshift bins)
z_list = [6.,12.,18.]
for z in z_list:
    for BW in BW_list:
        zback,kperp,kpar,ktot = mkPlot(restFreq,BW,D,coeff)
        y = 0.9*kpar[int(np.where(zback>0.99*z)[0][0])]
        dz = get_dz(z,BW,restFreq)
        if BW<0.02:
	    plotit=True
	elif z>11. and z<13.:
	    y = 0.9*y
	    plotit = True
	else:
	    plotit = False
	if plotit:
            plt.plot([z-dz/2.,z+dz/2.],[y,y],'b',lw=2)
            plt.plot([z-dz/2.,z-dz/2.],[0.9*y,1.1*y],'b',lw=2)
            plt.plot([z+dz/2.,z+dz/2.],[0.9*y,1.1*y],'b',lw=2)


plt.xlabel('Redshift [z]',fontsize=16)
plt.ylabel('k(res) [h/Mpc]',fontsize=16)
#plt.legend(loc='upper right')
plt.grid()
plt.axis([restFreq/0.220 - 1.0,restFreq/0.065-1.0,2e-3,1])
