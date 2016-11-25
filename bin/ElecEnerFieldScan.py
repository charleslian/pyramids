#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
from pyramids.plot.PlotUtility import scanFolder
#------------------------------------------------------------------------------
efield = 2
exElectron = 0
exEnergy = 1

def action(index, folder):
#------------------------------------------------------------------------------
  timeEf, eField = dP.getEField()
  timeEl, exe = dP.getExcitedElectrons()
  exe  -= exe[0]
  timeEn, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure()
  deltaE =  (E_ks[2:,] - E_ks[2])
  
  return [(index, folder), (timeEf, eField), (timeEl, exe), (timeEn,deltaE)]
#------------------------------------------------------------------------------

fig, axs = plt.subplots(3,1,sharex=True,sharey=False,figsize=(8,5))
SaveName = __file__.split('/')[-1].split('.')[0]


data = scanFolder(action)
#print data[-1][0][0]
c = ma.getColors(data[-1][0][0]+1)



maxElectrons = []
maxEnergies = []
minEnergies = []

for [(index, folder), (timeEf, eField), (timeEl, exe), (timeEn,deltaE)] in data:
  ax = axs[efield]
  for i in range(3):
    if max(eField[:,i]) > 1E-10:
      directionE = ['/x','/y','/z'][i]
      ax.plot(timeEf,eField[:,i], c=c[index],
            label="%4.1e " % float(folder) + directionE ,lw=2,alpha=0.8) 
  #eField = float(folder) * 13.6/0.529
  ax = axs[exElectron]
  ax.plot(timeEl,exe,'-',alpha=0.8,
          #label=r'%5.2f $V/\AA$' % eField,
          c=c[index],
          markerfacecolor='w',lw=2)
  #------------------------------------------------------------------------------
  ax = axs[exEnergy]
  tolerance = 0.5
  for ie, e in enumerate(deltaE[1:-2]):
    if np.abs(deltaE[ie] - deltaE[ie-1]) > tolerance and np.abs(deltaE[ie] - deltaE[ie+1]) > tolerance:
      deltaE[ie] = (deltaE[ie - 1] + deltaE[ie + 1])/2
      
  ax.plot(timeEn[2:], deltaE,'-', c=c[index],
          lw=2, alpha=1)
  maxElectrons.append(exe.max())
  maxEnergies.append(deltaE.max())
  minEnergies.append(deltaE.min())
  
kargs=ma.getPropertyFromPosition(exElectron, ylabel=r'n(e)',
                                 title='Excited Electrons', 
                                 ylimits=[0,np.max(maxElectrons)],
                                 xlimits=None,)
ma.setProperty(axs[exElectron],**kargs)
kargs=ma.getPropertyFromPosition(exEnergy, ylabel=r'E(eV)',
                                 ylimits=[np.min(minEnergies),np.max(maxEnergies)],
                                 title='Excitation Energy'
                                 )
ma.setProperty(axs[exEnergy],**kargs)

kargs=ma.getPropertyFromPosition(efield, ylabel=r'$\varepsilon$',
                                 xlabel = 'Time (fs)',
                                 title='Electric Field'
                                 )
ma.setProperty(axs[efield],**kargs)

plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)