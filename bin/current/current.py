#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 07:49:06 2017

@author: cl-iop
"""
import pyramids.io.result as dp
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as ppu
import os
SaveName = __file__.split('/')[-1].split('.')[0]


from matplotlib import pyplot as plt
import numpy as np

def readCurrent():
  import os
  lines = os.popen('grep "TDAP: Afield: Current" result').readlines()
  data = []
  for line in lines:
    #print line.split()
    data.append([float(i) for i in line.split()[4:7]])
  data = np.array(data)
  return data - data[0,:]

data = readCurrent()

from pyramids.io.fdf import tdapOptions
options = tdapOptions()
timestep = options.tdTimeStep[0]

fig, axs = plt.subplots(3,1,sharex=True,sharey=False)#,figsize=(10,6)
ax = axs[0]
for i in range(3):
  ax = axs[i]
  ax.plot(np.arange(data.shape[0])*timestep,data[:,i], '-o',
          label=['x','y','z'][i],lw=2, alpha=1.0)


  args = ma.getPropertyFromPosition()
  ma.setProperty(ax,**args)

#ax = axs[1]
#ppu.plotEField(ax,label='efield')

plt.tight_layout()
for save_type in ['.png']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)