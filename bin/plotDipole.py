import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dp
import pyramids.plot.setting as ma
import os


fig, axs = plt.subplots(2,1,sharex=True,sharey=False,figsize=(6,8))
SaveName = __file__.split('/')[-1].split('.')[0]

startStep = 10
c = ma.getColors(4)


ax = axs[0]
time, T, E_ks, E_tot, Vol, P  = dp.getEnergyTemperaturePressure()
time, dipoles = dp.getDipolePython()
for i,direct in enumerate(('x','y','z')):
  ax.plot(time[2:],dipoles[2:,i],label=direct)
  
ax.grid(which=u'major',axis='x')
ax.grid(which=u'major',axis='y')
kargs=ma.getPropertyFromPosition(ylabel=r'Dipole(a.u)',
                                 xlabel='Time(fs)')
ma.setProperty(ax,**kargs)

ax = axs[1]
time, dipoles = dp.getEField()
for i,direct in enumerate(('x','y','z')):
  ax.plot(time,dipoles[:,i]-dipoles[0,i],label=direct)
  
ax.grid(which=u'major',axis='x')
ax.grid(which=u'major',axis='y')
kargs=ma.getPropertyFromPosition(ylabel=r'$\varepsilon$(a.u)',
                                 xlabel='Time(fs)')

ma.setProperty(ax,**kargs)
                            

plt.tight_layout()