#/usr/bin/python
"""
Created on Fri Jul 22 09:54:42 2016
@author: Chao (Charles) Lian
@email: Charleslian@126.com
"""

import matplotlib.pyplot as plt
from pyramids.io.result import getTDEig
from pyramids.plot.setting import getPropertyFromPosition
from pyramids.plot.setting import setProperty
from pyramids.plot.setting import getColors
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import os
colors = getColors(5)
#ti = 3; tf = 1000; 
#selectTime =range(ti,tf) # initial timestep and final timestep
#selectBand = [0]# initial band and final band
selectKpts = [0]#[0,1,4,6,7]# initial band and final band

numK = len(selectKpts)
fig, axs  = plt.subplots(1,len(selectKpts),sharex=True,figsize=(8,6)) 



#print eig.shape, time.shape,
#for diri, directory in enumerate(['TDDFT','BOMD']):
#os.chdir(directory)
time, eig = getTDEig()
#print time.shape
print eig
for k in selectKpts: 
  if numK == 1:
    ax = axs
  else:
    ax = axs[k]
  ax.plot(time,eig[:,k])
  args = getPropertyFromPosition(k,xlabel='Time(fs)',ylabel='Eigenvalues(eV)',
                                 ylimits=[eig[:,k].min(),0])
  setProperty(ax,**args)

fig.tight_layout() 
saveTypes = ['pdf']
for save_type in saveTypes:
  plt.savefig('Bands.'+save_type,transparent=True,dpi=600)
  