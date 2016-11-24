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

QEEnergy_file = os.popen('grep "!    total energy" */result |sort -n')
tuples = np.array([(float(line.split()[0].split('/')[0]),float(line.split()[-2]))
                    for line in QEEnergy_file.readlines()])
                      
ax =axs[0]
Efield = tuples[:,0]*VA         
Energy = (tuples[:,1] - np.max(tuples[:,1]))*Ry
ax.plot(Efield,Energy,'-o')
kargs=ma.getPropertyFromPosition(ylabel=r'Energy(eV)',xlabel=r'$\varepsilon(V/\AA)$',
                                 title='')
ma.setProperty(ax,**kargs)
ax.grid(which=u'major',axis='x')
ax.grid(which=u'major',axis='y')

ax =axs[1]
efields = os.popen('ls -d [0-9]*').readlines()
nDir = len(efields)
Efield = np.zeros([nDir])
dipoles = np.zeros([nDir,3])
for index, efield in enumerate(efields):
  QEDipole = os.popen('grep -i "Electronic Dipole per cell" '+efield[:-1]+'/result |tail -n 3')
  lines = QEDipole.readlines()
  Efield[index] = float(efield)*VA
  dipoles[index,:] = [float(line.split()[-1]) for line in lines]

print (Energy[-1]-Energy[0])/(Efield[-1]-Efield[0])
for i,direct in enumerate(['x','y','z']):
  if i ==2 : ax.plot(Efield,dipoles[:,i],'-o',label=direct)
kargs=ma.getPropertyFromPosition(ylabel=r'Dipole(a.u.)',xlabel=r'$\varepsilon(V/\AA)$',
                                 title='')
ma.setProperty(ax,**kargs)

ax.grid(which=u'major',axis='x')
ax.grid(which=u'major',axis='y')

plt.tight_layout()
for save_type in ['.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)