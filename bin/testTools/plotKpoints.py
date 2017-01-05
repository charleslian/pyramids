#!/usr/bin/python
"""
Created on Mon Mar 21 12:31:44 2016

@author: cl-iop
"""
import numpy as np
from scipy.fftpack import fft, ifft
from pyramids.plot.setting import getPropertyFromPosition, setProperty, getColors
from pyramids.io.fdf import tdapOptions
import pyramids.io.result as dp
import matplotlib.pyplot as plt
import os
import ase
from ase.calculators.siesta.import_functions import xv_to_atoms

atom_temp = xv_to_atoms('siesta.XV')
atoms = ase.atoms.Atoms(symbols=atom_temp.get_chemical_symbols(),
                        positions=atom_temp.get_positions(),
                        cell = atom_temp.get_cell())
                        
reciprocal_vectors = 2*np.pi*atoms.get_reciprocal_cell()

kcoor, kweight = dp.readKpoints()
                            
import matplotlib.pyplot as plt
cut = 1
fig = plt.figure()
from mpl_toolkits.mplot3d import Axes3D
ax = fig.add_subplot(1,1,1,projection='3d')

points=np.array([(reciprocal_vectors[0,0:2]*i+
                  reciprocal_vectors[1,0:2]*j+
                  reciprocal_vectors[2,0:2]*k) 
                  for i in range(-1,2) 
                  for j in range(-1,2)
                  for k in range(-1,2)])
print points[:,0].max(), points[:,0].min()
from scipy.spatial import Voronoi, voronoi_plot_2d, convex_hull_plot_2d
vor = Voronoi(points)
ax.scatter3D(kcoor[:,0],kcoor[:,1],kcoor[:,2],marker='o',s=50)
numKpts = kcoor.shape[0]

for i in range(numKpts):
  x,y,z = kcoor[i,:]
  label = str(i)
  ax.text(x, y, z, label)
  #an1 = ax.annotate(str(i+1), xy=(kcoor[i,0], kcoor[i,0], kcoor[i,2]), xycoords="data",
  #                  va="center", ha="center", fontsize=120/np.sqrt(numKpts), color='r',
  #                  bbox=dict(boxstyle="circle", fc='w',alpha=0.2))


  
  
plt.tight_layout()
