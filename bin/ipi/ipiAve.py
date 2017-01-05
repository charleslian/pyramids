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
  return [(index, folder), (timeEf, eField), (timeEl, exe), (timeEn[2:],deltaE)]
#------------------------------------------------------------------------------

fig, axs = plt.subplots(2,1,sharex=True,sharey=False,figsize=(6,8))
SaveName = __file__.split('/')[-1].split('.')[0]

#pimdData = getPIMDdata()
#axs[-1].plot(pimdData[:,0],pimdData[:,4])

data = scanFolder(action)

rows = data[-1][0][0]+1
c = ma.getColors(rows)
exSteps = min([line[2][0].shape[0] for line in data])
exAve = np.zeros(exSteps)
enSteps = min([line[3][0].shape[0] for line in data])
enAve = np.zeros(enSteps)


for [(index, folder), (timeEf, eField), (timeEl, exe), (timeEn,deltaE)] in data:
  exAve += exe[:exSteps]/rows
  enAve += deltaE[:enSteps]/rows



axs[0].plot(timeEl[:exSteps],exAve,label='4 Beads')
axs[1].plot(timeEn[:enSteps],enAve,label='4 Beads')

import os
print os.chdir('../../Beads=1/E=0.10/1')

[(index, folder), (timeEf, eField), (timeEl, exe), (timeEn,deltaE)] = action(0,'1')

axs[0].plot(timeEl,exe,label='1 Bead')
axs[1].plot(timeEn,deltaE,label='1, Bead')


kargs=ma.getPropertyFromPosition(ylabel=r'n(e)',
                                 title='Excited Electrons', 
                                 xlabel = 'Time (fs)', xlimits=[0,40])
ma.setProperty(axs[0],**kargs)
kargs=ma.getPropertyFromPosition(ylabel=r'E (eV)', xlimits=[0,40], grid=True,
                                 #ylimits=[np.min(minEnergies),np.max(maxEnergies)],
                                 title='Excitation Energy')
ma.setProperty(axs[1],**kargs)
os.chdir('..') 
plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)