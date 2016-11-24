import pyramids.io.result as dp
import pyramids.plot.setting as ma
import os
SaveName = __file__.split('/')[-1].split('.')[0]
dirName = os.path.abspath('.').split('/')[-1]
label = dirName.replace('&&','\\').replace('&',' ')
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
Q = np.loadtxt('q_list')


C = []
extrema = np.zeros([len(Q),100])
numExtreme = 1
print extrema.shape

for i, q in enumerate(Q):
  filename = 'EELS_' + str(i+1) 
  d = np.loadtxt(filename, delimiter=',')
  E = d[:, 0]
  C.append(d[:,2])


Z = np.transpose(np.array(C))  
X, Y = np.meshgrid(Q, E)

#from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
#ax = [ax, zoomed_inset_axes(ax, 2, loc=1)]#
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

nContour = 400 #Q.shape[0] * 5
cmap = 'jet'
for i, q in enumerate(Q):
  from scipy.signal import argrelextrema
  extreme = [ext for ext in argrelextrema(C[i], np.greater)[0]]
  exX = np.array([d[ext,0] for ext in extreme])
  exY = np.array([C[i][ext] for ext in extreme])
  print extreme
  #ax.fill_between(E,C[i],color='r',zs=i*0.01, zdir='z')
  ax.plot(E,C[i],color='r',zs=i*0.01, zdir='z')
  #ax.plot(exX,exY,'ob')
  

                 
args = ma.getPropertyFromPosition(ylimits=[None,0.2], xlimits=[None,5],
                                    grid = False,
                                    title='EELS spectra: $%s$' % label,
                                    #ylabel=r'q($\AA^{-1}$)',
                                    xlabel='Energy(eV)')
ma.setProperty(ax,**args)
  
#from mpl_toolkits.axes_grid1.inset_locator import mark_inset
#mark_inset(axs[0], axs[1], loc1=2, loc2=3, fc="none", ec="0.5",ls='--',lw=3,zorder=100)

plt.tight_layout()
for save_type in ['.png','.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)