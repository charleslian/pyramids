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
ipiTemp = 3
    
def action(index,folder):
  import os 
  os.chdir('1')
  timeEf, eField = dP.getEField()
  timeEl, exe = dP.getExcitedElectrons()
  exe  -= exe[0]
  timeEn, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure()
  deltaE =  (E_tot[2:,] - E_tot[2])
  os.chdir('..')
  return [(index, folder), (timeEf, eField), (timeEl, exe), (timeEn,deltaE)]

          
fig, axs = plt.subplots(3,1,sharex=True,sharey=False,figsize=(6,8))
axs = axs.flatten()
SaveName = __file__.split('/')[-1].split('.')[0]

#axs[ipiTemp].plot(pimdData[:,0],pimdData[:,2])
#
data = scanFolder(action)
print data[-1][0][0]
c = ma.getColors(data[-1][0][0]+1)

ls = ['-','-','-']

maxElectrons = []
maxEnergies = []
minEnergies = []
lw = 1

for [(index, folder), (timeEf, eField), (timeEl, exe), (timeEn,deltaE)] in data:
  #ax = axs[efield]
  #ax.plot(timeEf,eField[:,2], c=c[index],
  #      label=folder,lw=2,alpha=0.8) 
  #eField = float(folder) * 13.6/0.529
  ax = axs[exElectron]
  ax.semilogy(timeEl,exe,'-',alpha=0.8, c=c[index], label=folder,ls=ls[index],
          #label=r'%5.2f $V/\AA$' % eField,c=c[index],
          lw=lw)
  #------------------------------------------------------------------------------
  ax = axs[exEnergy]
  tolerance = 0.5
  for ie, e in enumerate(deltaE[1:-2]):
    if np.abs(deltaE[ie] - deltaE[ie-1]) > tolerance and np.abs(deltaE[ie] - deltaE[ie+1]) > tolerance:
      deltaE[ie] = (deltaE[ie - 1] + deltaE[ie + 1])/2
      
  ax.plot(timeEn[2:], deltaE,'-', c=c[index],ls=ls[index],
          lw=lw, alpha=1)
  
  ax = axs[efield]
  #print timeEf.shape, eField.shape 
  ax.plot(timeEf, eField*13.6/0.529, c=c[index], ls=ls[index], lw=lw) 

  maxElectrons.append(exe.max())
  maxEnergies.append(deltaE.max())
  minEnergies.append(deltaE.min())
  
kargs=ma.getPropertyFromPosition(exElectron, ylabel=r'n(e)',
                                 title='Excited Electrons', 
                                 xlabel = 'Time (fs)', xlimits=[0,40],
                                 #ylimits=[0,np.max(maxElectrons)],
                                 grid=True,
                                 )
ma.setProperty(axs[exElectron],**kargs)
kargs=ma.getPropertyFromPosition(exEnergy, ylabel=r'E (eV)', xlimits=[0,40], grid=True,
                                 #ylimits=[np.min(minEnergies),np.max(maxEnergies)],
                                 title='Excitation Energy')
ma.setProperty(axs[exEnergy],**kargs)
kargs=ma.getPropertyFromPosition(efield, ylabel=r'E ($V/\AA$)',
                                 xlabel = 'Time (fs)', xlimits=[0,40], grid=True,
                                 #ylimits=[np.min(minEnergies),np.max(maxEnergies)],
                                 title='Electric Field')
ma.setProperty(axs[efield],**kargs)

plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)