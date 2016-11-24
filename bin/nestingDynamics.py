import numpy as np
from scipy.fftpack import fft, ifft

from pyramids.plot.setting import getPropertyFromPosition, setProperty, getColors
from pyramids.io.fdf import tdapOptions
import pyramids.io.result as dp
from pyramids.plot.PlotUtility import insertImag,generateStructPNG
import matplotlib.pyplot as plt


fig, axs = plt.subplots(1,1,figsize=(8,6))
SaveName = __file__.split('/')[-1].split('.')[0]

iStruct = 0
iBZone  = 0

from ase.calculators.siesta.import_functions import xv_to_atoms
atoms = xv_to_atoms('siesta.XV')
# --------------------------------------a----------------------------------
# --------------------------------------b----------------------------------
ax = axs
reciprocal_vectors = 2*np.pi*atoms.get_reciprocal_cell()
#print reciprocal_vectors
points=np.array([(reciprocal_vectors[0,0:2]*i+
                reciprocal_vectors[1,0:2]*j+
                reciprocal_vectors[2,0:2]*k)
                for i in range(-1,2)
                for j in range(-1,2)
                for k in range(0,1)])

#from ase.dft.kpoints import monkhorst_pack
#kpts = np.array([np.dot(k,atoms.cell) for k in monkhorst_pack((12,12,1))])

from scipy.spatial import Voronoi, voronoi_plot_2d
vor = Voronoi(points)
voronoi_plot_2d(vor,ax)

eigen = dp.readEigFile('siesta.EIG')
time, partAll  = dp.getProjectedPartition()


xlimits = None
ylimits = None

if os.path.exists('localSetting.py'):
  import localSetting as ls
  conf  = ls.nesting
  xlimits = conf.xlimits
  ylimits = conf.ylimits
  
import os
kargs=getPropertyFromPosition(xlabel=r'$k_x (\AA^{-1})$',
                            ylabel=r"$k_y (\AA^{-1})$",
                            title='', grid=False,
                            xlimits=xlimits,
                            ylimits=ylimits,
                            #xticklabels=[],
                            #,yticklabels=[]
                            )
ax.axis('equal')
setProperty(ax,**kargs)

print eigen.shape

lb = 0
rb = 22

sc = ax.scatter([0,0], [0,0], s=0, c=[lb,rb], lw = 0.0, cmap = 'jet')

def plotPart(num):
  data = []
  part = partAll[num] - partAll[0]
  kcoor, kweight = dp.readKpoints()
  
  kall = [kcoor[:,:2] + point for point in points]
  kall.extend([-kcoor[:,:2] + point for point in points])
  
  for k1 in kall:
    for k in range(eigen.shape[0]):
      x = eigen[k,:]
      data.extend([(k1[k,0], k1[k,1], value, part[k,index])
                   for index, value in enumerate(x)
                   if lb < value < rb and part[k,index] > 3E-6])
  if len(data) != 0:
    data = np.array(data)
    sc.remove()
    sc = ax.scatter(data[:,0], data[:,1], s=data[:,3]*3E3,
                   c=data[:,2], lw =0.0, cmap = 'jet')
    #sc.remove()
  
  #cb = plt.colorbar(sc,format='%3.1f')
  #cb.remove()
  #cb.set_label('Energy (eV)',fontsize='xx-large')


from matplotlib import animation
def update(num):
  """updates the horizontal and vertical vector components by a
  fixed increment on each frame
  """
  cycle = partAll.shape[0]
  
  #x = np.arange(kpath.shape[0])
  print num,
  i = num*10 % cycle
  plotPart(i)
  
anim = animation.FuncAnimation(fig, update, interval=40, blit=False)
