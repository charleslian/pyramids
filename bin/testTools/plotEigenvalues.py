# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 08:02:34 2016

@author: cl-iop
"""
def plotEigenvalues(index,folder):
  import pyramids.io.result as dp
  from pyramids.io.result import getHomo
  eigenvalues = dp.readEigFile()
  x = float(folder)
  y = eigenvalues
  plotedBand = getHomo()
  return x,y,plotedBand

import pyramids.plot.setting as ma
SaveName = __file__.split('/')[-1].split('.')[0]
from matplotlib import pyplot as plt
import numpy as np
fig, ax = plt.subplots(1,1,sharex=True,sharey=False,figsize=(8,6))
from pyramids.plot.PlotUtility import scanFolder

data = scanFolder(plotEigenvalues)
y0 = data[0][1].flatten()
numBand = y0.shape[0]

x = []
y = []
for x1,y1,homo in data:
  x.append(x1)
  y.append(y1.flatten()-y0)
  
y = np.array(y)

plotedBand = homo + 0
colors = ma.getColors(plotedBand)
for i in range(plotedBand):
  ax.plot(x,y[:,i],'-o',color=colors[i],label=str(i)+' + '+str(y0[i]))

args = ma.getPropertyFromPosition(xlabel=r'$\varepsilon(a.u.)$',
                                  ylabel=r'Eigenvalues(eV)')
ma.setProperty(ax,**args)
plt.tight_layout()

for save_type in ['.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)