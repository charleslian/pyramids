# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 21:13:51 2017

@author: clian
"""

import pyramids.io.result as dp
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as ppu
from pyramids.io.fdf import tdapOptions
from matplotlib import pyplot as plt
import numpy as np
import os
def action(index, folder):
  norm, kweight, nocc = dp.readExcitationFile()
  excite = (norm[-1,:,nocc:] - norm[0,:,nocc:]).sum()
  
  evalue, kweight, nocc = dp.readExcitationFile('pwscf.value.dat')
  

  energy = dp.readTotalEnergy()
  exEn =  energy[-1] - energy[0]
  dEva = (evalue[-1,:,:nocc]-evalue[0,:,:nocc]).mean()
#  for ib in range(excite.shape[2]):
#      excite[:,:,ib] *= kweight
  return float(folder), excite, exEn, dEva


fig, axs = plt.subplots(2,1,sharex=False,sharey=False,figsize=(6,8))

data = np.array(ppu.scanFolder(action))

tStep = data[:,0]
print (data[-1,1]-data[0,1])/(tStep[-1]-tStep[0])
axs[0].loglog(tStep,data[:,1]/tStep,'o-')
#axs[1].plot(data[:,0],data[:,2]/data[:,0],'o-')
axs[1].loglog(tStep,data[:,3]/tStep,'o-')
