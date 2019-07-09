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
from ase.units import Rydberg, Bohr

#print Rydberg, Bohr

fig, axs = plt.subplots(3,1,sharex=True,sharey=False,figsize=(6,8))

dt = dp.getElectronStepLength()

Efield = [[float(i) for i in line.split()] for line in open('TDEFIELD')]
Efield = np.array(Efield)/1E5 *  Rydberg/Bohr
axs[2].plot(Efield)


f = os.popen('grep "!    total energy" result')
energy = np.array([float(line.split()[-2]) for line in f.readlines()])*13.6
#print energy

axs[1].plot(energy - energy[0])

norm, kweight, nocc = dp.readExcitationFile()
excite = (norm - norm[0,:,:])
for ib in range(excite.shape[2]):
    excite[:,:,ib] *= kweight
    #pass
time = np.array(range(excite.shape[0]+1))
step = min(time.shape[0]-1, excite.shape[0])
axs[0].plot(time[1:step+1], (excite[:step,:,:nocc]).sum(axis=(1,2)), label='VB')
axs[0].plot(time[1:step+1], (excite[:step,:,nocc:]).sum(axis=(1,2)), label='CB')


ma.setProperty(axs[0], 
               **ma.getPropertyFromPosition(ylabel='Electrons (e)'))
ma.setProperty(axs[1], 
               **ma.getPropertyFromPosition(ylabel='KS Energy (eV)'))
ma.setProperty(axs[2], 
               **ma.getPropertyFromPosition(xlabel='Time (fs)',
                                            xlimits=[time[1],time[step]],
                                            ylabel='E Field (V/$\AA$)'))   