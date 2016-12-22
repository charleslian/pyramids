import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dp
from pyramids.io.fdf import tdapOptions
import pyramids.plot.setting as ma

#------------------------------------------------------------------------------
fig, axs = plt.subplots(1,2,sharex=False,sharey=False,figsize=(8,6))
SaveName = __file__.split('/')[-1].split('.')[0] 
homo = dp.getHomo()
time, exe = dp.getProjectedPartition()
time, eigen = dp.getAdiabaticEigenvalue()
print eigen.shape
option = tdapOptions()

import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dp
import pyramids.plot.setting as ma
import pyramids.plot.PlotUtility as pu
import os

from ase.dft.kpoints import special_paths, special_points

ax = axs[1]
import pyramids.plot.PlotUtility as pu
pu.plotEField(ax)

timeE, Efield = dp.getEField()
lightScat, = ax.plot(0,Efield[0,0],'o')
kargs=ma.getPropertyFromPosition(xlabel=r'Time',ylabel=r'EField')
ma.setProperty(ax,**kargs)

ax = axs[0]
kpath = np.arange(exe.shape[1])
x = kpath
#print list(kpath+1)
evolvingBands = range(exe.shape[2])


excited = np.abs(exe[1,kpath,:] -  exe[0,kpath,:])
norm = 100.0/np.max(exe[:,kpath,:] -  exe[0,kpath,:])
eigenvalue = eigen[0,kpath,:]

#print eigenvalue.shape, excited.shape, x.shape

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
    
       
  l, = ax.plot(x, eigenvalue[:,band],'-',lw=0.2,c='k')
  line.append(l)
  

#plt.axis('tight')
timeText = ax.text("1",0,4,fontsize='xx-large')             
kargs=ma.getPropertyFromPosition(ylabel=r'Eigenvalues(eV)',
                                 xlabel='', 
                                 title='Population',
                                 hline=[0.0],)         
ma.setProperty(ax,**kargs)

plt.tight_layout()

from matplotlib import animation
def update(num):
    """updates the horizontal and vertical vector components by a
    fixed increment on each frame
    """
    cycle = eigen.shape[0]
    step  = num%cycle
    timeText.set_text('%4.2f fs'%(time[step]))
    eigenvalue = eigen[step,kpath,:] 
    excited = np.abs(exe[step,kpath,:] -  exe[0,kpath,:])
    cycle = exe.shape[0]
    
    for i, band in enumerate(evolvingBands):
      line[i].set_data(x,eigenvalue[:,band])
      part = excited[:,band]
      if band < homo:
        scatter[i].remove()
        scatter[i] = ax.scatter(x,eigenvalue[:,i],s=norm*part,c='b',)
      else:
        scatter[i].remove()
        scatter[i] = ax.scatter(x,eigenvalue[:,i],s=norm*part,c='r')
    
    for direct in range(3):
      if max(Efield[:,direct]) > 1E-10:
        estep = int(time[step]/option.tdTimeStep[0])
        lightScat.set_data(time[step],Efield[estep,direct])

anim = animation.FuncAnimation(fig, update, interval=1,frames=800, blit=False)
#anim.save(SaveName+'.mp4',dpi=300)                              
#------------------------------------------------------------------------------

