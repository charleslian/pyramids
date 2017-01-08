import numpy as np
from matplotlib import pyplot as plt
import pyramids.io.result as dp
from pyramids.plot.PlotUtility import scanFolder
import pyramids.plot.setting as ma
import pyramids.process.struct as pps


fig, axs = plt.subplots(2,1,sharex=True,sharey=False,figsize=(6,8))#

def action(index,folder):
  #--------------------------------------------------------------------------------------------
  ax = axs[0]
  dp.getTrajactory()
  time, distance = pps.calculateRMSD()
  ax.plot(time, distance, lw=3)
  kargs=ma.getPropertyFromPosition(xlabel='Time (fs)', ylabel=r'$\langle u \rangle^\frac{1}{2}$ ($\AA$)', 
                                   title='RMSD')
  ma.setProperty(ax,**kargs)
  #ax.ticklabel_format(style='sci',axis='y',scilimits=[0,0])
  #--------------------------------------------------------------------------------------------
  ax = axs[1]
  time, T, E_ks, E_tot, Vol, P  = dp.getEnergyTemperaturePressure()
  ax.plot(time, T, lw=3, label=folder)
  kargs=ma.getPropertyFromPosition(xlabel='Time (fs)', ylabel=r'T (K)', 
                                   title='Temperature')
  ma.setProperty(ax,**kargs)
  #ax.ticklabel_format(style='sci',axis='y',scilimits=[0,0])
  #--------------------------------------------------------------------------------------------

scanFolder(action)
#plt.style.use('ggplot')
#plt.ticklabel_format(style='sci',scilimits=(-2,2))
plt.tight_layout()
SaveName = __file__.split('/')[-1].split('.')[0]
if True:
  for save_type in ['.pdf','.png']:
    filename = SaveName + save_type
    plt.savefig(filename,dpi=600)

