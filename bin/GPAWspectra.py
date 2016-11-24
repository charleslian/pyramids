import numpy as np
import matplotlib.pyplot as plt
from pyramids.plot.setting import getPropertyFromPosition, setProperty
from gpaw.tddft import photoabsorption_spectrum
import os

print os.path.abspath('.')
name= os.path.abspath('.').split('/')[-1]

fig,ax = plt.subplots(1,1,figsize=(6, 6 / 2 ** 0.5))
colors = ['r','g','b']
direct = ['x','y','z']
for i in range(3):
  photoabsorption_spectrum(name+str(i)+'.dm', name+str(i)+'.spec', width=0.5)
  data = np.loadtxt(name+str(i)+'.spec')
  ax.plot(data[:, 0], data[:, 1], colors[i],label=direct[i])
  setProperty(ax,**getPropertyFromPosition(title=r'Absorption spectrum of '+name,
                                           xlabel='eV',
                                           ylabel='Absorption (arbitrary units)'))

plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = name + save_type
  plt.savefig(filename,dpi=600)