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

time, Efield = dp.getEField()
#print Efield
lightScat, = ax.plot(0,Efield[0,0],'o')

kargs=ma.getPropertyFromPosition(xlabel=r'Time',ylabel=r'EField')
ma.setProperty(ax,**kargs)

#for i, k in enumerate(kpath):
#  n = i/nkx
#  if n % 2 == 1:
#    kpath[i] = 2*n*nkx + nkx - i - 1
ax = axs[0]
kpath = np.arange(exe.shape[1])

from ase.calculators.siesta.import_functions import xv_to_atoms
points = special_points['hexagonal']
points['K1']= [-0.3333, 0.333, 0]
points['K2']= [0.666, 0.333, 0]
kline = ['K2','K1','K2']
xticks, kinfo = dp.findBandPath(xv_to_atoms('siesta.XV'),points,kline,toleAngle=0.001)
kpath = kinfo['uc-index']
x = kinfo['distance']
print x
#print list(kpath+1)
evolvingBands = range(exe.shape[2])


excited = np.abs(exe[1,kpath,:] -  exe[0,kpath,:])
norm = 1000.0/np.max(exe[:,kpath,:] -  exe[0,kpath,:])
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
                                 xlabel='', xticks = xticks, 
                                 vline=xticks,
                                 xticklabels=kline,
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
    timeText.set_text('%4.2f %s'%(step*option.tdTimeStep[0],option.tdTimeStep[1]))
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
        lightScat.set_data(time[step],Efield[step,direct])

anim = animation.FuncAnimation(fig, update, interval=20,frames=800, blit=False)
anim.save(SaveName+'.mp4',dpi=300)                              
#------------------------------------------------------------------------------

