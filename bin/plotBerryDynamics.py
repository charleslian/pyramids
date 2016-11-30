import numpy as np
from matplotlib import pyplot as plt
import pyramids.io.result as dp
from pyramids.plot.PlotUtility import scanFolder
import pyramids.plot.setting as ma
#import matplotlib
plt.style.use('ggplot')
#plt.xkcd()



selectTime, berry = dp.getBerry()
fig, axs = plt.subplots(2,1,sharex=True,sharey=False,figsize=(8,6))#
ax = axs[0] 
directions = ['x', 'y', 'z','x-','y-','z-']
for direction in range(3):
  #print direction
  sumBerry = np.sum(berry[:,:,direction],axis=1)%(2.0*np.pi) #/(2.0*np.pi)  #%(2.0*np.pi)  / (2.0*np.pi) 
  print sumBerry
  if np.max(sumBerry) > 1E-10:
    for i in range(1,sumBerry.shape[0]):
      if sumBerry[i] - sumBerry[i-1] > np.pi:
        sumBerry[i] -= 2.0*np.pi
    #for index in range(3):
    ax.plot(selectTime,sumBerry,'-o',label=directions[direction])
  
ax.get_xaxis().get_major_formatter().set_powerlimits([-1,2])
kargs=ma.getPropertyFromPosition(ylabel=r'Polarization', xlabel='Time (fs)',
                                 title='')
ma.setProperty(ax,**kargs)
ax.ticklabel_format(style='sci',axis='y',scilimits=[0,0])

ax = axs[1]
time, Efield = dp.getEField()
directions = ['x', 'y', 'z']
for direct in range(3):
  if np.max(Efield[:,direct]) > 1E-10:
    E = Efield[:,direct][1:] - Efield[:,direct][:-1]
    ax.plot(time[:-1], E/time[1] ,'o',
            label='E' + directions[direct],lw=2,alpha=0.8) 
    ax.plot(time, Efield[:,direct], '-',
            label='A' + directions[direct],lw=2,alpha=0.8) 
    
kargs=ma.getPropertyFromPosition(ylabel=r'$\varepsilon$(a.u.)',xlabel='Time(fs)',
                                 title='Electric Field')
ma.setProperty(ax,**kargs)


plt.tight_layout()
SaveName = __file__.split('/')[-1].split('.')[0]
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)
#for direct in range(3):
#  axs[direct].plot(np.sum(berry[direct]))


