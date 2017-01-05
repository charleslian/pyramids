#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
from pyramids.io.fdf import tdapOptions
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as pu

#------------------------------------------------------------------------------
fig, ax = plt.subplots(1,1,sharex=True,sharey=False,figsize=(8,6))
SaveName = __file__.split('/')[-1].split('.')[0] 
homo = dP.getHomo()
time, exe = dP.getProjectedPartition()
time, eigen = dP.getAdiabaticEigenvalue()
option = tdapOptions()

kpath = []
cut = [0]
specialKPoints = [r'$M$',r'$\Gamma$',r'$K$',r'$\Gamma$']
for i in range(667,38,-37):
  kpath.append(i)
cut.append(len(kpath))
for i in range(36,421,35):
  kpath.append(i+1) 
  kpath.append(i) 
cut.append(len(kpath))
for i in range(421,649,38):
  kpath.append(i)
  kpath.append(i+1) 
cut.append(len(kpath))
kpath = np.array(kpath) - 1 

c = ma.getColors(exe.shape[2] - homo + 1,cmap='brg')
evolvingBands = range(0, homo + 9)

x = np.arange(kpath.shape[0])
excited = np.abs(exe[1,kpath,:] -  exe[0,kpath,:])
norm = 2.0/np.max(exe[:,kpath,:] -  exe[0,kpath,:])
eigenvalue = eigen[0,kpath,:]

print eigenvalue.shape, excited.shape, x.shape

line = []
scatter = []
for band in evolvingBands:
  if band < homo:
    part = excited[:,band]
    s = ax.fill_between(x, eigenvalue[:,band] - norm*part, 
                               eigenvalue[:,band] + norm*part,
                               lw=0.0,color='b',alpha=0.7)
    
  else:
    part = excited[:,band]
    s = ax.fill_between(x, eigenvalue[:,band] - norm*part, 
                               eigenvalue[:,band] + norm*part
                               ,lw=0.0,color='r',alpha=0.7)                          
  scatter.append(s)
    
       
  l, = ax.plot(x, eigenvalue[:,band],'--',lw=1.5,c='grey')
  line.append(l)
  

plt.axis('tight')
timeText = ax.text("1",0,4,fontsize='xx-large')             
kargs=ma.getPropertyFromPosition(ylabel=r'Eigenvalues(eV)',
                                 xlabel='',xticks=cut,
                                 xticklabels=specialKPoints,
                                 xlimits=[cut[0],cut[1]],
                                 vline=cut,
                                 title='Population',
                                 hline=[0.0],)         
ma.setProperty(ax,**kargs)

from matplotlib import animation
def update(num):
    """updates the horizontal and vertical vector components by a
    fixed increment on each frame
    """
    cycle = eigen.shape[0]
    x = np.arange(kpath.shape[0])
    print num
    timeText.set_text(str(num%cycle*option.tdTimeStep[0])+' '+option.tdTimeStep[1])
    eigenvalue = eigen[num%cycle,kpath,:] 
    excited = np.abs(exe[num%cycle,kpath,:] -  exe[0,kpath,:])
    for i, band in enumerate(evolvingBands):
      line[i].set_data(x,eigenvalue[:,band])
      part = excited[:,band]
      if band < homo:
        scatter[i].remove()
        scatter[i] = ax.fill_between(x, eigenvalue[:,band] - norm*part, 
                               eigenvalue[:,band] + norm*part,
                               lw=0.0,color='b',alpha=0.7)
      else:
        scatter[i].remove()
        scatter[i] = ax.fill_between(x, eigenvalue[:,band] - norm*part, 
                       eigenvalue[:,band] + norm*part,
                       lw=0.0,color='r',alpha=0.7)
    
anim = animation.FuncAnimation(fig, update, interval=40, blit=False)
anim.save(SaveName+'.mp4',dpi=300)                              
#------------------------------------------------------------------------------

