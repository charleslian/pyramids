#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as pu
import os



#------------------------------------------------------------------------------
time, exe = dP.getProjectedPartition()
time, eigen = dP.getAdiabaticEigenvalue()

c = ma.getColors(exe.shape[2], cmap='brg')

kpts = [0]
ylimits=None

if os.path.exists('localSetting.py'):
  import localSetting as ls
  kpts = ls.selectedKPoints.kSet
  ylimits = ls.selectedKPoints.ylimits
  norms = ls.selectedKPoints.norms
  names = ls.selectedKPoints.names
  commonNorm = ls.selectedKPoints.commonNorm

SaveName = __file__.split('/')[-1].split('.')[0] 
fig, axs = plt.subplots(len(kpts),1,sharex=True,sharey=True,figsize=(6*1,3*len(kpts)))



for index, kpt in enumerate(kpts):
  ax = axs[index]
  norm = norms[index]/np.max(exe[:,:,:] -  exe[0,:,:])
  name = names[index]
  
  for i, band in enumerate(eigen[0,kpt,:]):
    if band < 0.0:
      homo = i
  #print homo
  
  evolvingBands = range(1, eigen.shape[-1])
  excited = np.abs(exe[:,kpt,:] - exe[0,kpt,:])
  for i in evolvingBands:
    part = excited[:,i]
    if i <= homo:
      s = ax.fill_between(time, eigen[:,kpt,i] - norm*commonNorm*part, 
                               eigen[:,kpt,i] + norm*commonNorm*part
                               ,lw=0.0,color='b',alpha=0.7)
    else:
      s = ax.fill_between(time, eigen[:,kpt,i] - norm*commonNorm*part, 
                               eigen[:,kpt,i] + norm*commonNorm*part
                               ,lw=0.0,color='r',alpha=0.7)
    ax.plot(time,eigen[:,kpt,i], lw=1.0, c='k' ,alpha=0.7)
    
#  if norms[index] > 1.0:
#    ax.fill_between([0],[0],label = r'$\times$%3.0f' % norms[index],
#                    lw=0.0,color='r',alpha=0.7)
#    ax.fill_between([0],[0],label = r'$\times$%3.0f' % norms[index],
#                    lw=0.0,color='b',alpha=0.7)                
    #ax.text(0.5,0.9,r'$\times$%3.0f' % norms[index], fontsize='xx-large',
    #        transform=ax.transAxes)
    
  kargs=ma.getPropertyFromPosition(index, ylabel=r'Eigenvalues(eV)',
                                   xlabel='Time(fs)',
                                   title=name, grid=False,
                                   hline=[0.0],
                                   xlimits=[np.min(time),np.max(time)],
                                   ylimits=ylimits)             
  ma.setProperty(ax,**kargs)
#------------------------------------------------------------------------------
  plt.tight_layout()
  for save_type in ['.pdf']:
    filename = SaveName + save_type
    plt.savefig(filename,dpi=400)
