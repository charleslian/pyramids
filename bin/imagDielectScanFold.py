#
import numpy as np
from pyramids.plot.setting import getPropertyFromPosition, setProperty, getColors
from pyramids.io.fdf import tdapOptions
import pyramids.io.result as dp
import matplotlib.pyplot as plt
import pyramids.plot.PlotUtility as pu
import os

fig1, axs = plt.subplots(1,1,sharey=True,sharex=True,figsize=(8,6))
peaks = [0]
colors = ['r','g','b','y']
count = 0

def action(index,folder):
  for i, direct in enumerate(['x','y','z']):
      if not os.path.exists(direct):
          continue
      os.chdir(direct)
      energyArray, absorbance, reflect = dp.getImagElectricFunction(i,0.005)
  
      #
      os.chdir('..')
  return folder, energyArray, absorbance

xlimits = [0,25]
ylimits = [0,300]
data = pu.scanFolder(action) 
for index, (folder, energyArray, absorbance) in enumerate(data):
  eFieldStr = float(folder) * 13.6/0.529
  peak = 100 * index
  absorbance /= float(folder)
  axs.fill_between(energyArray, absorbance + peak ,peak, color = colors[index],
                   label=r'%5.2f $V/\AA$'%(eFieldStr),alpha=0.6)

  from scipy.signal import argrelextrema
  extrema = argrelextrema(absorbance, np.greater)
  maxPeakValue = max(absorbance)
  peaks = []
  for extreme in extrema[0]:
    peakPosition, peakValue = energyArray[extreme], absorbance[extreme]
    if peakValue > 0.3 * maxPeakValue and xlimits[0] < peakPosition < xlimits[1]:
      peaks.append((peakPosition,peakValue))
      axs.text(peakPosition, peak + 50,'%3.2f eV' % peakPosition, fontsize='x-large',rotation=-90)
      axs.axvline(peakPosition,1/3.0*index,1/3.0*(index+1),ls='--',lw=2.0,color='k')
      break
peaks = np.array(peaks)  

args = getPropertyFromPosition(xlimits=xlimits, ylimits=ylimits, 
                               yticklabels=[], 
                               legendLoc=2,
                               ylabel='Absorbance',xlabel='Energy(eV)')
setProperty(axs,**args)

plt.tight_layout()
plt.savefig('dielectriFunction.pdf',dpi=600)
