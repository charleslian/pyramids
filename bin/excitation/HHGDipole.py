#
import numpy as np
from pyramids.plot.setting import getPropertyFromPosition, setProperty, getColors
from pyramids.io.fdf import tdapOptions
import pyramids.io.result as dp
import matplotlib.pyplot as plt
import os


guassFieldEnergy = 6.21 
fig1, axs = plt.subplots(2,1,sharey=False,sharex=False,figsize=(8,10))
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
#      import sys
#      if sys.platform != 'win32':
#          axin, imag = pu.insertStruct(axs, width="50%", height=1.5, loc=6, 
#                                   rotation=rotation, 
#                                   camera='perspective', cell=True)
      count += 1
                 
      absorbanceSum = absorbance*energyArray/4.1356
      absorbanceSumHHG = np.power(absorbance,2)
      absorbanceSumHHG = absorbanceSumHHG*np.power(energyArray/4.1356,4)
    else:
      absorbanceSum += absorbance*energyArray/4.1356
      absorbanceSumHHG += np.power(absorbance,2)
      absorbanceSumHHG += absorbanceSumHHG*np.power(energyArray/4.1356,4)
#    axs.fill_between(energyArray/0.86,absorbance,0.0,color=colors[i],label=direct,alpha=0.6)
    os.chdir('..')
    
maxPeak = energyArray[np.argmax(absorbanceSum)], np.max(absorbanceSum)
maxMinusPeak = energyArray[np.argmin(absorbanceSum)], np.min(absorbanceSum)

xlimits = [0, 8]#maxPeak[0]*1.5] 
ylimits = None#[0, 50]#[0, maxPeak[1]]

from scipy.signal import argrelextrema
extrema = argrelextrema(absorbanceSum, np.greater)
maxPeakValue = max(absorbanceSum)
peaks = []
for extreme in extrema[0]:
  peakPosition, peakValue = energyArray[extreme]/4.3, absorbanceSum[extreme]
  if peakValue > 0.01 * maxPeakValue:
    peaks.append((peakPosition,peakValue))
#    axs.text(peakPosition, maxPeakValue*0.7,'%3.2f' % peakPosition, fontsize='large',rotation=90)

peaks = np.array(peaks)    
axs[0].semilogy(energyArray/guassFieldEnergy,absorbanceSumHHG,'-',linewidth=2.,color='black',label='Total',alpha=0.5)
axs[1].plot(energyArray/guassFieldEnergy,absorbanceSumHHG,'-',linewidth=2.,color='red',label='Total')
args1 = getPropertyFromPosition(xlimits=xlimits,ylimits=ylimits,
                               ylabel='absorbance',xlabel='Order')

args2 = getPropertyFromPosition(xlimits=xlimits,ylimits=None,
                               ylabel='absorbance',xlabel='Order')
setProperty(axs[0],**args1)
setProperty(axs[1],**args2)

#plt.tight_layout()
plt.savefig('HHG.pdf',dpi=600)
