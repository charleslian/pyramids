# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 17:06:35 2016

@author: cl-iop
"""
import numpy as np
import matplotlib.pyplot as plt


fig, axs = plt.subplots(2,2,sharex=True,sharey=True)


# Plot Block #
frequencies = np.linspace(1,4,4)
t = np.linspace(0.0,1.0,201)
for i,f in enumerate(frequencies):  
  ax = axs.flatten()[i]
  E = np.cos(2.0*np.pi*f*t)
  ax.plot(t,E)

  import plotSetting as ma
  kargs=ma.getPropertyFromPosition(ylabel=r'E(V/$\AA$)',xlabel='Time(fs)',
                                   title='F='+str(f)+'(/fs)', 
                               xticks=None, yticks=None, 
                               xticklabels=None, yticklabels=None,
                               xlimits=None, ylimits=None)

  ma.setProperty(ax,**kargs)

plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = __file__.split('.')[0]+save_type
  plt.savefig(filename,dpi=600)
  #import os
  #os.popen('mv '+filename+' /home/lianchao/Workdir/Figures/')
