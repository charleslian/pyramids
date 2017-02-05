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

numStep = 5

fig, axs = plt.subplots(numStep,1,sharex=True,sharey=True,figsize=(8,6))

steps = dp.getEIGSteps()
selectedSteps = range(0,len(steps),len(steps)/numStep)

print selectedSteps
for i in range(numStep):
  ax = axs[i]
  ppu.plotDOS(ax, selectedSteps[i], bins=100)
  
  
plt.tight_layout()