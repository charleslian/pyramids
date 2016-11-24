# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 14:52:50 2016

@author: cl-iop
"""

import numpy as np
import matplotlib.pyplot as plt
import plotSetting as ma
import dataProcess as dP

fig, axs = plt.subplots(1,1,sharex=True,sharey=True)
selectedImage = [50, 100, 200]

colors = ['b','r']
ls = ['-','--']
for axindex, title in enumerate(['WithoutE','WithE']):
  import os
  os.chdir(title)
  ax = axs
  Bands = dP.getEigenFromEig('')
  ax.plot(Bands,ls[axindex],color=colors[axindex],lw=3,alpha=1)
  ax.plot([],ls[axindex],color=colors[axindex],lw=3,alpha=1,label=title)
  kargs=ma.getPropertyFromPosition(ylabel=r'Energy',xlabel=r'',title='', 
                               xticks=None, yticks=None, 
                               xticklabels=None, yticklabels=None,
                               xlimits=None, ylimits=[-2,2])
  ma.setProperty(ax,**kargs)
  os.chdir('..')
  
plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = __file__.split('.')[0]+save_type
  plt.savefig(filename,dpi=600)