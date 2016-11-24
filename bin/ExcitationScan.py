#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
from pyramids.io.fdf import tdapOptions 
from pyramids.plot.PlotUtility import scanFolder
#------------------------------------------------------------------------------
efield = 2
exElectron = 0
exEnergy = 1
start = 2

def action(index, folder):
  timeEf, eField = dP.getEField()
  timeEl, exe = dP.getExcitedElectrons()
  exe  -= exe[0]
  timeEn, T, E_ks, E_tot, Vol, P  = dP.getEnergyTemperaturePressure()
  deltaE = E_ks[start:,] - E_ks[2]
  return [(index, folder), (timeEf, eField), (timeEl, exe), (timeEn,deltaE)]
  
#------------------------------------------------------------------------------
fig, axs = plt.subplots(3,1,sharex='col',sharey='row',figsize=(6,8))
SaveName = __file__.split('/')[-1].split('.')[0]

data = scanFolder(action)
c = ma.getColors(data[-1][0][0]+1)

exElectron = 0
exEnergy = 1
exAverage = 2

#option = tdapOptions()
#freq, pulseTime, pulseWidth = option.laserParam[0][:3]

#int((pulseTime + 1.5*pulseWidth)/option.tdTimeStep[0])
#photonEnergy = freq*4.1356


for [(index, folder), (timeEf, eField), (timeEl, exe), (timeEn,deltaE)] in data:
  #waveLength = 300/float(folder)
  #------------------------------------------------------------------------------
  ax = axs[exElectron]
  ax.plot(timeEl,exe,'-',alpha=1.0, c=c[index], 
          label = folder,
          markerfacecolor='w', lw=2,)
  #------------------------------------------------------------------------------
  ax = axs[exEnergy]   
  #------------------------------------------------------------------------------
  print timeEn.shape, deltaE.shape
  ax.plot(timeEn[start:], deltaE,'-',alpha=1.0, c=c[index], 
          markerfacecolor='w', lw=2)
  
  ax = axs[exAverage]
  ax.plot(timeEf[start:], eField[start:,:]*13.6/0.529, '-', 
          alpha=1.0, 
          #c=c[index],
          markerfacecolor='w', lw=2,)
          
#------------------------------------------------------------------
kargs=ma.getPropertyFromPosition(ylabel=r'Excited Electrons $n$(e)',
                                 title='', 
                                 xlimits=None,)
ma.setProperty(axs[exElectron],**kargs)
#---------------------------------------
kargs=ma.getPropertyFromPosition(ylabel=r'Energy $E$(eV)',
                                 title='')
ma.setProperty(axs[exEnergy],**kargs)
#------------------------------------------------------------------
kargs=ma.getPropertyFromPosition(ylabel=r'Electric Field ($V/\AA$)',
                                 #xlimits=[timeEl[0],timeEl[-1]],
                                 xlabel='Time (fs)')         
ma.setProperty(axs[exAverage],**kargs)
#------------------------------------------------------------------

plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)