import numpy as np
import matplotlib.pyplot as plt
from pyramids.plot.setting import getPropertyFromPosition, setProperty
from gpaw.tddft import photoabsorption_spectrum
from pyramids.io.output import writeGPAWdipole
from pyramids.io.result import getDipole
import os

print os.path.abspath('.')
name= os.path.abspath('.').split('/')[-1]

fig,ax = plt.subplots(1,1,figsize=(6, 6 / 2 ** 0.5))
colors = ['r','g','b']
direct = ['x','y','z']
for i in range(3):
  os.chdir(direct[i])
  time, dipole = getDipole()
  kick = [0.0, 0.0, 0.0]
  kick[i] = 1e-1
  print time.shape, dipole.shape
  writeGPAWdipole(name+str(i)+'.dm',kick,time,dipole)
  photoabsorption_spectrum(name+str(i)+'.dm', name+str(i)+'.spec', width=0.001)
  data = np.loadtxt(name+str(i)+'.spec')
  ax.plot(data[:, 0], data[:, 1]/data[:, 0], colors[i],label=direct[i])
  os.chdir('..')
  
setProperty(ax,**getPropertyFromPosition(title=r'Absorption spectrum of '+name,
                                         xlabel='eV',
                                         ylabel='Absorption (arbitrary units)'))
plt.tight_layout()
for save_type in ['.pdf','.png']:
  filename = name + save_type
  plt.savefig(filename,dpi=600)