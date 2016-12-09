import numpy as np
from matplotlib import pyplot as plt
import pyramids.io.result as dp
from pyramids.plot.PlotUtility import scanFolder
import pyramids.plot.setting as ma


fig, axs = plt.subplots(1,1,sharex=True,sharey=False,figsize=(8,6))#

#--------------------------------------------------------------------------------------------
ax = axs
selectTime, berry = dp.getBerry()
time, Efield = dp.getEField()
directions = ['x', 'y', 'z','x-','y-','z-']
for direction in range(3):
  #print direction
  sumBerry = np.sum((berry[:,:,direction] - berry[:,:,direction+3]),axis=1)%(2.0*np.pi) #/(2.0*np.pi)  #%(2.0*np.pi)  / (2.0*np.pi) 
  #print sumBerry
  if np.max(sumBerry) > 1E-10:
    E = Efield[:,direction][1:] - Efield[:,direction][:-1]
    A = Efield[:,direction]
    for i in range(1,sumBerry.shape[0]):
      if sumBerry[i] - sumBerry[i-1] > np.pi:
        sumBerry[i] -= 2.0*np.pi
    d = directions[direction]
    ax.plot(selectTime,sumBerry,'-o',lw=3, label='$\Gamma_'+d+'$')
    multiplierE = np.max(sumBerry)/np.max(E)
    multiplierA = np.max(sumBerry)/np.max(A)
    elabel = '$E_' + d +'$'
    alabel = '$A_' + d +'$'
    ax.plot(time[:-1], E*multiplierE,'-',label=elabel, lw=3)
    #ax.plot(time, A*multiplierA + 4*np.max(sumBerry),'-',label=alabel, lw=3)
  
kargs=ma.getPropertyFromPosition(xlabel='Time (fs)', #ylabel=r'$\Gamma$', 
                                 title='Vector Field and Berry Phase')
ma.setProperty(ax,**kargs)
ax.ticklabel_format(style='sci',axis='y',scilimits=[0,0])


#--------------------------------------------------------------------------------------------
plt.style.use('ggplot')
plt.ticklabel_format(style='sci',scilimits=(-2,2))
plt.tight_layout()
SaveName = __file__.split('/')[-1].split('.')[0]
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)

