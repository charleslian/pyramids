#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 06:28:23 2016

@author: cl-iop
"""
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dp
import pyramids.plot.setting as ma
numSample = 20
thetas = np.linspace(0,np.pi/2.0,numSample)
x = 0.2*np.sin(thetas)
y1 = np.load('intense.npy')
y2 = np.load('angle.npy')
fig, ax = plt.subplots(1,1,sharex=False,sharey=False,figsize=(8,6))
ax.plot(x,y1,'-',label = 'intense')
ax.plot(x,y2,'o',label = 'angle')
kargs = ma.getPropertyFromPosition(ylabel=r'', xlabel=r'$A \sin\theta$',title='')
ma.setProperty(ax,**kargs)

plt.tight_layout()
SaveName = __file__.split('/')[-1].split('.')[0] 
for save_type in ['.pdf']:
  plt.savefig(SaveName+save_type,transparent=True,dpi=600)