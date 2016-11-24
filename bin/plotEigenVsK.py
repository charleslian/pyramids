import numpy as np
import pyramids.plot.setting as ma
from pyramids.io.fdf import tdapOptions
import pyramids.io.result as dp
import matplotlib.pyplot as plt
import os
import pyramids.io.result as dp
from pyramids.io.result import getHomo
SaveName = __file__.split('/')[-1].split('.')[0]
fig1, ax = plt.subplots(1,1,sharey=True,sharex=True,figsize=(8,6))
eigenvalues = dp.readEigFile()

k = np.arange(eigenvalues.shape[0])
print k
k = []
for i in range(120,785,95):
  k.append(i)
  k.append(i+47)
for i in range(785,746,-1):
  k.append(i)

k = np.array(k) - 1

y = eigenvalues
#plotedBand = getHomo()

ax.plot(np.arange(k.shape[0]),eigenvalues[k,:],'-o')

args = ma.getPropertyFromPosition(xlabel=r'$n_k$', ylimits=[-2,2],
                                  ylabel=r'Eigenvalues(eV)')
ma.setProperty(ax,**args)
plt.tight_layout()

for save_type in ['.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)