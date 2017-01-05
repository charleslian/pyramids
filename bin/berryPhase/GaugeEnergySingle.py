# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 08:52:16 2016

@author: cl-iop
"""
import numpy as np
from matplotlib import pyplot as plt
import pyramids.io.result as dp
import pyramids.plot.setting as ma
import os

fig, axs = plt.subplots(2,1,sharex=True,sharey=False,figsize=(8,6))
SaveName = __file__.split('/')[-1].split('.')[0]
Ry = 13.605
Bohr = 0.549
VA = Ry/Bohr      

ax =axs[0]


efields = os.popen('ls -d [0-9]*').readlines()
nDir = len(efields)
Efield = np.zeros([nDir])
energy = np.zeros([nDir])
dipoles = np.zeros([nDir,3])
dipolesIon = np.zeros([nDir,3])
for index, efield in enumerate(efields):
  os.chdir(efield[:-1])
  Efield[index] = float(efield[:-1])*VA
  energy[index] = dp.getEnergyTemperaturePressure()[3][-1]
  x = dp.getGaugeFreePolarization()[-1]
  dipolesIon[index,:] = dp.getIonicPolarization()[-1] 
  dipoles[index,:] = (dp.getElectronPolarization()[-1]/x)
  os.chdir('..')
  
correct = np.zeros([nDir,3])
#correct[:,2] = np.array([1,0,1,1,2,2,2,2,2])
print dipoles 
#print dipolesIon
print dipoles + dipolesIon
#print (energy[-1]-energy[0])/(Efield[-1]-Efield[0])
axs[0].plot(Efield,energy ,'-o',) 
for i, direction in enumerate(('x','y','z')):
  axs[1].plot(Efield,(dipoles+correct)[:,i] ,'-o',label=direction) 


  
kargs=ma.getPropertyFromPosition(ylabel=r'Energy(eV)',xlabel=r'$\varepsilon(V/\AA)$',
                                 title='', grid = True)
ma.setProperty(axs[0],**kargs)              

kargs=ma.getPropertyFromPosition(ylabel=r'Dipole(a.u.)',xlabel=r'$\varepsilon(V/\AA)$',
                                 title='', grid = True)
ma.setProperty(axs[1],**kargs)     


plt.tight_layout()
for save_type in ['.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)