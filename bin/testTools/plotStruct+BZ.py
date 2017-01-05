import numpy as np
from scipy.fftpack import fft, ifft

from pyramids.plot.setting import getPropertyFromPosition, setProperty, getColors
from pyramids.io.fdf import tdapOptions
import pyramids.io.result as dp
from pyramids.plot.PlotUtility import insertImag
import matplotlib.pyplot as plt
from ase.calculators.siesta.import_functions import xv_to_atoms
import ase

fig, axs = plt.subplots(2,1,figsize=(7,8))
SaveName = __file__.split('/')[-1].split('.')[0]

atoms = xv_to_atoms('siesta.XV')
#atoms = ase.atoms.Atoms(symbols=atom_temp.get_chemical_symbols(),
#                        positions=atom_temp.get_positions(),
#                        cell = atom_temp.get_cell())
view(atoms)
ax = axs[0]

insertImag(ax)
colors = ['r','g','b']
ax.annotate(s='',xy=(0.4,0),xytext=(0,0),xycoords='axes fraction',
              arrowprops=dict(width=2.0,color=colors[0])) 
              
ax.text(0.45,-0.02,'x',fontsize='xx-large',transform=ax.transAxes)
ax.text(0,0.45,'y',fontsize='xx-large',transform=ax.transAxes)
ax.text(0.22,0.22,'z',fontsize='xx-large',transform=ax.transAxes)
 
ax.annotate(s='',xy=(0,0.4),xytext=(0,0),xycoords='axes fraction',
              arrowprops=dict(width=2.0,color=colors[1]))  
ax.annotate(s='',xy=(0.2,0.2),xytext=(0,0),xycoords='axes fraction',
              arrowprops=dict(width=2.0,color=colors[2])) 
kargs=getPropertyFromPosition(0,r'',"",title='Structure',)
setProperty(ax,**kargs)     
       
# --------------------------------------b----------------------------------   
reciprocal_vectors = 2*np.pi*atoms.get_reciprocal_cell()
kcoor, kweight = dp.readKpoints()
points=np.array([(reciprocal_vectors[0,0:2]*i+
                  reciprocal_vectors[1,0:2]*j+
                  reciprocal_vectors[2,0:2]*k) 
                  for i in range(-1,2) 
                  for j in range(-1,2)
                  for k in range(0,1)])
print points[:,0].max(), points[:,0].min()
from scipy.spatial import Voronoi, voronoi_plot_2d

vor = Voronoi(points)
numKpts = kcoor.shape[0]
direct = 0
ax = axs[1]
voronoi_plot_2d(vor,ax)
dim1 = direct%3
dim2 = (direct+1)%3

xlimits = [points[:,dim1].min(), points[:,dim1].max()]
ylimits = [points[:,dim2].min(), points[:,dim2].max()]
print xlimits
#for i in range(numKpts):
#  an1 = ax.annotate(str(i+1), xy=(kcoor[i,dim1], kcoor[i,dim2]), xycoords="data",
#                    va="center", ha="center", fontsize=50.0/np.sqrt(numKpts), color='r',
#                    bbox=dict(boxstyle="circle", fc='w',alpha=0.2))
import os
if os.path.exists('localSetting.py'):
  import localSetting as ls
  lines = ls.BZ.lines
  xlimits = ls.BZ.xlimits
  ylimits = ls.BZ.xlimits
  for index, line in enumerate(lines):
    #x = [kcoor[line[0],0],kcoor[line[1],0]]
    #y = [kcoor[line[0],1],kcoor[line[1],1]]
    initial = kcoor[line[0],:2]
    final = kcoor[line[1],:2]
    print line
    ax.annotate(s='',xytext=initial, xy=final,
                xycoords='data',
                arrowprops=dict(color='b',width = 2.0, headwidth = 6,shrink=0.005)) 
    ax.annotate(ls.specialKPoints[index], xy=initial, xycoords="data",
                fontsize='xx-large', color='k',
                #bbox=dict(boxstyle="circle",alpha=0.4,color='y')
                )
    if index == len(lines) - 1:
      ax.annotate(ls.specialKPoints[index + 1], xytext=final, 
                  xy=final, xycoords="data",
                  fontsize='xx-large', color='k',
                  #bbox=dict(boxstyle="circle",alpha=0.4,color='y')
                  )
                
                
kargs=getPropertyFromPosition(1,r'$k_x(\AA^{-1})$',"$k_y(\AA^{-1})$",
                              title='Brillouin zone',
                              xlimits=xlimits,
                              ylimits=ylimits
                              )

ax.axis('equal')                                  
setProperty(ax,**kargs)  

plt.tight_layout()
for save_type in ['.pdf']:
  filename = SaveName + save_type
  plt.savefig(filename,orientation='portrait',dpi=600)