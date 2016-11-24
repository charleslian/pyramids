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
for i, direct in enumerate(['x','y','z']):
    if not os.path.exists(direct):
        continue
    os.chdir(direct)
    energyArray, absorbance, reflect = dp.getImagElectricFunction(i,0.0)
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
    
    axs.fill_between(energyArray/8.56,absorbance,0.0,color=colors[i],label=direct,alpha=0.6)
    os.chdir('..')
    
maxPeak = energyArray[np.argmax(absorbanceSum)], np.max(absorbanceSum)
maxMinusPeak = energyArray[np.argmin(absorbanceSum)], np.min(absorbanceSum)

xlimits = [0.1, 8]#maxPeak[0]*1.5] 
ylimits = [0, maxPeak[1]]

from scipy.signal import argrelextrema
extrema = argrelextrema(absorbanceSum, np.greater)
maxPeakValue = max(absorbanceSum)
peaks = []
for extreme in extrema[0]:
  peakPosition, peakValue = energyArray[extreme], absorbanceSum[extreme]
  if peakValue > 0.05 * maxPeakValue:
    peaks.append((peakPosition,peakValue))
    axs.text(peakPosition, maxPeakValue*0.7,'%3.2f' % peakPosition, fontsize='large',rotation=90)

peaks = np.array(peaks)    
#axs.semilogy(energyArray/8.56,absorbanceSum,'-',linewidth=2.,color='black',label='Total',alpha=0.5)
axs.plot(energyArray/8.56,absorbanceSum,'-',linewidth=2.,color='black',label='Total')
args = getPropertyFromPosition(xlimits=xlimits,ylimits=ylimits,
                               ylabel='absorbance',xlabel='energy(eV)')
setProperty(axs,**args)

plt.tight_layout()
#plt.savefig('dielectriFunction.pdf',dpi=600)
