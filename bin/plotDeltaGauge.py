#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 08:43:43 2016

@author: cl-iop
"""

import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
from pyramids.plot.PlotUtility import scanFolder
import os 

os.chdir('Demo/Comp')
time, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure(ave=True)
ref = np.load('ref.npy')

fig, ax = plt.subplots(1,1,sharex=False,sharey=False,figsize=(8,6))
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
axin = inset_axes(ax, width=2.5, height=2, loc=1)

axin.plot(time,E_ks,'-',lw=3,)
axin.plot(time,ref,'-',lw=3,)
axin.fill_between(time,E_ks,ref, color = 'r', alpha=0.8, label=r'$\Delta$')
#axin.text(10.0,-0.10,r'$\Delta$',transform=axin.transAxes,fontsize=100)
#ax.annotate('eqweqweqeqw$\Delta$',(0,0.0),(0,0),fontsize=50,arrowprops={ 'arrowstyle': '->'}) #()
kargs=ma.getPropertyFromPosition(ylabel=r'Total enegy',xlabel='Time', 
                                 xticklabels=[], yticklabels=[]
                                 )
ma.setProperty(axin,**kargs)

def getEnergy(index,folder):
  time, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure(ave=True)
  return index, folder, E_ks
  
def errorFunc(x, A,B):
  return A*np.exp(B/x)
  
os.chdir('../../Data/')
for ufolder in os.listdir('.'):
  if os.path.isdir(ufolder):
    os.chdir(ufolder)
    ax = ax
    data = scanFolder(getEnergy)
    ref = np.load('ref.npy')
    deltaEnergy = np.array([np.average(np.abs(energy - ref)) for index, folder, energy in data])
    #xticks = [ for index, folder, energy in data]
    xdata = np.array([ int(folder) for index, folder, energy in data])
    ax.semilogy(xdata, deltaEnergy,'o-', ms=10, lw=3, label=ufolder, alpha=0.8, mew = 3)
    #from scipy.optimize import curve_fit  
    #popt, pcov = curve_fit(errorFunc, xdata, deltaEnergy)    
    #xfit = np.linspace(xdata[0],xdata[-1],1000)
    #ax.semilogy(xdata, errorFunc(xdata,*popt),'-',lw=3)
    os.chdir('..')
    kargs=ma.getPropertyFromPosition(ylabel=r'$\Delta$ (eV)',xlabel='$N$',
                                     legendLoc=3,
                                     )
    ma.setProperty(ax,**kargs)
    
ax.grid(which='both', axis='both')
plt.tight_layout()
SaveName = __file__.split('/')[-1].split('.')[0]
for save_type in ['.pdf','.eps']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)