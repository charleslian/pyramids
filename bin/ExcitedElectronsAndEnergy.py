#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma



#------------------------------------------------------------------------------
fig, axs = plt.subplots(3,1,sharex=True,sharey=False,figsize=(8,6))
SaveName = __file__.split('/')[-1].split('.')[0]
c = ma.getColors(2,cmap='brg')
#------------------------------------------------------------------------------
Time, exe = dP.getExcitedElectrons()
ax = axs[0]
ax.plot(Time,exe - exe[0],'.',alpha=0.8,c='b',markerfacecolor='w',lw=2,label='Excited Electrons')
kargs=ma.getPropertyFromPosition(ylabel=r'n(e)',
                                 title='', 
                                 xlimits=None,)
ma.setProperty(ax,**kargs)
#------------------------------------------------------------------------------
ax = axs[1]
time, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure()
deltaE = (E_ks[2:] - E_ks[2]) 
deltaEt = (E_tot[2:] - E_tot[2])
#ax.plot(time[2:], deltaE,'.',c='r', lw=2, alpha=1,label='Excitation Energy')
ax.plot(time[2:], deltaEt,'.',c='g', lw=2, alpha=1,label='Excitation Energy')
kargs=ma.getPropertyFromPosition(ylabel=r'E(eV)',xlabel = r'Time(fs)',
                                 title='')
ma.setProperty(ax,**kargs)
#------------------------------------------------------------------------------
ax = axs[2]
ax.plot(time[2:], T[2:],'.',c='r', lw=2, alpha=1,label='Excitation Energy')
kargs=ma.getPropertyFromPosition(ylabel=r'E(eV)',xlabel = r'Time(fs)',
                                 title='')
ma.setProperty(ax,**kargs)
#------------------------------------------------------------------------------

plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)