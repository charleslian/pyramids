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
fig, axs = plt.subplots(cut,1,figsize=(8,8*cut))

points=np.array([(reciprocal_vectors[0,0:2]*i+
                  reciprocal_vectors[1,0:2]*j+
                  reciprocal_vectors[2,0:2]*k) 
                  for i in range(-1,2) 
                  for j in range(-1,2)
                  for k in range(0,1)])
print points[:,0].max(), points[:,0].min()
from scipy.spatial import Voronoi, voronoi_plot_2d, convex_hull_plot_2d

vor = Voronoi(points)
#print vor.vertices

#ax.scatter(kcoor[:,0],kcoor[:,1],marker='o',facecolor='w',s=50)
numKpts = kcoor.shape[0]
for direct in range(cut):
  ax = axs#[direct]
  voronoi_plot_2d(vor,ax)
  dim1 = direct%3
  dim2 = (direct+1)%3
  print dim1,dim2
  for i in range(numKpts):
    an1 = ax.annotate(str(i+1), xy=(kcoor[i,dim1], kcoor[i,dim2]), xycoords="data",
                      va="center", ha="center", fontsize=120/np.sqrt(numKpts), color='r',
                      bbox=dict(boxstyle="circle", fc='w',alpha=0.2))
    #plt.text(kcoor[i,0],kcoor[i,1],str(i+1),fontsize=8)
  d = 0.1              
  kargs=getPropertyFromPosition(direct,r'$k_x(\AA^{-1})$',"$k_y(\AA^{-1})$",
                                    xlimits=[kcoor[:,dim1].min() - d , kcoor[:,dim1].max() + d],
                                    ylimits=[kcoor[:,dim2].min() - d, kcoor[:,dim2].max() + d])

  ax.axis('equal')                                  
  ax.minorticks_on()
  setProperty(ax,**kargs)  
#plt.show()
plt.tight_layout()
ims = []
#plt.show()
#  import matplotlib.animation as manimation
#  FFMpegWriter = manimation.writers['ffmpeg']
#  metadata = dict(title='Movie Test', artist='Matplotlib',
#                  comment='Movie support!')
#  writer = FFMpegWriter(fps=15, metadata=metadata)
saveTypes = ['pdf']
#for save_type in saveTypes:
  #plt.savefig('Ksampling.'+save_type,transparent=True,dpi=600)
