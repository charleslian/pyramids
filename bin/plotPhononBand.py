from pyramids.io.result import getBands
from pyramids.plot.setting import getPropertyFromPosition, setProperty
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------
fig,ax=plt.subplots(1,1)

X, Ek, xticks, xticklabels = getBands()

import numpy as np
for ispin in range(Ek.shape[2]):
  for iband in range(1,Ek.shape[1]):
    ax.plot(X[:],Ek[:,iband,ispin]*0.03,'b.',lw=2)
    
xticklabels = [label.replace('Gamma','\Gamma') for label in xticklabels]
kargs=getPropertyFromPosition(ylabel=r'$\omega$(THz)') #
kargs['xlimits'] = [X.min(),X.max()]
kargs['ylimits'] = None
kargs['xticks'] = xticks
kargs['xticklabels'] = xticklabels
kargs['vline'] = xticks[1:-1]
kargs['hline'] = [0.0]
setProperty(ax,**kargs)

plt.tight_layout()
SaveName = __file__.split('/')[-1].split('.')[0]+'i'
for save_type in ['.pdf','.png']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)
