#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import dataProcess as dP
import plotSetting as ma
import os
from matplotlib.collections import LineCollection

fig, axs = plt.subplots(3,1,sharex='col',sharey='none',figsize=(6,8))
axs = axs.flatten()

epsilon0 = 8.85E-12
powerFactor = 0.5*np.sqrt(np.pi/2)*epsilon0

IntenseAll = []
ExcitedAll = []
EnergyAll = []

allFolder = os.popen('ls |sort -n').readlines()
scanFolder = [intense[:-1] for intense in allFolder 
              if intense[0] in [str(j) for j in range(0,10)]]
                
colors = dP.getColors(len(scanFolder))
for index, intense in enumerate(scanFolder):
  os.chdir(intense)
  IntenseAll.append(float(intense)*13.6/0.529)
  print intense,
  #------------------------------------------------------------------------------
  Time, exe = dP.getExcitedElectrons()
  ax = axs[0]

  ExcitedAll.append(exe[-1])
  ax.plot(Time,exe,'-',lw=2,alpha=0.7,color=colors[index],label=intense)
  #------------------------------------------------------------------------------
  ax = axs[1]
  time, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure()
  x=ax.plot(time, E_ks - E_ks[0],'-',lw=2,alpha=0.7,color=colors[index])#,label=intense)
  EnergyAll.append((E_ks[-1] - E_ks[0]))
  #------------------------------------------------------------------------------
  ax = axs[2]
  if(index == len(scanFolder) - 1):
    time, Efield = dP.getEField()
    directions = ['x', 'y', 'z']
    for direct in range(3):
      #if(np.max(Efield[:,direct]) > 0.001):
        ax.plot(time,Efield[:,0]*13.6/0.529,lw=1,alpha=0.6,color='g')
  os.chdir('..')
#------------------------------------------------------------------------------
IntenseAll = np.array(IntenseAll)
EnergyAll  = np.array(EnergyAll)
ExcitedAll = np.array(ExcitedAll)



#---------------------------------------------------------------------------
ma.setProperty(axs[0],
               **ma.getPropertyFromPosition(
               ylabel=r'n(e)',title='Excited Electrons', 
               xlabel='Time(fs)'))
ma.setProperty(axs[1],
               **ma.getPropertyFromPosition(ylabel=r'E(eV)',title='Excitation Energy',
               xlabel='Time(fs)'))
ma.setProperty(axs[2],
               **ma.getPropertyFromPosition(
               ylabel=r'I$_l$(V/$\AA$)',title='Intensity',
               xlabel='Time(fs)'))

plt.tight_layout()
SaveName = __file__.split('/')[-1].split('.')[0]+'t'
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=600)



fig, axs = plt.subplots(3,1,sharex='col',sharey='none',figsize=(6,8))
axs = axs.flatten()
x = IntenseAll**2 * powerFactor * 1E20
axs[0].plot(x,ExcitedAll,'bo-',lw=3,markersize=9,alpha=1)
axs[1].plot(x,EnergyAll,'ro-',lw=3,markersize=9,alpha=1)
axs[2].plot(x,EnergyAll/ExcitedAll,'go-',lw=3,markersize=9,alpha=1)#,markerfacecolor='w'

ma.setProperty(axs[0],
               **ma.getPropertyFromPosition(
               ylabel=r'n(e)',title='(a)Electrons',
               xlabel=r''))     
ma.setProperty(axs[1],
               **ma.getPropertyFromPosition(
               ylabel=r'E(eV)',title='(b)Energy',
               xlabel=r''))
ma.setProperty(axs[2],
               **ma.getPropertyFromPosition(
               ylabel=r'E/$n_e$(eV/e)',title='(c)E/e', ylimits=[30,80],
               xlabel=r'I$_l$(V/$\AA$)'))
plt.tight_layout()
SaveName = __file__.split('/')[-1].split('.')[0]+'i'
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)
