#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
from pyramids.plot.PlotUtility import scanFolder
#------------------------------------------------------------------------------
efield = -1
exTemp = 0
exEnergy = 1

def action(index, folder):
#------------------------------------------------------------------------------
  timeEn, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure()
  deltaE =  (E_tot[2:,] - E_tot[2])
  return [(index, folder), (timeEn[2:], deltaE, T[2:])]
#------------------------------------------------------------------------------

fig, axs = plt.subplots(2,1,sharex=True,sharey=False,figsize=(6,8))
SaveName = __file__.split('/')[-1].split('.')[0]


data = scanFolder(action)
#print data[-1][0][0]
chenc = ma.getColors(5)[1:-1]

#print data

maxElectrons = []
maxEnergies = []
minEnergies = []

for [(index, folder), (timeEn,deltaE, T)] in data:
  eField = float(folder) * 13.6/0.529
  ax = axs[exTemp]        
  ax.plot(timeEn, T,'-', c=c[index], 
          lw=2, alpha=1)
          
  ax = axs[exEnergy]
  ax.plot(timeEn, deltaE,'-', c=c[index],
          label=r'%5.2f $V/\AA$' % eField,
          lw=2, alpha=1)
          

  
kargs=ma.getPropertyFromPosition(exEnergy, ylabel=r'E(eV)',
                                 title='Excitation Energy', 
                                 xlabel='Time (fs)',
                                 #ylimits=[0,np.max(maxElectrons)],
                                 xlimits=None,)
ma.setProperty(axs[exEnergy],**kargs)
kargs=ma.getPropertyFromPosition(exTemp, ylabel=r'T(K)',                     
                                 #ylimits=[np.min(minEnergies),np.max(maxEnergies)],
                                 title='Temperature')
ma.setProperty(axs[exTemp],**kargs)

plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)