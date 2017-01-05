#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 06:28:23 2016

@author: cl-iop
"""
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dp
import pyramids.plot.setting as ma
import qutip as qp
#numSample = 20
#thetas = np.linspace(0,np.pi/2.0,numSample)
#x = 0.2*np.sin(thetas)
#x = thetas
#y = np.ones(numSample)
#y2 = np.load('angle.npy')

#
##ax.plot(x,y1,'-',label = 'angle')
#ax.scatter(x,y,s=y2*100,label = 'angle')
#kargs = ma.getPropertyFromPosition(ylabel=r'', xlabel=r'$A \sin\theta$',title='')
#ma.setProperty(ax,**kargs)
#
#plt.tight_layout()
#SaveName = __file__.split('/')[-1].split('.')[0] 
#for save_type in ['.pdf']:
#  plt.savefig(SaveName+save_type,transparent=True,dpi=600)

import ase.dft.kpoints as adk
from ase.calculators.siesta.import_functions import xv_to_atoms
from ase.visualize import view
from graphene import *
import pyramids.plot.PlotUtility as pu


atoms = xv_to_atoms('siesta.XV')
#view(atoms)
reciprocal_vectors = 2*np.pi*atoms.get_reciprocal_cell()
N = 24
mesh = adk.monkhorst_pack([N ,N ,1])+ np.array([0.5/N , 0.5/N , 0.0])
shiftK = np.array([1/3.0 , 2/3.0, 0.0]).dot(reciprocal_vectors)

kpoints = mesh.dot(reciprocal_vectors)[:,:2]/3.0

args={'t0':10.0,'sigma': 4.0, 'omega':2.0, 'phi':0.0, 'parity':1, 'vFermi' : 6.348}
args['A'] = 0.2
args['times'] = np.linspace(0.0, 20.0, 100.0)

energyBandDown = []
energyBandUp = []



import os
if os.path.exists('function.npy'):
  function = np.load('function.npy')
else:
  function = []
  
  
if len(function) == 0 or function.shape[0] != kpoints.shape[0]:
  function = []
  for index, kpoint in enumerate(kpoints):
    print index,
    args['kpoint'] = kpoint
    H0 = args['parity']*args['vFermi']*(args['kpoint'][0]*qp.sigmax() + args['kpoint'][1]*qp.sigmay())
    #eigen1, eigen2 = H0.eigenenergies()
    result, proj0, proj1 = excitation(args)
    #energyBandDown.append(eigen1)
    #energyBandUp.append(eigen2)
    function.append(proj1)
  
  function = np.array(function)
  np.save('function', function)
  
#for f in function:
#  plt.plot(args['times'],f)
#print function
#from mpl_toolkits.mplot3d import Axes3D
fig, ax=plt.subplots(1,1)
pu.plot2DBZ(ax,atoms)
ax.scatter(kpoints[:,0]+shiftK[0], kpoints[:,1]+shiftK[1],500*function[:,-1],lw=0,cmap= 'gist_rainbow')
ax.grid()
#fig = plt.figure(figsize=(8,6))
#ax = fig.add_subplot(111,projection='3d')
#ax.scatter(kpoints[:,0],kpoints[:,1],energyBandDown)
#ax.scatter(kpoints[:,0],kpoints[:,1],energyBandUp)

#function = []
#for index, theta in enumerate(thetas):
#  args['kpoint'] = (np.cos(theta), np.sin(theta))
#  ax = axs[1]
#  #label = r'$A = $ %2.1f eV'% (A)
#  ax.plot(args['times'], HCoeff(args['times'],args), color=colors[index])
