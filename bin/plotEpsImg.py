# -*- coding: utf-8 -*-
import pyramids.io.result as dp
import pyramids.plot.setting as ma

SaveName = __file__.split('/')[-1].split('.')[0]
from matplotlib import pyplot as plt
import numpy as np
fig, ax = plt.subplots(1,1,sharex=True,sharey=False,figsize=(8,6))
data = dp.readEpsilonImaginary()
from scipy.signal import argrelextrema
extrema = argrelextrema(data, np.greater)
#print peaks[0]
maxPeakValue = max(data[:,1])
peaks = []
for extreme in extrema[0]:
  peakPosition, peakValue = data[extreme,0], data[extreme,1]
  if peakValue > 0.1 * maxPeakValue:
    peaks.append((peakPosition,peakValue))
    ax.text(data[extreme,0], maxPeakValue*0.5,'%3.2f' % data[extreme,0],fontsize='large',rotation=90)

peaks = np.array(peaks)
ax.fill_between(data[:,0], data[:,1], 0.0, alpha=0.5,lw=3)
args=ma.getPropertyFromPosition(xlabel='Energy(eV)',
                                ylabel='Absorbance',)
ma.setProperty(ax,**args)
for save_type in ['.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)