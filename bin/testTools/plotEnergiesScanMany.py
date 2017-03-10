import numpy as np
from matplotlib import pyplot as plt
import pyramids.io.result as dp
from pyramids.plot.PlotUtility import scanFolder
import pyramids.plot.setting as ma
import pyramids.process.struct as pps

#--------------------------------------------------------------------------------------------
def action(index,folder):
  dataCurFolder = []
  dataCurFolder.append([index, folder])
  dataCurFolder.append(dp.getEnergyTemperaturePressure(ave=True))
  dataCurFolder.append(dp.getEField())
  return dataCurFolder
  
#--------------------------------------------------------------------------------------------
fig, axs = plt.subplots(2,1,sharex=True,sharey=False,figsize=(10,8))#
data = scanFolder(action)
c = ma.getColors(len(data))

for line in data:
  index, folder = line[0]
  ax = axs[1]
  cts = ax.plot(line[1][0], line[1][2] - line[1][2][0], lw=3, label=folder, c=c[index])
  kargs=ma.getPropertyFromPosition(xlabel='Time (fs)', ylabel=r'E/atom (eV)', title='Excitation Energy')
  ma.setProperty(ax,**kargs)
  ax = axs[0]
  if index == 5:  
    cts = ax.plot(line[2][0], line[2][1][:,2], lw=1, c=c[index], label = '400 nm')
    kargs=ma.getPropertyFromPosition(xlabel='Time (fs)', ylabel=r'$\varepsilon$ (a.u.)', title='Electric Field') 
  #plt.colorbar(cts,ax=ax)
    ma.setProperty(ax,**kargs)
  #--------------------------------------------------------------------------------------------
  
  
plt.tight_layout()
SaveName = __file__.split('/')[-1].split('.')[0]
if True:
  for save_type in ['.pdf','.png']:
    filename = SaveName + save_type
    plt.savefig(filename,dpi=600)