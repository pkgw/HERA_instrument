import numpy as np
import matplotlib.pyplot as plt

h127=np.load('h127drift_mod_0.158.npz')
h19=np.load('h19.drift_mod_0.158.npz')
h350=np.load('h350drift_mod_0.158.npz')
h37=np.load('h37drift_mod_0.158.npz')
lofar=np.load('lofar_coredrift_mod_0.158.npz')
mwa=np.load('mwa128drift_mod_0.158.npz')
paper=np.load('paper128drift_mod_0.158.npz')
h331=np.load('h331drift_mod_0.158.npz')

D_lofar = 30.75
D_hera = 14.0
D_mwa = 2.32*2.
D_paper = 1.18*2.

#plt.figure('T_errs')
#plt.semilogy(h127['ks'],h127['T_errs'],label='h127')
#plt.semilogy(h19['ks'],h19['T_errs'],label='h19')
#plt.semilogy(h37['ks'],h37['T_errs'],label='h37')
#plt.semilogy(h350['ks'],h350['T_errs'],label='h350')
#plt.semilogy(lofar['ks'],lofar['T_errs'],label='lofar')
#plt.semilogy(mwa['ks'],mwa['T_errs'],label='mwa')
#plt.semilogy(paper['ks'],paper['T_errs'],label='paper')

def plotPwr(p=2,title='-',ylabel='-'):
    N37_19    = (D_hera/D_hera)**p*(h19['T_errs']/h37['T_errs'])
    N127_19   = (D_hera/D_hera)**p*(h19['T_errs']/h127['T_errs'])
    N331_19   = (D_hera/D_hera)**p*(h19['T_errs']/h331['T_errs'])
    N350_19   = (D_hera/D_hera)**p*(h19['T_errs']/h350['T_errs'])
    Nmwa_19   = (D_hera/D_mwa)**p*(h19['T_errs']/mwa['T_errs'])
    Nlofar_19 = (D_hera/D_lofar)**p*(h19['T_errs']/lofar['T_errs'])
    Npaper_19 = (D_hera/D_paper)**p*(h19['T_errs']/paper['T_errs'])
    
    clr = ['b','r','g','k','c','m','g']
    yshift = [1.35,0.8,0.8,0.76,1.12,1.17,0.72]
    if p==2:
	lbl = ['Hex-37','Hex-127','Hex-split350','Imaging-128','Imaging-48','Grid-128','Hex-331']
    else:
        lbl = ['HERA-37','HERA-127','HERA-350','MWA-128','LOFAR-Core','PAPER-128','HERA-331'] 
    plt.figure(p+1)
    i=0
    plt.loglog(h19['ks'],N37_19,label='37/19',color=clr[i],lw=2)
    plt.text(h19['ks'][1],N37_19[1]*yshift[i],lbl[i],color=clr[i])
    i=1
    plt.loglog(h19['ks'],N127_19,label='127/19',color=clr[i],lw=2)
    plt.text(h19['ks'][2],N127_19[2]*yshift[i],lbl[i],color=clr[i])
    if p==0:
        i=2
        plt.loglog(h19['ks'],N350_19,label='350/19',color=clr[i],lw=2)
        plt.text(h19['ks'][5],N350_19[5]*yshift[i],lbl[i],color=clr[i])
    i=3
    plt.loglog(h19['ks'],Nmwa_19,label='mwa/19',color=clr[i],lw=2)
    plt.text(h19['ks'][7],Nmwa_19[7]*yshift[i],lbl[i],color=clr[i])
    i=4
    plt.loglog(h19['ks'],Nlofar_19,label='lofar/19',color=clr[i],lw=2)
    plt.text(h19['ks'][9],Nlofar_19[9]*yshift[i],lbl[i],color=clr[i])
    i=5
    plt.loglog(h19['ks'],Npaper_19,label='paper/19',color=clr[i],lw=2)
    plt.text(h19['ks'][2]*0.85,Npaper_19[2]*yshift[i],lbl[i],color=clr[i])
    if p==2:
        i=6
        plt.loglog(h19['ks'],N331_19,label='331/19',color=clr[i],lw=2)
        plt.text(h19['ks'][11],N331_19[11]*yshift[i],lbl[i],color=clr[i])
    
    plt.loglog([h19['ks'][0],h19['ks'][-1]],[1.0,1.0],'k--')
    plt.title(title)
    plt.xlabel('k [h/Mpc]',fontsize=14)
    plt.ylabel(ylabel,fontsize=14)
    plt.axis(xmin=0.12,xmax=1.5)
    #plt.legend()

plotPwr(0,'Sensitivity Ratio',r'$\Delta_{19}^2/\Delta_x^2$')
#plotPwr(1)
plotPwr(2,'Redundancy Boost Ratio',r'$\mathcal{N}_{19}/\mathcal{N}_{x}$')