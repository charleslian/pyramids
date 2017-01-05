# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 12:12:31 2016

@author: cl-iop
"""


from scipy import linalg
import numpy as np
import matplotlib.pyplot as plt
from numpy import exp, sqrt, pi
from ase.dft.kpoints import monkhorst_pack
import ase
import pyramids.plot.setting as ma


#Parameters
numBands = 2
t1 = t2 = t3 = 1
Ep = 0
t  = 4 
a = 1.42 # C-C bond length
nk = 36 # K mesh grid : 6N x 6N x 1

#Basic setting
cell = np.array([[0.5*sqrt(3)*a, 1.5*a, 0],[0.5*sqrt(3)*a, -1.5*a, 0], [0,0,10]])
positions = np.array([[0,0,0],[0,-a,0]])
atoms = ase.Atoms(symbols='C2', cell=cell, positions=positions, pbc=True)
recLattice = 2*pi*atoms.get_reciprocal_cell()

mesh = monkhorst_pack([nk,nk,1]) + np.array([0.5/nk, 0.5/nk, 0]) #shift to Gamma
kpoints = np.dot(mesh,recLattice)

#For 3D surface ploting
kxs = list(set(mesh[:,0]));kxs.sort()
kys = list(set(mesh[:,1]));kys.sort()
surfX, surfY = np.meshgrid(kxs,kys)


def setupHamiltonian(kx, ky):
  H = np.zeros([2,2],dtype=complex)
  H[0,1] = np.sum([t1*exp(-0.5j*(sqrt(3)*a*kx + a*ky)),
                   t2*exp(-0.5j*(-sqrt(3)*a*kx + a*ky)), 
                   t3*exp(-1.0j*(a*ky))])
  H[1,0] = np.conj(H[0,1])
  H[0,0] = Ep
  H[1,1] = Ep
  return H

eigenPi = []

for kx, ky, kz in kpoints:
  H = setupHamiltonian(kx, ky)
  eigenvalues, eigvectors = linalg.eigh(H)
  eigenPi.append(eigenvalues)
  
eigenPi = np.array(eigenPi).reshape([nk,nk,2])

# Drawing
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize=(10,6))
ax = fig.gca(projection='3d')

surf = ax.plot_surface(surfX, surfY, eigenPi[:,:,0], rstride=1, cstride=1, cmap='Blues_r',
                       linewidth=0.1, antialiased=True, shade=True)
surf = ax.plot_surface(surfX, surfY, eigenPi[:,:,1], rstride=1, cstride=1, cmap='Reds',
                       linewidth=0.1, antialiased=True, shade=True)