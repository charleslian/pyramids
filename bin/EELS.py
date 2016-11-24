import pyramids.io.result as dp
import pyramids.plot.setting as ma
import os
SaveName = __file__.split('/')[-1].split('.')[0]
dirName = os.path.abspath('.').split('/')[-1]
label = dirName.replace('&&','\\').replace('&',' ')

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import numpy as np

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')

from ase.io import write, read
atoms = read('structure.vasp',format='vasp')

fig, axs = plt.subplots(3,1,figsize=(6,8))



Q = np.loadtxt('q_list') #q_list include all the q length 

# Read data, loop all q
# Energy array saved to E, omega append to Z
Z = []

for i, q in enumerate(Q):
  filename = 'EELS_' + str(i+1) 
  d = np.loadtxt(filename, delimiter=',')
  E = d[:, 0]
  C = d[:, 2]
  Z.append(C)

# to plot contour, transpose Z is needed (exchange x and y)
 # get all the element index less than 2 eV
selectIndex = np.where( E < 5 )

contour = np.transpose(np.array(Z))
X, Y = np.meshgrid(Q, E[selectIndex])

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
ax = axs[0]
ax1 = axs[1]
c = ma.getColors(Q.shape[0])
#print np.sqrt(np.abs(np.log(Q)))
print atoms.cell
#Q = np.array(Q)
latticeVector = np.linalg.norm(atoms.cell[0,:])/(2*np.pi)
print latticeVector
dispersion = Q*np.sqrt(np.abs(np.log(Q*latticeVector)))


print dispersion
maxE = np.ones(Q.shape[0])*3.5*dispersion + 0.3


def d1dispersion(q,A,a=1):
  return A*q*np.sqrt(np.abs(np.log(q*a)))

qfit = np.linspace(0.0001,0.9999,200)

axs[2].plot(qfit/latticeVector,d1dispersion(qfit,7.6),'-',lw=3)

print maxE
for i, q in enumerate(Q):
  from scipy.signal import argrelextrema
  #extremM = [ext for ext in argrelextrema(Z[i][np.where( E < 2 + i*0.2 )], np.less, order=1)[0]]
  #print extremM
  extreme = [ext for ext in argrelextrema(Z[i][np.where(E < maxE[i])], np.greater, order=80)[0]]
  exX = np.array([d[ext,0] for ext in extreme])
  exY = np.array([Z[i][ext] for ext in extreme])
  #miX = np.array([d[ext,0] for ext in extremM])
  #miY = np.array([Z[i][ext] for ext in extremM])
  ax1.scatter(q*np.ones(exY.shape[0]),exY,30,lw=0.0)
  #ax1.scatter(q*np.ones(miY.shape[0]),miY,miX*30,lw=0.0,color='r')
  #print extreme
  #ax.fill_between(E,C[i],color='r',zs=i*0.01, zdir='z')
  shift =  -i*0.0
  #ax.plot(E[selectIndex],Z[i][selectIndex], lw=1, color=c[i])
  ax.fill_between(E[selectIndex],Z[i][selectIndex]+shift, shift, lw=3, color=c[i])
  axs[2].plot(q*np.ones(exX.shape[0]),exX,'or')
  ax.plot(exX,exY,'ob')
  

                 
args = ma.getPropertyFromPosition(#ylimits=[None,0.2], xlimits=[None,5],
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