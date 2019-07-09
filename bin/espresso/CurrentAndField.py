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


    

dt =dp.getElectronStepLength()
nocc = int(float(os.popen('grep "number of electrons" result').readline().split()[-1])/2.0)

fig, axs = plt.subplots(2,2,sharex=True,
                        sharey='row',
                        figsize=(8,6))
#axs = axs.flatten()



idir = [0,1]


for idir in range(2):
    ax = axs[0][idir]
    Afield = np.array([[float(i)/1E5 for i in line.split()] for line in open('TDAFIELD')])
    time = np.array(range(Afield.shape[0]))*dt
    ax.plot(time,Afield[:,idir],'-',label='$A_{ext}$')
    
    Ascreen = np.array([[float(i) for i in line.split()[-3:]] for line in os.popen('grep "Ascreen is " result').readlines()])
    time = np.array(range(Ascreen.shape[0]))*dt
    ax.plot(time,Ascreen[:,idir],'--',label='$A_{ind}$')
    
    f = os.popen('grep "current is " result')
    current = np.array([[float(i) for i in line.split()[-3:]] for line in f.readlines()])
    time = np.array(range(current.shape[0]))*dt
    rescale = (max(Afield[:,idir].max(),Ascreen[:,idir].max())/current[:,idir].max())
    ax.plot(time, current[:,idir]*rescale,'-.',label=r'current $\times$ %3.2f'%(rescale))
    args = ma.getPropertyFromPosition(ylabel=r'$A/c$(a.u.)')
    ma.setProperty(ax,**args)


    ax = axs[1][idir]
    Efield = [[float(i)/1E5 for i in line.split()] for line in open('TDEFIELD')]
    Efield = np.array(Efield)
    time = np.array(range(Efield.shape[0]))*dt
    ax.plot(time,Efield[:,idir],'-',label='$E_{ext}$')
    
    Escreen = [[float(i) for i in line.split()[-3:]] for line in os.popen('grep "Escreen is " result').readlines()]
    Escreen = np.array(Escreen)
    time = np.array(range(Escreen.shape[0]))*dt
    ax.plot(time,Escreen[:,idir],'--',label='$E_{ind}$')
    
    nablaV = [[float(i) for i in line.split()[-3:]] for line in os.popen('grep "nablaV is " result').readlines()]
    nablaV = np.array(nablaV)
    
    time = np.array(range(nablaV.shape[0]))*dt
    rescale = (Afield[:,idir].max()/nablaV[:,idir].max())
    ax.plot(time,nablaV[:,idir],'-.',label=r'$\nabla V$')
    
    args = ma.getPropertyFromPosition(ylabel=r'$E$(a.u.)')
    ma.setProperty(ax,**args)
    
    plt.tight_layout()

SaveName = __file__.split('/')[-1].split('.')[0]
for save_type in ['.png','.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)