#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 09:55:49 2017

@author: clian
"""

import numpy as np
from matplotlib import pyplot as plt
import pyramids.io.result as dp
import pyramids.plot.PlotUtility as ppu
import pyramids.plot.setting as ma
from pyramids.io.fdf import tdapOptions
numStep = 5

fig, axs = plt.subplots(numStep,1,sharex=True,sharey=True,figsize=(6,8))


timeStep = tdapOptions().tdTimeStep
steps = dp.getEIGSteps()
selectedSteps = range(0,len(steps),len(steps)/numStep)

print selectedSteps
for i in range(numStep):
  ax = axs[i]
  title = '$t = %3.2f$ %s' % (i*len(steps)/numStep*timeStep[0], timeStep[1])
  ppu.plotDOS(ax, selectedSteps[i], bins=100, title = title, yticks=[])
  
  
plt.tight_layout()
SaveName = __file__.split('/')[-1].split('.')[0]
if True:
  for save_type in ['.pdf']:
    filename = SaveName + save_type
    plt.savefig(filename,dpi=600)