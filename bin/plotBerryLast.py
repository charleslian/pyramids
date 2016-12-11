#!/usr/bin/python
import numpy as np
from matplotlib import pyplot as plt
import pyramids.io.result as dp
from pyramids.plot.PlotUtility import scanFolder
import pyramids.plot.setting as ma
plt.style.use('ggplot')
def action(index, folder):
  berry = dp.readBerryFile(str(dp.getBerrySteps()[-1]))
  return index, folder, np.array([np.sum(berry[:,direct]) for direct in range(6)])
  

data = scanFolder(action)

x = []
y = []
ax = plt.subplot(111) #, projection='polar'
for index, folder, berry in data:
  x.append(float(folder))
  y.append(berry%(2*np.pi))

y = np.array(y)
#print y
labels = ['x','y','z']
for index in range(3):
  ax.plot(x,y[:,index],'-o',label = labels[index])
ax.get_xaxis().get_major_formatter().set_powerlimits([-1,2])
kargs=ma.getPropertyFromPosition(ylabel=r'Polarization', xlabel='Vector Field (Bohr$^{-1}$)',
                                 title='')
ma.setProperty(ax,**kargs)
plt.tight_layout()

SaveName = __file__.split('/')[-1].split('.')[0]
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,dpi=800)
#for direct in range(3):
#  axs[direct].plot(np.sum(berry[direct]))


