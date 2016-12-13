#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
plt.style.use('ggplot')
#------------------------------------------------------------------------------
fig, axs = plt.subplots(3,1,sharex=True,sharey=False,figsize=(6,8))
SaveName = __file__.split('/')[-1].split('.')[0]
c = ['b','r','g','y']

ax = axs[2]
time, Efield = dP.getEField()
directions = ['x', 'y', 'z']
for direct in range(3):
  ax.plot(time,Efield[:,direct] ,c=c[direct],
          label=directions[direct],lw=2,alpha=0.8) 
kargs=ma.getPropertyFromPosition(ylabel=r'$\varepsilon$(a.u.)',xlabel='Time(fs)',
                                 title='Electric Field')
ma.setProperty(ax,**kargs)
ax.ticklabel_format(style='sci',axis='y',scilimits=[0,0])
#------------------------------------------------------------------------------
ax = axs[0]
Time, exe = dP.getExcitedElectrons()  
ax.plot(Time,exe - exe[0],'-',alpha=0.8,c=c[0],markerfacecolor='w',lw=2)
kargs=ma.getPropertyFromPosition(ylabel=r'n(e)',
                                 title='Excited Electrons', 
                                 xlimits=None,)
                                 #ylimits=[exe.min(),exe.max()])
print exe[-1] - exe[0]
ma.setProperty(ax,**kargs)
#------------------------------------------------------------------------------
ax = axs[1]
time, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure()
deltaE =  (E_ks - E_ks[0])
ax.plot(time, deltaE,'-',c=c[-1], lw=2, alpha=1, label=r'$E_{total}$')
kargs=ma.getPropertyFromPosition(ylabel=r'E(eV)',title='Excitation Energy')
ma.setProperty(ax,**kargs)
#------------------------------------------------------------------------------

plt.tight_layout()
if False:
  for save_type in ['.pdf','.png']:
    filename = SaveName + save_type
    plt.savefig(filename,dpi=600)