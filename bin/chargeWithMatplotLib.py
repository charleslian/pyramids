# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 09:24:19 2016

@author: cl-iop
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 09:31:02 2016

@author: cl-iop
"""

from ase.io.cube import read_cube_data
from ase.io import write
from pyramids.plot.setting import getPropertyFromPosition, setProperty

from ase.data import covalent_radii
from ase.data.colors import cpk_colors
from ase.calculators.siesta.import_functions import xv_to_atoms

from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

selectedTimeSteps = range(5,1000,20)

vmax = 0.01
vmin = -vmax

slide = 27

dataAndAtoms = [read_cube_data(str(i)+'/siesta.DRHO.cube') for i in selectedTimeSteps]

fig, axs = plt.subplots(1,2,figsize=(12,6))

pho0,atoms  = dataAndAtoms[0]
#atoms = xv_to_atoms('siesta.XV')
X = np.arange(pho0.shape[1])*atoms.cell[1,1]/pho0.shape[1]
Y = np.arange(pho0.shape[2])*atoms.cell[2,2]/pho0.shape[2]
x, y = np.meshgrid(X, Y)


import pyramids.io.result as dP
time, light = dP.getEField()
step = len(time)/len(dataAndAtoms)
#print light.shape
line, = axs[1].plot(time,light[:,2])
scatter, = axs[1].plot(0,0,'o')

def animate(i): 
  i = i % len(dataAndAtoms)
  z = (dataAndAtoms[i][0]-pho0)[slide,:,:] 
  atoms = dataAndAtoms[i][1]
  print z.min(), z.max()
  axs[0].contourf(x, y, z, 100,vmin = vmin,vmax =vmax, cmap = cm.jet)
  for pos, Z in zip(atoms.positions, atoms.numbers):
    axs[0].scatter(pos[2],pos[1],c=tuple(cpk_colors[Z]),s=400*covalent_radii[Z])
  setProperty(axs[0],**getPropertyFromPosition(0,xlimits=[2,6],ylimits=[2,6],
              xlabel = r'distance($\AA$)',ylabel = r'distance($\AA$)')) 
  scatter.set_data(time[selectedTimeSteps[i]],light[selectedTimeSteps[i],2])
  setProperty(axs[1],**getPropertyFromPosition(1,
              xlabel = r'time(fs)',ylabel = r'E-Field(a.u.)'))
  plt.tight_layout()
  #return cont


anim = animation.FuncAnimation(fig, animate, frames=40)
#anim.save('H2O_Sawtooth.mp4',dpi=300)
