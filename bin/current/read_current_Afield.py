

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 07:49:06 2017
@author:mxguan-iop
"""
import pyramids.io.result as dp
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as ppu
from pyramids.io.fdf import tdapOptions
import os
SaveName = __file__.split('/')[-1].split('.')[0]


from matplotlib import pyplot as plt
import numpy as np

#----------------------------------------------- 
def getCurrentPython():
  options = tdapOptions()
  context = []
  for line in open('result').readlines():
      if len(line) == 1:
          continue
      if 'Current' in line.split() :
          context.append(line[:-1])
  #print context
  current = [[float(line.split()[-4]),float(line.split()[-3]),float(line.split()[-2])] for line in context]
 # print current
  data = np.array(current)
  #print data
  #time = np.arange(len(current))*timestep
  #print data
  return data 

#----------------------------------------------- 
def getAField():
  if os.path.exists('TDAFIELD'):
     Afield = [[float(i) for i in line.split()] for line in open('TDAFIELD')]   
     Afield = np.array(Afield)/1E5
     options = tdapOptions()
     timestep = options.tdTimeStep[0]
     time = np.arange(len(Afield))*timestep
  else:
    time = np.zeros(2)
    Afield = np.zeros([2,3])
  return time, Afield 
#-----------------------------------------------   
#----------------------------------------------- 
def plotAField(ax, label=''):
  time, Afield = dp.getAField()
  #directions = ['x', 'y', 'z']
  for direct in range(3):
    if max(Afield[:,direct]) > 1E-10:
      ax.plot(time,Afield[:,direct],
              label=label, lw=2, alpha=1.0) 
  kargs=ma.getPropertyFromPosition(ylabel=r'$\varepsilon$(a.u.)',xlabel='Time(fs)',
                                   title='vector Field')
  ma.setProperty(ax,**kargs)  
#----------------------------------------------- 
data =getCurrentPython()
options = tdapOptions()
timestep = options.tdTimeStep[0]

fig, axs = plt.subplots(3,1,sharex=True,sharey=False,figsize=(15,9))
ax = axs[0]
for i in range(3):
  ax.plot(np.arange(data.shape[0])*timestep,data[:,i],
          label=['x','y','z'][i],lw=2, alpha=1.0)

args = ma.getPropertyFromPosition(xlimits=None,ylimits=None,ylabel='I(a.u)')
ma.setProperty(ax,**args)

ax = axs[1]
ppu.plotAField(ax,label='Afield')
ax = axs[2]
ppu.plotEField(ax,label='Efield')
plt.tight_layout()
for save_type in ['.png']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)
