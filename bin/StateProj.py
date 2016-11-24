#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dP
import pyramids.plot.setting as ma

#------------------------------------------------------------------------------
fig, axs = plt.subplots(3,1,sharex=True,sharey=False,figsize=(6,8))
SaveName = __file__.split('/')[-1].split('.')[0]

time, exe = dP.getProjectedPartition()
time, eigen = dP.getAdiabaticEigenvalue()
ax = axs[0]
homo = dP.getHomo()

c = ma.getColors(exe.shape[2] - homo + 1,cmap='brg')
for i in range(homo-3,homo+2):
  norm = 5E4
  if i < homo:
    part = 2.0 - exe[:,0,i]
  else:
    part = exe[:,0,i]
  ax.scatter(time,eigen[:,0,i],s=norm*part, cmap='Greens',
             marker='o',lw=0, c=part ,alpha=0.8)
  ax.plot(time,eigen[:,0,i], lw=1, c='grey' ,alpha=0.8)
  
kargs=ma.getPropertyFromPosition(ylabel=r'Eigenvalues(eV)',
                                 title='Population')
print exe[-1,0,:]
pu.insertStruct(ax, width="50%", height=1, loc=1, 
                rotation=[-90,90,0], 
                camera='perspective', cell=False)
ma.setProperty(ax,**kargs)
#------------------------------------------------------------------------------
Time, exe = dP.getExcitedElectrons()
ax = axs[1]
ax.plot(Time,exe,'-',alpha=0.8,c=c[0],markerfacecolor='w',lw=2)
kargs=ma.getPropertyFromPosition(ylabel=r'n(e)',
                                 title='Excited Electrons', 
                                 xlimits=None,)
                                 #ylimits=[exe.min(),exe.max()])
print exe[-1]
ma.setProperty(ax,**kargs)
#------------------------------------------------------------------------------
ax = axs[2]
time, Efield = dP.getEField()
directions = ['x', 'y', 'z']
c = ma.getColors(3,cmap='brg')
for direct in range(3):
  ax.plot(time,Efield[:,direct] ,c=c[direct],
          label=directions[direct],lw=2,alpha=0.8) 

kargs=ma.getPropertyFromPosition(ylabel=r'$\varepsilon$(Ry/Bohr)',
                                 xlabel='Time(fs)',
                                 title='Electric Field',
                                 xlimits=[np.min(time),np.max(time)])         
          
ma.setProperty(ax,**kargs)
#------------------------------------------------------------------------------
plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)