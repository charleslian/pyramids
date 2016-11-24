# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 14:52:50 2016

@author: cl-iop
"""

import numpy as np
import matplotlib.pyplot as plt
import plotSetting as ma
import dataProcess as dP

SaveName = 'FloquetBand'
Bands = dP.loadSaved(SaveName)

if len(Bands) == 0:
  print 'Calculation'
  Bands = dP.getEigenFromEig('3td')
  All = range(4,2000)
  for step in All:
    Bands += dP.getEigenFromEig(str(step)+'td')
  Bands = Bands/(len(All)+1)
  np.save(SaveName,Bands)


fig, axs = plt.subplots(1,4,sharex=True,sharey=True)
selectedImage = [50, 100, 200]
for axindex in range(4):
  ax = axs.flatten()[axindex]
  if axindex != 3:
    BandsPlot = dP.getEigenFromEig(str(selectedImage[axindex])+'td')
    title = 'Step = ' + str(selectedImage[axindex])
  else:
    BandsPlot = Bands
    title = 'Floquet'
  ax.plot(BandsPlot,'-b',lw=3)
  kargs=ma.getPropertyFromPosition(ylabel=r'Energy',xlabel=r'',title=title, 
                               xticks=None, yticks=None, 
                               xticklabels=None, yticklabels=None,
                               xlimits=None, ylimits=[-3,3])
  ma.setProperty(ax,**kargs)

plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = __file__.split('.')[0]+save_type
  plt.savefig(filename,dpi=600)
  import os
  os.popen('mv '+filename+' /home/lianchao/Workdir/Figures/')