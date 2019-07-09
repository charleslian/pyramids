#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 07:43:17 2017

@author: clian
"""

import pyramids.io.result as dp
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as ppu
from pyramids.io.fdf import tdapOptions
from matplotlib import pyplot as plt
import numpy as np
import os

from pyramids.io.result import readData
dt = dp.getElectronStepLength()

nocc = int(float(os.popen('grep "starting charge" result').readline().split()[-1])/2.0)
print nocc
fig, axs = plt.subplots(1,2,sharex=True,figsize=(8,5))

ax = axs[0]
norm, kweight = readData('pwscf.norm.dat')
excite = (norm - norm[0,:,:])
for ib in range(excite.shape[2]):
    excite[:,:,ib] *= kweight
    #pass
#print excite
time = np.arange(excite.shape[0]) * dt
ax.plot(time, (excite[:,:,:nocc]).sum(axis=(1,2)))
ax.plot(time, (excite[:,:,nocc:]).sum(axis=(1,2)))

args = ma.getPropertyFromPosition(0,title='Excited electrons',ylabel='n (e)')
ma.setProperty(ax,**args)

ax = axs[1]

value, kweight = readData('pwscf.value.dat')
#print norm
ax.plot(time, value[:,0,:],'-')

args = ma.getPropertyFromPosition(0,title='Excited electrons',ylabel='n (e)')
ma.setProperty(ax,**args)



plt.tight_layout()

SaveName = __file__.split('/')[-1].split('.')[0]
for save_type in ['.png']:
  filename = SaveName + save_type
  #plt.savefig(filename,orientation='portrait',dpi=600)