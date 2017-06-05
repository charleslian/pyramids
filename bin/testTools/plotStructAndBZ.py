import numpy as np
from scipy.fftpack import fft, ifft
from pyramids.plot.setting import getPropertyFromPosition, setProperty, getColors
from pyramids.io.fdf import tdapOptions
import pyramids.io.result as dp
from pyramids.plot.PlotUtility import insertImag,generateStructPNG,confStructrueFigure
import matplotlib.pyplot as plt


fig, axs = plt.subplots(2,1,figsize=(4,8))
SaveName = __file__.split('/')[-1].split('.')[0]

iStruct = 0
iBZone  = 1

#from ase.calculators.siesta.import_functions import xv_to_atoms
#atoms = xv_to_atoms('siesta.XV')

import os

atoms = dp.getStructrue()

  
# --------------------------------------a----------------------------------   
ax = axs[iStruct]

generateStructPNG(atoms,cell=True,repeat = [5,3,1])
insertImag(ax)
#confStructrueFigure(ax)

kargs = getPropertyFromPosition(iStruct,r'',"",title='Structure',)
setProperty(ax,**kargs)     
# --------------------------------------b----------------------------------   
ax = axs[iBZone]
reciprocal_vectors = 2*np.pi*atoms.get_reciprocal_cell()
#print reciprocal_vectors
points=np.array([(reciprocal_vectors[0,0:2]*i+
                  reciprocal_vectors[1,0:2]*j+
                  reciprocal_vectors[2,0:2]*k) 
                  for i in range(-1,2) 
                  for j in range(-1,2)
                  for k in range(-0,1)])

from scipy.spatial import Voronoi
from pyramids.plot.PlotUtility import voronoi_plot_2d
vor = Voronoi(points)
voronoi_plot_2d(vor,ax)

import os
if os.path.exists('input.fdf'):
  kcoor, kweight = dp.readKpoints()
  kall, klist = dp.recoverAllKPoints(kcoor, reciprocal_vectors)
  ax.plot(kcoor[:,0], kcoor[:,1],'o')
  ax.plot(kall[:,0], kall[:,1],'.')

xlimits = [min(points[:,0]),max(points[:,0])]
ylimits = [min(points[:,1]),max(points[:,1])]

if os.path.exists('localSetting.py'):
  import localSetting as ls
  lines = ls.BZ.lines
  if ls.BZ.xlimits is not None:
    xlimits = ls.BZ.xlimits
  if ls.BZ.ylimits is not None:  
    ylimits = ls.BZ.ylimits 
    
  for index, line in enumerate(lines):
    initial = np.dot(line[0],reciprocal_vectors)[:2]
    final = np.dot(line[1],reciprocal_vectors)[:2]
    specialKPoints = ls.BZ.specialKPoints[index]
    
    ax.annotate(s='',xytext=initial, xy=final,
                xycoords='data',
                arrowprops=dict(color='b',width = 2.0, alpha=0.5, headwidth = 6,shrink=0.005)) 
    ax.annotate(specialKPoints[0], xy=initial, xycoords="data",
                fontsize='xx-large', color='k', 
                #bbox=dict(boxstyle="circle",alpha=0.4,color='y')
                )
    ax.annotate(specialKPoints[1], xy=final, xycoords="data",
                fontsize='xx-large', color='k', 
                #bbox=dict(boxstyle="circle",alpha=0.4,color='y')
                )
                              
kargs=getPropertyFromPosition(iBZone,r'$k_x (/\AA)$',"$k_y (/\AA)$",
                              title='Brillouin zone', grid=False,
                              xlimits=xlimits,
                              ylimits=ylimits,
                              #xticklabels=[],
                              #,yticklabels=[]
                              )
ax.axis('equal')
                          
setProperty(ax,**kargs)
# --------------------------------------Final----------------------------------   
plt.tight_layout()
for save_type in ['.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)