# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 12:54:01 2017

@author: cl-iop
"""
import pyramids.io.result as dp
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as ppu
from pyramids.io.fdf import tdapOptions
from matplotlib import pyplot as plt
import numpy as np
import os

fig, axs = plt.subplots(3,1,sharex=True,sharey=False,figsize=(6,8))

dt = dp.getElectronStepLength()

Efield = [[float(i) for i in line.split()] for line in open('TDAFIELD')]
Efield = np.array(Efield)/1E5

axs[2].plot(Efield)


f = os.popen('grep "!    total energy" result')
energy = np.array([float(line.split()[-2]) for line in f.readlines()])*13.6
print energy

axs[1].plot(energy)


norm, kweight, nocc = dp.readExcitationFile()
excite = (norm - norm[0,:,:])
for ib in range(excite.shape[2]):
    excite[:,:,ib] *= kweight
    #pass
time = np.array(range(excite.shape[0]+1))
step = min(time.shape[0]-1, excite.shape[0])
axs[0].plot(time[1:step+1], (excite[:step,:,:nocc]).sum(axis=(1,2)))
axs[0].plot(time[1:step+1], (excite[:step,:,nocc:]).sum(axis=(1,2)))