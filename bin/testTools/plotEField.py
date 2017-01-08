#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyramids.io.result as dp
import pyramids.plot.setting as ma

time, Efield = dp.getEField()
fig, axs = plt.subplots(1,1,sharex=True,sharey=True)
ax = axs

# print Efield
# Plot Block #
for i in range(3):
  if np.max(np.abs(Efield[:,i])) > 1E-7:  
    ax.plot(time,Efield[:,i],label=i)
#ax.plot(time,Efield[:,1],label='y')
#ax.plot(time,Efield[:,2],label='z')
#ax.plot(Efield)

kargs=ma.getPropertyFromPosition(ylabel=r'E(a.u.)',xlabel='',title='', 
                               xticks=None, yticks=None, 
                               xticklabels=None, yticklabels=None,
                               xlimits=None, ylimits=None)

ma.setProperty(ax,**kargs)

plt.tight_layout()

SaveName = __file__.split('/')[-1].split('.')[0]
for save_type in ['.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)
