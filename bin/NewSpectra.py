# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 12:59:03 2016

@author: cl-iop
"""

import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dp
import pyramids.plot.setting as ma
import os


fig, axs = plt.subplots(2,1,sharex=False,sharey=False,figsize=(6,8))
SaveName = __file__.split('/')[-1].split('.')[0]

startStep = 10
c = ma.getColors(4)
scandir = ('x','y')
for idir, direct in enumerate(scandir):
  os.chdir(direct)  
  
  ax = axs[0]
  time, T, E_ks, E_tot, Vol, P  = dp.getEnergyTemperaturePressure()
  dipoles = dp.getDipole()
  dipoles[:,idir] = (dipoles[:,idir] - dipoles[0,idir]) #* np.exp(-0.01*time)
  ax.plot(time,dipoles[:,idir],label=direct)
  ax.grid(which=u'major',axis='x')
  ax.grid(which=u'major',axis='y')
  
  ax = axs[1]
  N = dipoles.shape[0]
  timeStep = (time[-1] - time[0]) / (N-1)
  
  omega = np.linspace(0,70,1000)
  absorbance = np.abs([np.imag(io*np.sum(np.exp(1j*io*np.arange(N)*timeStep)*dipoles[:,idir])) for io in omega])

  energy = 1245.0/(300*2*np.pi)*omega
  #plt.fill_between(energy, absorbance,label=direct, color=c[idir],alpha=0.3)
  if idir == 0:
    omegaAve = absorbance/3.0
  else:
    omegaAve += absorbance/3.0
  if idir == len(scandir) -1 :
    ax.fill_between(energy, omegaAve, label='Averaged', color=c[3],alpha=0.5)
  ax.ticklabel_format(style='sci',axis='y',scilimits=[0,0])
  ax.grid(which=u'major',axis='x')
  ax.grid(which=u'major',axis='y')
  os.chdir('..') 
  
kargs=ma.getPropertyFromPosition(ylabel=r'Dipole(a.u)',
                                 xlabel='Time(fs)')
ma.setProperty(axs[0],**kargs)



kargs=ma.getPropertyFromPosition(ylabel=r'Absorbance(.a.u.)',
                                 xlabel=r'Energy(eV)',
                                 xlimits=[0,10])
                                 #ylimits=[0,0.2E2])
ma.setProperty(axs[1],**kargs)
                                 

plt.tight_layout()
#ma.setProperty(axs[0,1],**kargs)
