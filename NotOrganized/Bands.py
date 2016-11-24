# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/lianchao/.spyder2/.temp.py
"""

import numpy as np
import matplotlib.pyplot as plt
import dataProcess as dP
import plotSetting as ma

fig, axes = plt.subplots(1,1,sharex=True,sharey=True)
ax = axes

#---------------------------Ploting Block-----------------------------#
bands = dP.getEigenFromEig('400td')
ax.plot([],'-g',lw=2,label='400 td')
ax.plot(bands,'-g',lw=2)

bands = dP.getEigenFromEig('400')
ax.plot([],'--b',lw=2,label='400 diag')
ax.plot(bands,'--b',lw=2)

bands = dP.getEigenFromEig('10')
ax.plot([],'or',alpha=0.5,label='0 diag')
ax.plot(bands,'or',alpha=0.5)
#---------------------------Ploting Block-----------------------------#

kargs=ma.getPropertyFromPosition(ylabel=r'E(eV)',xlabel=r'',title='', 
                               xticks=None, yticks=None, 
                               xticklabels=[r'$\Gamma$','','','','',r'X'], yticklabels=None,
                               xlimits=None, ylimits=[-2,2])

ma.setProperty(ax,**kargs)
plt.tight_layout()
for save_type in ['pdf','png']:
  plt.savefig('Bands.'+save_type,dpi=600)

