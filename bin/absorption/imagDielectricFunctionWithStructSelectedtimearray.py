# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 11:15:03 2016

@author: moomin
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 08 10:34:13 2016

@author: moomin
"""

import numpy as np
from scipy.fftpack import fft, ifft
from pyramids.plot.setting import getPropertyFromPosition, setProperty, getColors
from pyramids.io.fdf import tdapOptions
import pyramids.io.result as dp
import matplotlib.pyplot as plt
import os


fig1, axs = plt.subplots(1,1,sharey=True,sharex=True,figsize=(8,5))
peaks = [0]
colors = ['r','g','b']
count = 0
for i, direct in enumerate(['x','y','z']):
    if not os.path.exists(direct):
        continue
      
    os.chdir(direct)
    timeArray, efield = dp.getEField()  
    
    option = tdapOptions()
    lengthTime = option.tdTimeStep[0]
    numStep =  option.tdFinalStep - 3200
    
    timeArray = (timeArray[1600:2400]-1600*lengthTime)/option.tdTimeStep[0]
    time, dipole = dp.getDipolePython()
      
    dipole = dipole[1600:2400,i]
                              
    freqResolution = 1.0/(lengthTime*numStep)
    freqArray = (timeArray-(numStep/2.0))*freqResolution
    
    energyArray = freqArray*4.1356
    energyArray = energyArray[numStep/2:]
    
    epsilon = fft(dipole)[:numStep/2] 
    epsilon = (np.real(epsilon),np.imag(epsilon))
    
    absorbance = np.abs(epsilon[0])
    if count == 0:
      import pyramids.plot.PlotUtility as pu
      rotation = [0,0,0]
      #rotation[i] = 90
      import sys
      if sys.platform != 'win32':
          axin, imag = pu.insertStruct(axs, width="50%", height=1.5, loc=6, 
                                   rotation=rotation, 
                                   camera='perspective', cell=True)
      count += 1           
      absorbanceSum = absorbance
    else:
      absorbanceSum += absorbance
    
    axs.fill_between(energyArray/1.91,absorbance,linewidth=0.0,color=colors[i],label=direct,alpha=0.6)
    os.chdir('..')
    

maxPeak = energyArray[np.argmax(absorbanceSum)], np.max(absorbanceSum),  
xlimits = [0,10]   
ylimits = [0, 1800]
peaks = []
for j in range(1,len(absorbanceSum)-1):
    if energyArray[j] > xlimits[0] and energyArray[j] < xlimits[1]:    
        if absorbanceSum[j] >= absorbanceSum[j-1] and absorbanceSum[j] >= absorbanceSum[j+1]:
            if absorbanceSum[j] > 0.1*maxPeak[1]: # energyArray[j] < 22.0 and  
                peaks.append(energyArray[j])
            #print energyArray[j], absorbanceSum[j]
for peak in peaks:
  axs.text(peak, maxPeak[1]*0.5,'%3.2f' % peak,fontsize='large',rotation=90)
  
axs.plot(energyArray/1.91,absorbanceSum,'-',linewidth=1.,color='black',label='Total')
args = getPropertyFromPosition(xlimits=xlimits,ylimits=ylimits,
                               ylabel='Absorbance',xlabel='Energy(eV)',vline=peaks)
setProperty(axs,**args)

plt.tight_layout()
plt.savefig('dielectriFunction.pdf',dpi=600)
#plt.plot(2*np.real(y))