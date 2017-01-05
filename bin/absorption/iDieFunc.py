#
import numpy as np
from pyramids.plot.setting import getPropertyFromPosition, setProperty, getColors
from pyramids.io.fdf import tdapOptions
import pyramids.io.result as dp
import matplotlib.pyplot as plt
import os

fig1, axs = plt.subplots(1,1,sharey=True,sharex=True,figsize=(8,6))
peaks = [0]
colors = ['r','g','b']
count = 0
xlimits = [0,8]
 
for i, direct in enumerate(['x','y','z']):
    if not os.path.exists(direct):
        continue
    os.chdir(direct)
    energyArray, absorbance, reflect = dp.getImagElectricFunction(i,0.015)
    if count == 0:
      import pyramids.plot.PlotUtility as pu
      rotation = [0,0,0]
      import sys
      if sys.platform != 'win32':
          axin, imag = pu.insertStruct(axs, width="50%", height=1.5, loc=6, 
                                   rotation=rotation, 
                                   camera='perspective', cell=True)
      count += 1           
      absorbanceSum = absorbance
    else:
      absorbanceSum += absorbance
      
    xStep = energyArray[1] - energyArray[0]
    xDownIndex, xUpIndex = int(xlimits[0]/xStep), int(xlimits[1]/xStep)  
    
    from scipy.interpolate import interp1d
    spline = interp1d(energyArray[xDownIndex:xUpIndex], 
                      absorbance[xDownIndex:xUpIndex], 
                      kind='cubic')  
                      
    interpX = np.linspace(energyArray[xDownIndex],
                          energyArray[xUpIndex-1], 500)  
    last = spline(interpX)                      
    axs.fill_between(interpX,last,0.0,color=colors[i],label=direct,alpha=0.6)
    os.chdir('..')
    
maxPeak = energyArray[np.argmax(absorbanceSum)], np.max(absorbanceSum)
maxMinusPeak = energyArray[np.argmin(absorbanceSum)], np.min(absorbanceSum)

#xlimits = [0, 3]#maxPeak[0]*1.5] 
#ylimits = [0, maxPeak[1]]
ylimits = [0,np.max(last)]
from scipy.signal import argrelextrema
extrema = argrelextrema(absorbanceSum, np.greater)
maxPeakValue = max(absorbanceSum)
peaks = []
for extreme in extrema[0]:
  peakPosition, peakValue = energyArray[extreme], absorbanceSum[extreme]
  if peakValue > 0.1 * maxPeakValue:
    peaks.append((peakPosition,peakValue))
    axs.text(peakPosition, maxPeakValue*0.5,'%3.2f' % peakPosition, fontsize='large',rotation=90)

peaks = np.array(peaks)    
#axs.plot(energyArray,absorbanceSum,'-',linewidth=3.,color='black',label='Total',alpha=0.5)
args = getPropertyFromPosition(xlimits=xlimits,
                               ylimits=ylimits,
                               ylabel='Absorbance',xlabel='Energy(eV)')
setProperty(axs,**args)

plt.tight_layout()
plt.savefig('dielectriFunction.pdf',dpi=600)
