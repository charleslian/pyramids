import pyramids.io.result as dp
import pyramids.plot.setting as ma
import os
SaveName = __file__.split('/')[-1].split('.')[0]
dirName = os.path.abspath('.').split('/')[-1]
label = dirName.replace('&&','\\').replace('&',' ')

from matplotlib import pyplot as plt
import numpy as np

fig, axs = plt.subplots(1,2,sharex=False,sharey=False,figsize=(10,6))
Q = np.loadtxt('q_list')


C = []
extrema = np.zeros([len(Q),100])
numExtreme = 1
print extrema.shape

for i, q in enumerate(Q):
  filename = 'EELS_' + str(i+1) 
  d = np.loadtxt(filename, delimiter=',')
  E = d[:, 0]
  from scipy.signal import argrelextrema
  extreme = [ext for ext in argrelextrema(d[:,2], np.greater, order=50)[0]]
  exY = np.array([d[ext,0] for ext in extreme])
  exX = np.array([q for ext in extreme])
  C.append(d[:,2])
    
Z = np.transpose(np.array(C))  
X, Y = np.meshgrid(Q, E)

mainX = None
mainY = None
mainV = 1.0  
zoomX = None
zoomY = None
zoomV = 1.0

if os.path.exists('localSetting.py'):
  from localSetting import EELS
  mainX = EELS.mainX
  mainY = EELS.mainY
  mainV = EELS.mainV  
  zoomX = EELS.zoomX
  zoomY = EELS.zoomY
  zoomV = EELS.zoomV

if zoomX is not None:
  zoomX[0] = Q[0]
  
v = [mainV, zoomV]
x = [mainX, zoomX]
y = [mainY, zoomY]

nContour = 300#Q.shape[0] # * 5
cmap = 'hot'
for iax in range(2):
  ax = axs[iax]
  for f in ax.contour, ax.contourf:  
    ct = f(X, Y, (Z), nContour, cmap=cmap, alpha = 1.0, )
              #vmax=np.max(Z[2:]))np.log
        
  plt.colorbar(ct,ax=ax)          
  args = ma.getPropertyFromPosition(iax,ylimits=y[iax], xlimits=x[iax],
                                    grid = False,
                                    title='EELS spectra: $%s$' % label,
                                    xlabel=r'q ($\AA^{-1}$)',
                                    ylabel='Energy (eV)')
  ma.setProperty(ax,**args)
  
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
mark_inset(axs[0], axs[1], loc1=2, loc2=3, fc="none", ec="0.5",ls='--',lw=3,zorder=100)

plt.tight_layout()
for save_type in ['.png','.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)