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
fig, ax = plt.subplots(1,1,sharex=False,sharey=True,figsize=(8,6))
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

#for index, step in enumerate(ls.selectedTimeStep):
excited = np.abs(exe[0,kpath,:] - exe[0,kpath,:])
norm = ls.norm/np.max(exe[:,kpath,:] - exe[0,kpath,:])
eigenvalue = eigen[0,kpath,:]
line = [] 
scatter = []
for i in evolvingBands:
  if i < homo:
    part = excited[:,i]
    if ls.drawfill:
      s = ax.fill_between(x, eigenvalue[:,i] - norm*part, 
                          eigenvalue[:,i] + norm*part,
                          lw=0.0,color='b',alpha=0.7)
    else:                    
      scatter1 = ax.scatter(x,eigenvalue[:,i],s=norm*part,c='b',)                    
  else:
    part = excited[:,i]
    if ls.drawfill:
      s = ax.fill_between(x, eigenvalue[:,i] - norm*part, 
                          eigenvalue[:,i] + norm*part,
                          lw=0.0,color='r',alpha=0.7)
    else:  
      scatter1 = ax.scatter(x,eigenvalue[:,i],s=norm*part,c='r')
               
  line1 = ax.plot(x, eigenvalue[:,i],'-',lw=1.5,c='k',alpha=0.7)  
  line.append(line1)
  scatter.append(scatter1)
#if index/nCol == nRow -1 :

xticklabels = specialKPoints
#else:
#  xticklabels=[]
kargs=ma.getPropertyFromPosition(
                                 ylabel=r'Eigen(eV)', grid = False,
                                 xlabel='',
                                 xticks=cut,
                                 ylimits=ls.ylimits,
                                 xticklabels=xticklabels,
                                 xlimits=[cut[0],cut[-1]],
                                 vline=cut,
                                 hline=[0.0])          
ma.setProperty(ax,**kargs)
#timeText = ax.text("1",0,4,fontsize='xx-large') 
#------------------------------------------------------------------------------
from matplotlib import animation
def update(num):
    """updates the horizontal and vertical vector components by a
    fixed increment on each frame
    """
    cycle = exe.shape[0]
    
    #x = np.arange(kpath.shape[0])
    print num,
    #timeText.set_text(str(num%cycle*option.tdTimeStep[0])+' '+option.tdTimeStep[1])
    #eigenvalue = eigen[num%cycle,kpath,:] 
    excited = np.abs(exe[num%cycle,kpath,:] -  exe[0,kpath,:])
    for i, band in enumerate(evolvingBands):
      #line[i].set_data(x,eigenvalue[:,band])
      part = excited[:,band]
      if band < homo:
        scatter[i].remove()
        scatter[i] = ax.scatter(x,eigenvalue[:,i],s=norm*part,c='b',)
      else:
        scatter[i].remove()
        scatter[i] = ax.scatter(x,eigenvalue[:,i],s=norm*part,c='r')
    
anim = animation.FuncAnimation(fig, update, interval=40, blit=False)
anim.save(SaveName+'.mp4',dpi=300)
