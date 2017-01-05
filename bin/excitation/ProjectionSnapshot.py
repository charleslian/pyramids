#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as pu
from ase.dft.kpoints import get_special_points
from ase.calculators.siesta.import_functions import xv_to_atoms
from ase.lattice import hexagonal


#------------------------------------------------------------------------------



kpath = []
cut = [0]
atom = xv_to_atoms('siesta.XV')
specialKPoints = [r'$M$',r'$\Gamma$',r'$K$',r'$M$']

kpoints, kwgt = dP.readKpoints()
nkpts = kpoints.shape[0]

for i in range(79,2,-13):
  print i
  kpath.append(i)
cut.append(len(kpath))

kpath.append(6)
kpath.append(5)
for i in range(12,45,11):
  print i
  kpath.append(i)
  kpath.append(i-1)
cut.append(len(kpath))

for i in range(45,73,14):
  print i
  kpath.append(i)
  kpath.append(i+1)
cut.append(len(kpath))
kpath.append(73)

kpath = np.array(kpath) - 1
cut = np.array(cut)

x = np.arange(kpath.shape[0])

homo = dP.getHomo()
evolvingBands = range(0, homo + 7)
time, exe = dP.getProjectedPartition()
time, eigen = dP.getAdiabaticEigenvalue()
#exe -= exe[0,:,:]
fig, axs = plt.subplots(2,2,sharex=True,sharey=True,figsize=(8,6))
axs = axs.flatten()
SaveName = __file__.split('/')[-1].split('.')[0] 
for i, step in enumerate(330, 450, 750, 900):
  excited = np.abs(exe[step,kpath,:] - exe[0,kpath,:])
  norm = 10.0/np.max(exe[:,kpath,:] - exe[0,kpath,:])
  eigenvalue = eigen[step,kpath,:]
  ax = axs[i]
  print eigenvalue.shape, excited.shape, x.shape
  for i in evolvingBands:
    if i < homo:
      part = excited[:,i]
      s = ax.fill_between(x, eigenvalue[:,i] - norm*part, 
                          eigenvalue[:,i] + norm*part,
                          lw=0.0,color='b',alpha=0.7)
    else:
      part = excited[:,i]
      s = ax.fill_between(x, eigenvalue[:,i] - norm*part, 
                          eigenvalue[:,i] + norm*part,
                          lw=0.0,color='r',alpha=0.7)  
                 
    ax.plot(x, eigenvalue[:,i],'.-',lw=1.5,c='k')
    
  plt.axis('tight')                
  kargs=ma.getPropertyFromPosition(ylabel=r'Eigenvalues(eV)',
                                   xlabel='',xticks=cut,
                                   xticklabels=specialKPoints,
                                   xlimits=[cut[0],cut[1]],
                                   vline=cut,
                                   title='Population',
                                   hline=[0.0],)            
  ma.setProperty(ax,**kargs)
#------------------------------------------------------------------------------
plt.tight_layout()
for save_type in ['.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=400)

#view(atom)
#print get_special_points('hexagonal',hexagonal.Graphene('C',latticeconstant=(1.42,10)).cell)
#coor = [(0.5, 0.5, 0), (0,0,0), 
#GXW = [points[k] for k in 'GXW']
#n = int(np.sqrt(nkpts*2))
#for i in range(n,n*(n/2-2),n-1):
#  print i
#  kpath.append(i)
#  kpath.append(i-1)
#cut.append(len(kpath))
