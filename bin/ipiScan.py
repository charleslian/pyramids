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

def getPIMDdata():
  ''' 
  column   1     --> time{femtosecond} : The elapsed simulation time.
  column   2     --> conserved : The value of the conserved energy quantity per bead.
  column   3     --> temperature{kelvin} : The current temperature, as obtained from the MD kinetic energy.
  column   4     --> kinetic_cv : The centroid-virial quantum kinetic energy of the physical system.
  column   5     --> potential : The physical system potential energy.
  column   6     --> pressure_cv{bar} : The quantum estimator for pressure of the physical system.
  '''
  return np.array([[float(i) for i in line.split()] 
                    for line in open('ipi.out').readlines() if line[0] != '#'])
    


def action(index, folder):
#------------------------------------------------------------------------------
  timeEf, eField = dP.getEField()
  timeEl, exe = dP.getExcitedElectrons()
  exe  -= exe[0]
  timeEn, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure()
  deltaE =  (E_tot[2:,] - E_tot[2])
  
  return [(index, folder), (timeEf, eField), (timeEl, exe), (timeEn,deltaE)]
#------------------------------------------------------------------------------

fig, axs = plt.subplots(2,2,sharex=True,sharey=False,figsize=(8,6))
axs = axs.flatten()
SaveName = __file__.split('/')[-1].split('.')[0]

pimdData = getPIMDdata()
axs[ipiTemp].plot(pimdData[:,0],pimdData[:,2])

data = scanFolder(action)
#print data[-1][0][0]
c = ma.getColors(data[-1][0][0]+1)


maxElectrons = []
maxEnergies = []
minEnergies = []

for [(index, folder), (timeEf, eField), (timeEl, exe), (timeEn,deltaE)] in data:
  #ax = axs[efield]
  #ax.plot(timeEf,eField[:,2], c=c[index],
  #      label=folder,lw=2,alpha=0.8) 
  #eField = float(folder) * 13.6/0.529
  ax = axs[exElectron]
  ax.plot(timeEl,exe,'-',alpha=0.8,
          #label=r'%5.2f $V/\AA$' % eField,c=c[index],
          markerfacecolor='w',lw=2)
  #------------------------------------------------------------------------------
  ax = axs[exEnergy]
  tolerance = 0.5
  for ie, e in enumerate(deltaE[1:-2]):
    if np.abs(deltaE[ie] - deltaE[ie-1]) > tolerance and np.abs(deltaE[ie] - deltaE[ie+1]) > tolerance:
      deltaE[ie] = (deltaE[ie - 1] + deltaE[ie + 1])/2
      
  ax.plot(timeEn[2:], deltaE,'-', c=c[index],
          lw=2, alpha=1)
  
  ax = axs[efield]
  #print timeEf.shape, eField.shape 
  ax.plot(timeEf, eField*13.6/0.529) 

  maxElectrons.append(exe.max())
  maxEnergies.append(deltaE.max())
  minEnergies.append(deltaE.min())
  
kargs=ma.getPropertyFromPosition(exElectron, ylabel=r'n(e)',
                                 title='Excited Electrons', 
                                 xlabel = 'Time (fs)', xlimits=[0,40],
                                 #ylimits=[0,np.max(maxElectrons)],
                                 )
ma.setProperty(axs[exElectron],**kargs)
kargs=ma.getPropertyFromPosition(exEnergy, ylabel=r'E (eV)', xlimits=[0,40],
                                 #ylimits=[np.min(minEnergies),np.max(maxEnergies)],
                                 title='Excitation Energy')
ma.setProperty(axs[exEnergy],**kargs)
kargs=ma.getPropertyFromPosition(efield, ylabel=r'E ($V/\AA$)',
                                 xlabel = 'Time (fs)', xlimits=[0,40],
                                 #ylimits=[np.min(minEnergies),np.max(maxEnergies)],
                                 title='Electric Field')
ma.setProperty(axs[efield],**kargs)
kargs=ma.getPropertyFromPosition(ipiTemp, ylabel=r'T (K)',
                                 xlabel = 'Time (fs)', xlimits=[0,40],
                                 #ylimits=[np.min(minEnergies),np.max(maxEnergies)],
                                 title='Temperature')
ma.setProperty(axs[ipiTemp],**kargs)

plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)