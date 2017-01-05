# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 11:40:24 2016

@author: cl-iop
"""

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

for eFieldType in ('ExternalElectricField','TD.GaugeField'):
  print eFieldType
  os.chdir(eFieldType)
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
    if eFieldType == 'TD.GaugeField': 
      dipolesIon[index,:] = dp.getIonicPolarization()[-1] 
      dipoles[index,:] = dp.getElectronPolarization()[-1] 
    else:
      dipoles[index,:] = dp.getDipole()[1][-1]
    os.chdir('..')
  print dipoles 
  print dipolesIon
  print dipoles + dipolesIon
  #print (energy[-1]-energy[0])/(Efield[-1]-Efield[0])
  axs[0].plot(Efield,energy ,'-o',label=eFieldType) 
  for i, direction in enumerate(('x','y','z')):
    axs[1].plot(Efield,(dipoles + dipolesIon)[:,i] ,'-o',label=eFieldType+' '+direction) 

  os.chdir('..')
  
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