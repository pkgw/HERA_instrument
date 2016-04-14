import numpy as np
import matplotlib.pyplot as plt
datafile = 'spec_on_foreground_reflected_power_21cmfast_14.6m_150.0_MHz_subband_v2.npz'

npzdata = np.load(datafile)
tau = npzdata['tau']
achrm = npzdata['achrmbeam']

bottom = np.zeros(len(tau))
plt.plot(tau,achrm[0],lw=2,label=r'$k_{||}>0.10$ h/Mpc')
plt.fill_between(tau,bottom,achrm[0],color='b',alpha='0.25')
plt.plot(tau,achrm[1],lw=2,label=r'$k_{||}>0.15$ h/Mpc')
plt.fill_between(tau,bottom,achrm[1],color='g',alpha='0.25')
plt.plot(tau,achrm[2],lw=2,label=r'$k_{||}>0.20$ h/Mpc')
plt.fill_between(tau,bottom,achrm[2],color='k',alpha='0.25')
t60 = [60,60,500]
a60 = [0,60,60]
a0 = [0.0,0.0,0.0]
plt.fill_between(t60,a0,a60,color='k',alpha='0.05')
plt.plot(t60,a60)
plt.axis([0,500,75,0])
plt.xlabel(r'$\tau$ [ns]')
plt.ylabel('Attenuation [dB]')
plt.legend()

delay = np.load('delay_spectrum.npz')
#plt.plot(delay['tau'],delay['dpaper'])
plt.plot(delay['tau'],-1.*delay['dhera'],'k',lw=2)
#plt.figure('aaa')
#plt.plot(delay['tau'],delay['dhera'])

plt.savefig('delayspecplot.pdf',dpi=200)