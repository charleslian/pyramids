# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 06:50:11 2015
For All Electron potential plot in pseudopotential generation
@author: cl-iop
"""
import numpy as np
import matplotlib.pyplot as plt
from pyramids.plot.setting import getColors
from pyramids.plot.setting import A4_LANDSCAPE
from pyramids.plot.setting import getPropertyFromPosition
from pyramids.plot.setting import setProperty
import os
fig=plt.figure(figsize=A4_LANDSCAPE)#_LANDSCAPE
plt.subplots_adjust(left=0.1, bottom=0.10, right=0.95, top=0.95, wspace=0.3, hspace=0.05)

axs = [fig.add_subplot(2,1,1),
      fig.add_subplot(2,1,2)]

colors = getColors(4)
chargeData=np.loadtxt('AECHARGE')
kargs=getPropertyFromPosition(1,'Charge(e)',r'r($\AA$)')
axs[0].plot(chargeData[:,0],chargeData[:,1],':',linewidth=3,label='Down',color=colors[1])
axs[0].plot(chargeData[:,0],chargeData[:,2],'--',linewidth=3,label='Up',color=colors[2])
axs[0].plot(chargeData[:,0],chargeData[:,3],'-',linewidth=3,label='Core',color=colors[0])
axs[0].legend(fontsize=16,loc=1)
kargs['xlimits'] = [0,6]
kargs['xticklabels'] = []
setProperty(axs[0],**kargs)

numWFfiles=int(os.popen('ls AEWFNR* |wc -l').readline())

print numWFfiles
waveData = []
lineTypes=['-','--',':']
orbitalType=['s','p','d','f']
for indexFile in range(min(numWFfiles,3)):
  waveData=np.loadtxt('AEWFNR'+str(indexFile))
  axs[1].plot(waveData[:,0],waveData[:,1],lineTypes[indexFile],linewidth=3,label=orbitalType[indexFile],color=colors[indexFile])


kargs=getPropertyFromPosition(2,'Wavefunction',r'r($\AA$)')
axs[1].legend(fontsize=16,loc=1)
kargs['xlimits'] = [0,15]
setProperty(axs[1],**kargs)
