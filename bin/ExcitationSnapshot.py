#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
from pyramids.io.fdf import tdapOptions
import pyramids.io.result as dP
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as pu
import os
import localSetting


#------------------------------------------------------------------------------
nCol = 2
ls = localSetting.snapshot

nRow = len(ls.selectedTimeStep)/nCol
fig, axs = plt.subplots(nRow,nCol,sharex=False,sharey=True,figsize=(3*nCol,3*nRow))
axs = axs.flatten()
SaveName = __file__.split('/')[-1].split('.')[0] 

kpath = ls.kpath
cut = ls.cut
print kpath
specialKPoints = ls.specialKPoints

x = ls.x

homo = dP.getHomo()
evolvingBands = range(0, homo + 7)

time, exe = dP.getProjectedPartition()
time, eigen = dP.getAdiabaticEigenvalue()
colors = ma.getColors(5,cmap='gnuplot') 

for index, step in enumerate(ls.selectedTimeStep):
  excited = np.abs(exe[step,kpath,:] - exe[0,kpath,:])
  norm = ls.norm/np.max(exe[:,kpath,:] - exe[0,kpath,:])
  eigenvalue = eigen[step,kpath,:]
  ax = axs[index]
  for i in evolvingBands:
    if i < homo:
      part = excited[:,i]
      if ls.drawfill:
        s = ax.fill_between(x, eigenvalue[:,i] - norm*part, 
                            eigenvalue[:,i] + norm*part,
                            lw=0.0,color='b',alpha=0.7)
      else:                    
        ax.scatter(x,eigenvalue[:,i],s=norm*part,c='b',)                    
    else:
      part = excited[:,i]
      if ls.drawfill:
        s = ax.fill_between(x, eigenvalue[:,i] - norm*part, 
                            eigenvalue[:,i] + norm*part,
                            lw=0.0,color='r',alpha=0.7)
      else:  
        ax.scatter(x,eigenvalue[:,i],s=norm*part,c='r')
                 
    ax.plot(x, eigenvalue[:,i],'-',lw=1.5,c='k',alpha=0.7)  
    
  if index/nCol == nRow -1 :
    xticklabels = specialKPoints
  else:
    xticklabels=[]
  kargs=ma.getPropertyFromPosition(index,
                                   title=str(time[step]) +' fs',
                                   ylabel=r'Eigen(eV)', grid = False,
                                   xlabel='',
                                   xticks=cut,
                                   ylimits=ls.ylimits,
                                   xticklabels=xticklabels,
                                   xlimits=[cut[0],cut[-1]],
                                   vline=cut,
                                   hline=[0.0])          
  ma.setProperty(ax,**kargs)
#------------------------------------------------------------------------------
plt.tight_layout()
for save_type in ['.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=400)

#view(atom)
#print get_special_points('hexagonal',hexagonal.Graphene('C',latticeconstant=(1.42,10)).cell)
#coor = [(0.5, 0.5, 0), (0,0,0), 
#GXW = [points[k] for k in 'GXW']
#n = int(np.sqrt(nkpts*2))
#for i in range(n,n*(n/2-2),n-1):
#  print i
#  kpath.append(i)
#  kpath.append(i-1)
#cut.append(len(kpath))
